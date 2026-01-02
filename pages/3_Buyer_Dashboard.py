import streamlit as st
import base64
from utils.database import (
    get_inspected_properties, get_property_details, 
    get_property_findings, get_property_improvements, 
    get_inspection_summary, execute_query, get_property_gallery
)
from utils.theme import init_theme, toggle_theme, apply_theme_styles, get_theme_colors

st.set_page_config(
    page_title="Buyer Dashboard - Nivaasika",
    page_icon="🏠",
    layout="wide"
)

# Initialize and apply theme
init_theme()
apply_theme_styles()

# Get theme colors
colors = get_theme_colors()

# Theme toggle
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, key="theme_toggle"):
        toggle_theme()
        st.rerun()

# Header
st.markdown('<div class="main-header">🏠 Buyer Dashboard</div>', unsafe_allow_html=True)
st.markdown("Browse inspected properties with complete transparency and risk assessment.")

st.markdown("---")

# Initialize session state
if 'selected_property_id' not in st.session_state:
    st.session_state.selected_property_id = None

# Sidebar - Filters
with st.sidebar:
    st.markdown("### 🔍 Filter Properties")
    
    risk_filter = st.multiselect("Risk Level", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])
    st.markdown("#### Price Range (₹)")
    min_price = st.number_input("Min Price", min_value=0, value=0, step=100000)
    max_price = st.number_input("Max Price", min_value=0, value=100000000, step=100000)
    prop_types = st.multiselect("Property Type", ["Apartment", "Independent House", "Villa", "Penthouse", "Studio Apartment"], default=["Apartment", "Independent House", "Villa", "Penthouse", "Studio Apartment"])
    city_filter = st.text_input("City", placeholder="e.g., Mumbai")
    apply_filters = st.button("Apply Filters", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Market Stats")
    total_result = execute_query("SELECT COUNT(*) FROM PROPERTIES WHERE status = 'inspected'")
    if total_result and total_result.get('data'):
        st.metric("Total Inspected", total_result['data'][0][0])
    low_risk_result = execute_query("SELECT COUNT(*) FROM PROPERTIES WHERE status = 'inspected' AND risk_level = 'Low'")
    if low_risk_result and low_risk_result.get('data'):
        st.metric("Low Risk Properties", low_risk_result['data'][0][0])

# Main content
if st.session_state.selected_property_id:
    property_id = st.session_state.selected_property_id
    
    if st.button("← Back to All Properties"):
        st.session_state.selected_property_id = None
        st.rerun()
    
    st.markdown("---")
    
    with st.spinner("Loading property details..."):
        prop_result = get_property_details(property_id)
        
        if prop_result and prop_result.get('data'):
            prop_data = prop_result['data'][0]
            (prop_id, seller_name, seller_email, address, city, state, pincode, prop_type, bedrooms, bathrooms, sqft, price, description, landmarks, status, created_at, inspected_at, risk_score, risk_level, reno_min, reno_max, affected_rooms, total_defects, critical_issues) = prop_data
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"## {address}")
                st.markdown(f"📍 {city}, {state} - {pincode}")
            with col2:
                risk_class = f"risk-{risk_level.lower()}"
                st.markdown(f'<div class="{risk_class}">Risk: {risk_level}</div>', unsafe_allow_html=True)
                st.markdown(f"**Risk Score:** {risk_score}")
            
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("**💰 Price**")
                st.markdown(f"<h3 style='margin:0; color: {colors['text']}'>₹{price:,}</h3>", unsafe_allow_html=True)
            with col2:
                st.markdown("**🏠 Type**")
                st.markdown(f"<h4 style='margin:0; color: {colors['text']}'>{prop_type}</h4>", unsafe_allow_html=True)
            with col3:
                st.markdown("**📐 Area**")
                st.markdown(f"<h4 style='margin:0; color: {colors['text']}'>{sqft} sq ft</h4>", unsafe_allow_html=True)
            with col4:
                st.markdown("**🛏️ Configuration**")
                st.markdown(f"<h4 style='margin:0; color: {colors['text']}'>{bedrooms}BHK, {bathrooms}Bath</h4>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Inspection Summary", "🔍 Defects Found", "🔧 Improvements Needed", "📸 House Gallery", "ℹ️ Property Info"])
            
            with tab1:
                summary_result = get_inspection_summary(property_id)
                if summary_result and summary_result.get('data'):
                    summary_data = summary_result['data'][0]
                    summary_text, tot_defects, crit_issues, aff_rooms = summary_data
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown("**🔍 Total Defects**")
                        st.markdown(f"<h2 style='color:#FF6B35;margin:0'>{tot_defects}</h2>", unsafe_allow_html=True)
                    with col2:
                        st.markdown("**⚠️ Critical Issues**")
                        st.markdown(f"<h2 style='color:#dc3545;margin:0'>{crit_issues}</h2>", unsafe_allow_html=True)
                    with col3:
                        st.markdown("**🏠 Affected Rooms**")
                        st.markdown(f"<h2 style='color:#fd7e14;margin:0'>{aff_rooms}</h2>", unsafe_allow_html=True)
                    with col4:
                        st.markdown("**💰 Renovation Cost**")
                        st.markdown(f"<h4 style='margin:0; color: {colors['text']}'>₹{reno_min:,} - ₹{reno_max:,}</h4>", unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown("### 📝 AI-Generated Summary")
                    st.info(summary_text)
                else:
                    st.warning("Inspection summary not available.")
            
            with tab2:
                findings_result = get_property_findings(property_id)
                if findings_result and findings_result.get('data'):
                    st.markdown("### 🔍 Detailed Findings")
                    findings_by_room = {}
                    for row in findings_result['data']:
                        room, defect_type, severity, description, source = row
                        if room not in findings_by_room:
                            findings_by_room[room] = []
                        findings_by_room[room].append({'defect': defect_type, 'severity': severity, 'description': description, 'source': source})
                    for room, findings in findings_by_room.items():
                        with st.expander(f"📍 {room} ({len(findings)} issues)", expanded=True):
                            for finding in findings:
                                severity = finding['severity']
                                if severity >= 8:
                                    st.error(f"**{finding['defect'].title()}** (Severity: {severity}/10)")
                                elif severity >= 5:
                                    st.warning(f"**{finding['defect'].title()}** (Severity: {severity}/10)")
                                else:
                                    st.info(f"**{finding['defect'].title()}** (Severity: {severity}/10)")
                                st.caption(f"📝 {finding['description']}")
                                st.caption(f"🔍 Source: {finding['source']}")
                                st.markdown("---")
                else:
                    st.success("✅ No defects found in this property!")
            
            with tab3:
                improvements_result = get_property_improvements(property_id)
                if improvements_result and improvements_result.get('data'):
                    st.markdown("### 🔧 Recommended Improvements")
                    for row in improvements_result['data']:
                        defect_type, action, cost_range, priority, aff_rooms = row
            
                        # Priority colors
                        priority_colors = {
                'Critical': '#FF6B6B',
                'High': '#FFB020',
                'Medium': '#FFC107',
                'Low': '#00D9A5'
                        }
                        border_color = priority_colors.get(priority, '#666')
            
                        # Create improvement card with proper border
                        st.markdown(f"""
                        <div style="
                border-left: 5px solid {border_color};
                padding: 1.5rem;
                padding-left: 2rem;
                margin: 1rem 0;
                background: {colors['card_bg']};
                border-radius: 0 12px 12px 0;
            ">
                <h4 style="color: {colors['text']}; margin: 0 0 0.5rem 0;">
                    {defect_type.title()} - {priority} Priority
                </h4>
                <p style="color: {colors['text']}; margin: 0.5rem 0;">
                    ✓ {action}
                </p>
                <p style="color: {colors['text_secondary']}; font-size: 0.9rem; margin: 0.5rem 0;">
                    📍 Affected: {aff_rooms}
                </p>
                <p style="color: {colors['primary']}; font-weight: bold; margin: 0.5rem 0 0 0;">
                    {cost_range}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
                    st.markdown("---")
                    st.metric("💰 Renovation Budget", f"₹{reno_min:,} - ₹{reno_max:,}")
                else:
                    st.success("✅ No improvements needed!")
            
            with tab4:
                st.markdown("### 📸 Property Gallery")
                gallery_result = get_property_gallery(property_id)
                if gallery_result and gallery_result.get('data') and len(gallery_result['data']) > 0:
                    images = gallery_result['data']
                    st.success(f"📷 {len(images)} photo(s) available")
                    for i in range(0, len(images), 3):
                        cols = st.columns(3)
                        for j, col in enumerate(cols):
                            if i + j < len(images):
                                gallery_id, img_name, img_data, uploaded_at, img_order = images[i + j]
                                with col:
                                    try:
                                        img_bytes = base64.b64decode(img_data)
                                        st.image(img_bytes, caption=img_name, use_container_width=True)
                                        st.caption(f"📅 {uploaded_at.strftime('%Y-%m-%d')}")
                                    except Exception as e:
                                        st.error(f"❌ Failed to load image")
                else:
                    st.info("📭 No photos available for this property.")
                    st.markdown("**Why?** The seller hasn't uploaded photos yet.")
                    st.markdown('<div style="text-align:center;padding:3rem;background:#f0f2f6;border-radius:10px;margin:2rem 0;"><h1 style="font-size:4rem">🏠</h1><p style="color:#666">No photos uploaded yet</p></div>', unsafe_allow_html=True)
            
            with tab5:
                st.markdown("### 🏠 Property Details")
                st.markdown("**Description:**")
                st.write(description)
                st.markdown("**Nearby Landmarks:**")
                st.write(landmarks)
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Property Specifications:**")
                    st.write(f"• Type: {prop_type}")
                    st.write(f"• Bedrooms: {bedrooms}")
                    st.write(f"• Bathrooms: {bathrooms}")
                    st.write(f"• Area: {sqft} sq ft")
                with col2:
                    st.markdown("**Inspection Info:**")
                    st.write(f"• Listed: {created_at.strftime('%Y-%m-%d')}")
                    st.write(f"• Inspected: {inspected_at.strftime('%Y-%m-%d')}")
                    st.write(f"• Property ID: {prop_id}")
                    st.write(f"• Seller: {seller_name}")

else:
    st.subheader("🏘️ Available Properties")
    with st.spinner("Loading properties..."):
        result = get_inspected_properties()
        if result and result.get('data'):
            st.success(f"Found {len(result['data'])} inspected properties")
            filtered_data = result['data']
            if apply_filters:
                filtered_data = [row for row in filtered_data if row[8] in risk_filter and row[7] >= min_price and row[7] <= max_price and row[3] in prop_types and (not city_filter or city_filter.lower() in row[2].lower())]
                st.info(f"Filtered to {len(filtered_data)} properties")
            for row in filtered_data:
                (prop_id, address, city, prop_type, bedrooms, bathrooms, sqft, price, risk_score, risk_level, reno_min, reno_max, landmarks) = row
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.subheader(address)
                        st.write(f"📍 {city} | {prop_type} | {bedrooms}BHK | {sqft} sq ft")
                        st.caption(f"🗺️ Nearby: {landmarks[:100]}...")
                    with col2:
                        st.metric("💰 Price", f"₹{price:,}")
                        st.metric("📊 Risk Score", f"{risk_score}")
                        if reno_min and reno_max:
                            st.caption(f"🔧 Renovation: ₹{reno_min:,} - ₹{reno_max:,}")
                    with col3:
                        risk_class = f"risk-{risk_level.lower()}"
                        st.markdown(f'<div class="{risk_class}" style="text-align:center;margin-bottom:1rem">{risk_level} Risk</div>', unsafe_allow_html=True)
                        if st.button("🔍 View Details", key=f"view_{prop_id}", use_container_width=True):
                            st.session_state.selected_property_id = prop_id
                            st.rerun()
                    st.markdown("---")
        else:
            st.info("📭 No inspected properties available yet. Check back soon!")

st.markdown("---")
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")