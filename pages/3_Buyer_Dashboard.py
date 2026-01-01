import streamlit as st
from utils.database import (
    get_inspected_properties, get_property_details, 
    get_property_findings, get_property_improvements, 
    get_inspection_summary, execute_query
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
    
    # Risk level filter
    risk_filter = st.multiselect(
        "Risk Level",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"]
    )
    
    # Price range filter
    st.markdown("#### Price Range (₹)")
    min_price = st.number_input("Min Price", min_value=0, value=0, step=100000)
    max_price = st.number_input("Max Price", min_value=0, value=100000000, step=100000)
    
    # Property type filter
    prop_types = st.multiselect(
        "Property Type",
        ["Apartment", "Independent House", "Villa", "Penthouse", "Studio Apartment"],
        default=["Apartment", "Independent House", "Villa", "Penthouse", "Studio Apartment"]
    )
    
    # City filter
    city_filter = st.text_input("City", placeholder="e.g., Mumbai")
    
    apply_filters = st.button("Apply Filters", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Market Stats")
    
    total_query = "SELECT COUNT(*) FROM PROPERTIES WHERE status = 'inspected'"
    total_result = execute_query(total_query)
    if total_result and total_result.get('data'):
        total_inspected = total_result['data'][0][0]
        st.metric("Total Inspected Properties", total_inspected)
    
    low_risk_query = "SELECT COUNT(*) FROM PROPERTIES WHERE status = 'inspected' AND risk_level = 'Low'"
    low_risk_result = execute_query(low_risk_query)
    if low_risk_result and low_risk_result.get('data'):
        low_risk_count = low_risk_result['data'][0][0]
        st.metric("Low Risk Properties", low_risk_count)

# Main content
if st.session_state.selected_property_id:
    # Detailed property view
    property_id = st.session_state.selected_property_id
    
    if st.button("← Back to All Properties"):
        st.session_state.selected_property_id = None
        st.rerun()
    
    st.markdown("---")
    
    # Get property details
    with st.spinner("Loading property details..."):
        prop_result = get_property_details(property_id)
        
        if prop_result and prop_result.get('data'):
            prop_data = prop_result['data'][0]
            
            # Unpack property data
            (prop_id, seller_name, seller_email, address, city, state, pincode,
             prop_type, bedrooms, bathrooms, sqft, price, description, landmarks,
             status, created_at, inspected_at, risk_score, risk_level,
             reno_min, reno_max, affected_rooms, total_defects, critical_issues) = prop_data
            
            # Property header
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"## {address}")
                st.markdown(f"📍 {city}, {state} - {pincode}")
            
            with col2:
                risk_class = f"risk-{risk_level.lower()}"
                st.markdown(f'<div class="{risk_class}">Risk: {risk_level}</div>', unsafe_allow_html=True)
                st.markdown(f"**Risk Score:** {risk_score}")
            
            st.markdown("---")
            
            # Property details in columns
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
            
            # Tabs for detailed info
            tab1, tab2, tab3, tab4 = st.tabs([
                "📋 Inspection Summary", 
                "🔍 Defects Found", 
                "🔧 Improvements Needed",
                "ℹ️ Property Info"
            ])
            
            # Tab 1: Inspection Summary
            with tab1:
                summary_result = get_inspection_summary(property_id)
                
                if summary_result and summary_result.get('data'):
                    summary_data = summary_result['data'][0]
                    summary_text, tot_defects, crit_issues, aff_rooms = summary_data
                    
                    # Metrics
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
                        st.markdown(f"<h4 style='margin:0; color: {colors['text']}'>₹{reno_min:,}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style='margin:0; color: {colors['text']}'>to ₹{reno_max:,}</h4>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    st.markdown("### 📝 AI-Generated Summary")
                    st.info(summary_text)
                else:
                    st.warning("Inspection summary not available.")
            
            # Tab 2: Defects Found
            with tab2:
                findings_result = get_property_findings(property_id)
                
                if findings_result and findings_result.get('data'):
                    st.markdown("### 🔍 Detailed Findings")
                    
                    # Group by room
                    findings_by_room = {}
                    for row in findings_result['data']:
                        room, defect_type, severity, description, source = row
                        if room not in findings_by_room:
                            findings_by_room[room] = []
                        findings_by_room[room].append({
                            'defect': defect_type,
                            'severity': severity,
                            'description': description,
                            'source': source
                        })
                    
                    # Display by room
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
            
            # Tab 3: Improvements Needed
            with tab3:
                improvements_result = get_property_improvements(property_id)
                
                if improvements_result and improvements_result.get('data'):
                    st.markdown("### 🔧 Recommended Improvements")
                    
                    for row in improvements_result['data']:
                        defect_type, action, cost_range, priority, aff_rooms = row
                        
                        priority_class = f"improvement-{priority.lower()}"
                        
                        st.markdown(f'<div class="{priority_class}">', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**{defect_type.title()} - {priority} Priority**")
                            st.markdown(f"✓ {action}")
                            st.caption(f"📍 Affected: {aff_rooms}")
                        
                        with col2:
                            st.markdown(f"**{cost_range}**")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown("")
                    
                    st.markdown("---")
                    st.markdown(f"### 💰 Total Estimated Cost")
                    st.metric("Renovation Budget", f"₹{reno_min:,} - ₹{reno_max:,}")
                else:
                    st.success("✅ No improvements needed!")
            
            # Tab 4: Property Info
            with tab4:
                st.markdown("### 🏠 Property Details")
                
                st.markdown(f"**Description:**")
                st.write(description)
                
                st.markdown(f"**Nearby Landmarks:**")
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
    # Property listing view
    st.subheader("🏘️ Available Properties")
    
    with st.spinner("Loading properties..."):
        result = get_inspected_properties()
        
        if result and result.get('data'):
            st.success(f"Found {len(result['data'])} inspected properties")
            
            # Apply filters if button clicked
            filtered_data = result['data']
            
            if apply_filters:
                filtered_data = [
                    row for row in filtered_data
                    if row[8] in risk_filter  # risk_level
                    and row[7] >= min_price  # price
                    and row[7] <= max_price
                    and row[3] in prop_types  # property_type
                    and (not city_filter or city_filter.lower() in row[2].lower())  # city
                ]
                
                st.info(f"Filtered to {len(filtered_data)} properties")
            
            # Display properties - FIXED VERSION
            for row in filtered_data:
                (prop_id, address, city, prop_type, bedrooms, bathrooms, sqft, 
                price, risk_score, risk_level, reno_min, reno_max, landmarks) = row
                
                # Use Streamlit components directly - no custom CSS div
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
                        st.markdown(f'<div class="{risk_class}" style="text-align: center; margin-bottom: 1rem;">{risk_level} Risk</div>', unsafe_allow_html=True)
                        if st.button("🔍 View Details", key=f"view_{prop_id}", use_container_width=True):
                            st.session_state.selected_property_id = prop_id
                            st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("📭 No inspected properties available yet. Check back soon!")

# Footer
st.markdown("---")
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")