import streamlit as st
import uuid
from utils.rate_limiter import gemini_rate_limiter
from datetime import datetime
from utils.database import (
    get_pending_properties, execute_query, get_snowflake_connection
)
from utils.ai_analysis import analyze_property_image, parse_inspector_notes, generate_inspection_summary
from utils.cost_calculator import (
    calculate_risk_score, assign_risk_level, 
    calculate_renovation_costs, get_improvement_recommendations, get_statistics
)
from PIL import Image
from utils.theme import init_theme, toggle_theme, apply_theme_styles
import io

st.set_page_config(
    page_title="Inspector Dashboard - Nivaasika",
    page_icon="🔍",
    layout="wide"
)
# Initialize and apply theme
init_theme()
apply_theme_styles()

# Theme toggle
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, key="theme_toggle"):
        toggle_theme()
        st.rerun()

# Initialize view state
if 'inspector_view' not in st.session_state:
    st.session_state.inspector_view = 'list'

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        margin-bottom: 1rem;
    }
    .property-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #FF6B35;
    }
    .room-section {
        background-color: #e9ecef;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔍 Inspector Dashboard</div>', unsafe_allow_html=True)
st.markdown("Inspect properties, upload images, and let AI analyze defects.")

st.markdown("---")
#Test secrets loading
""" st.write("🔍 Debug Info:")
st.write("Secrets available:", list(st.secrets.keys()))
st.write("Has GEMINI_API_KEY:", 'GEMINI_API_KEY' in st.secrets)

if 'GEMINI_API_KEY' in st.secrets:
    key = st.secrets['GEMINI_API_KEY']
    st.success(f"✅ API Key loaded: {key[:20]}...")
else:
    st.error("❌ GEMINI_API_KEY not found!")
    st.write("Available keys:", list(st.secrets.keys())) """
# View: Pending Properties List
if st.session_state.inspector_view == 'list':
    st.subheader("🏠 Properties Awaiting Inspection")
    
    with st.spinner("Loading pending properties..."):
        result = get_pending_properties()
        
        if result and result.get('data'):
            st.success(f"Found {len(result['data'])} properties pending inspection")
            
            for row in result['data']:
                (prop_id, seller_name, seller_email, address, city, state, pincode, 
                prop_type, bedrooms, bathrooms, sqft, price, description, landmarks, 
                status, created_at, inspected_at, risk_score, risk_level, 
                reno_min, reno_max, affected_rooms, total_defects, critical_issues) = row
                
                with st.container():
                    st.markdown(f"""
                    <div class="property-card">
                        <h3>{address}</h3>
                        <p><strong>📍 Location:</strong> {city}, {state} - {pincode}</p>
                        <p><strong>🏠 Type:</strong> {prop_type} | {bedrooms} BHK | {sqft} sq ft</p>
                        <p><strong>💰 Price:</strong> ₹{price:,}</p>
                        <p><strong>📝 Description:</strong> {description}</p>
                        <p><strong>🗺️ Landmarks:</strong> {landmarks}</p>
                        <p><strong>👤 Seller:</strong> {seller_name} ({seller_email})</p>
                        <p><strong>🆔 Property ID:</strong> {prop_id}</p>
                        <p><strong>📅 Listed:</strong> {created_at.strftime('%Y-%m-%d %H:%M')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🔍 Inspect This Property", key=f"inspect_{prop_id}"):
                        st.session_state.selected_property = prop_id
                        st.session_state.property_details = {
                            'id': prop_id,
                            'address': address,
                            'city': city,
                            'type': prop_type,
                            'seller': seller_name
                        }
                        st.session_state.inspector_view = 'inspect'
                        st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("✅ No properties pending inspection at the moment.")

# View: Conduct Inspection
elif st.session_state.inspector_view == 'inspect':
    if 'selected_property' not in st.session_state:
        st.warning("⚠️ No property selected.")
        if st.button("← Back to Properties List"):
            st.session_state.inspector_view = 'list'
            st.rerun()
    else:
        property_id = st.session_state.selected_property
        prop_details = st.session_state.property_details
        
        # Back button
        if st.button("← Back to Properties List"):
            st.session_state.inspector_view = 'list'
            st.rerun()
        
        st.success(f"📸 Conducting Inspection: **{prop_details['address']}** (ID: {property_id})")
        
        st.markdown("---")
        
        # Inspector email
        inspector_email = st.text_input("Inspector Email *", placeholder="inspector@nivaasika.com")
        
        st.markdown("### 📸 Upload Images Room-wise")
        
        rooms = ["Kitchen", "Living Room", "Master Bedroom", "Bedroom 2", "Bedroom 3", 
                 "Bathroom 1", "Bathroom 2", "Balcony", "Other"]
        
        if 'all_findings' not in st.session_state:
            st.session_state.all_findings = []
        
        for room in rooms:
            with st.expander(f"📍 {room}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    uploaded_files = st.file_uploader(
                        f"Upload images for {room}",
                        type=['jpg', 'jpeg', 'png'],
                        accept_multiple_files=True,
                        key=f"upload_{room}"
                    )
                
                with col2:
                    room_notes = st.text_area(
                        f"Inspector notes for {room}",
                        placeholder="Any observations...",
                        height=100,
                        key=f"notes_{room}"
                    )
                
                if uploaded_files:
                    st.info(f"📸 {len(uploaded_files)} image(s) uploaded for {room}")
                    
                    cols = st.columns(min(len(uploaded_files), 4))
                    for idx, file in enumerate(uploaded_files):
                        with cols[idx % 4]:
                            image = Image.open(file)
                            st.image(image, caption=file.name, use_container_width=True)
                    
                    if st.button(f"🤖 Analyze {room} Images", key=f"analyze_{room}"):
                        with st.spinner(f"AI is analyzing {room} images..."):
                            for file in uploaded_files:
                                file.seek(0)
                                defects = analyze_property_image(file, room)
                                
                                for defect in defects:
                                    finding = {
                                        'property_id': property_id,
                                        'room_name': room,
                                        'defect_type': defect['defect_type'],
                                        'severity': defect['severity'],
                                        'description': defect['description'],
                                        'source': 'image_ai'
                                    }
                                    st.session_state.all_findings.append(finding)
                            
                            if room_notes:
                                notes_defects = parse_inspector_notes(room_notes, room)
                                for defect in notes_defects:
                                    finding = {
                                        'property_id': property_id,
                                        'room_name': room,
                                        'defect_type': defect['defect_type'],
                                        'severity': defect['severity'],
                                        'description': defect['description'],
                                        'source': 'inspector_notes'
                                    }
                                    st.session_state.all_findings.append(finding)
                            
                            st.success(f"✅ {room} analyzed successfully!")
                            st.rerun()
        
        st.markdown("---")
        
        if st.session_state.all_findings:
            st.markdown("### 📋 Current Findings")
            st.info(f"Total defects found: **{len(st.session_state.all_findings)}**")
            
            findings_df_data = []
            for f in st.session_state.all_findings:
                findings_df_data.append({
                    'Room': f['room_name'],
                    'Defect': f['defect_type'],
                    'Severity': f['severity'],
                    'Description': f['description'],
                    'Source': f['source']
                })
            
            st.dataframe(findings_df_data, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### ✅ Submit Inspection Report")
            
            if st.button("🚀 Generate Report & Submit", type="primary", use_container_width=True):
                if not inspector_email or '@' not in inspector_email:
                    st.error("Please enter a valid inspector email!")
                else:
                    with st.spinner("Processing inspection data..."):
                        risk_score = calculate_risk_score(st.session_state.all_findings)
                        risk_level = assign_risk_level(risk_score)
                        min_cost, max_cost = calculate_renovation_costs(st.session_state.all_findings)
                        stats = get_statistics(st.session_state.all_findings)
                        recommendations = get_improvement_recommendations(st.session_state.all_findings)
                        
                        conn = get_snowflake_connection()
                        cursor = conn.cursor()
                        
                        try:
                            for finding in st.session_state.all_findings:
                                finding_id = f"FIND_{uuid.uuid4().hex[:8].upper()}"
                                cursor.execute("""
                                INSERT INTO INSPECTION_FINDINGS 
                                (finding_id, property_id, room_name, defect_type, severity, description, source)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    finding_id, finding['property_id'], finding['room_name'],
                                    finding['defect_type'], finding['severity'], 
                                    finding['description'], finding['source']
                                ))
                            
                            for rec in recommendations:
                                improvement_id = f"IMP_{uuid.uuid4().hex[:8].upper()}"
                                cursor.execute("""
                                INSERT INTO PROPERTY_IMPROVEMENTS
                                (improvement_id, property_id, defect_type, improvement_action, 
                                 estimated_cost_range, priority, affected_rooms)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    improvement_id, property_id, rec['defect_type'],
                                    rec['action'], rec['cost_range'], rec['priority'], 
                                    rec['affected_rooms']
                                ))
                            
                            summary_text = generate_inspection_summary(
                                {'address': prop_details['address'], 'risk_score': risk_score},
                                st.session_state.all_findings
                            )
                            
                            summary_id = f"SUM_{uuid.uuid4().hex[:8].upper()}"
                            cursor.execute("""
                            INSERT INTO INSPECTION_SUMMARY
                            (summary_id, property_id, summary_text, total_defects, 
                            critical_issues, affected_rooms)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """, (
                                summary_id, property_id, summary_text,
                                stats['total_defects'], stats['critical_issues'], 
                                stats['affected_rooms']
                            ))
                            
                            cursor.execute("""
                            UPDATE PROPERTIES SET
                                status = 'inspected',
                                inspected_at = CURRENT_TIMESTAMP(),
                                risk_score = %s,
                                risk_level = %s,
                                total_renovation_cost_min = %s,
                                total_renovation_cost_max = %s,
                                affected_rooms = %s,
                                total_defects = %s,
                                critical_issues = %s
                            WHERE property_id = %s
                            """, (
                                risk_score, risk_level, min_cost, max_cost,
                                stats['affected_rooms'], stats['total_defects'],
                                stats['critical_issues'], property_id
                            ))
                            
                            conn.commit()
                            
                            st.success("✅ Inspection completed successfully!")
                            st.balloons()
                            
                            st.markdown("### 📊 Inspection Summary")
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Risk Score", f"{risk_score}")
                            col2.metric("Risk Level", risk_level)
                            col3.metric("Total Defects", stats['total_defects'])
                            col4.metric("Critical Issues", stats['critical_issues'])
                            
                            st.markdown("---")
                            st.markdown("### 💰 Total Renovation Cost Estimate")
                            col_min, col_max = st.columns(2)
                            with col_min:
                                st.metric("Minimum Cost", f"₹{min_cost:,}")
                            with col_max:
                                st.metric("Maximum Cost", f"₹{max_cost:,}")
                            
                            st.info(summary_text)
                            
                            del st.session_state.selected_property
                            del st.session_state.all_findings
                            del st.session_state.property_details
                            st.session_state.inspector_view = 'list'
                            
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Error: {str(e)}")
                        finally:
                            cursor.close()
        else:
            st.info("Upload and analyze images from at least one room to generate findings.")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Inspector Stats")
    
    total_query = "SELECT COUNT(*) FROM PROPERTIES WHERE status = 'inspected'"
    total_result = execute_query(total_query)
    if total_result and total_result.get('data'):
        inspected_count = total_result['data'][0][0]
        st.metric("Properties Inspected", inspected_count)
    
    pending_query = "SELECT COUNT(*) FROM PROPERTIES WHERE status = 'pending'"
    pending_result = execute_query(pending_query)
    if pending_result and pending_result.get('data'):
        pending_count = pending_result['data'][0][0]
        st.metric("Pending Inspection", pending_count)
    
    st.markdown("---")

    st.markdown("### 🔒 API Rate Limit")
    remaining = gemini_rate_limiter.get_remaining_requests()
    reset_time = int(gemini_rate_limiter.get_reset_time())
    st.success(f"✅ {remaining}/10 requests available")
    st.caption(f"Resets in {reset_time}s")
    st.markdown("---")
    
    st.markdown("### 💡 Inspection Tips")
    st.info("""
    - Upload clear, well-lit images
    - Cover all rooms systematically
    - Add detailed notes for context
    - Focus on visible defects
    - Multiple angles help AI accuracy
    """)

st.markdown("---")
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")