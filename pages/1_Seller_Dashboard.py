import streamlit as st
import uuid
from datetime import datetime
from utils.database import insert_property, execute_query
from utils.theme import init_theme, toggle_theme, apply_theme_styles
st.set_page_config(
    page_title="Seller Dashboard - Nivaasika",
    page_icon="🏪",
    layout="wide"
)
# Initialize and apply theme
init_theme()
apply_theme_styles()

# Theme toggle in top right
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, key="theme_toggle"):
        toggle_theme()
        st.rerun()
# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏪 Seller Dashboard</div>', unsafe_allow_html=True)
st.markdown("List your property for inspection and get it reviewed before it's visible to buyers.")

st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["📝 List New Property", "📋 My Properties"])

# Tab 1: List New Property
with tab1:
    st.subheader("Submit Property Details")
    
    with st.form("property_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            seller_name = st.text_input("Your Name *", placeholder="John Doe")
            seller_email = st.text_input("Your Email *", placeholder="john@example.com")
            property_address = st.text_area("Property Address *", placeholder="123 Main Street, Apartment 4B")
            city = st.text_input("City *", placeholder="Mumbai")
            state = st.text_input("State *", placeholder="Maharashtra")
            pincode = st.text_input("Pincode *", placeholder="400001")
        
        with col2:
            property_type = st.selectbox(
                "Property Type *",
                ["Apartment", "Independent House", "Villa", "Penthouse", "Studio Apartment"]
            )
            bedrooms = st.number_input("Bedrooms *", min_value=0, max_value=10, value=2)
            bathrooms = st.number_input("Bathrooms *", min_value=0, max_value=10, value=2)
            square_feet = st.number_input("Area (sq ft) *", min_value=100, max_value=50000, value=1000)
            price = st.number_input("Price (Rs) *", min_value=100000, max_value=1000000000, value=5000000, step=100000)
        
        description = st.text_area(
            "Property Description",
            placeholder="Describe your property... (e.g., Well-maintained 2BHK apartment with modern amenities)",
            height=100
        )
        
        nearby_landmarks = st.text_area(
            "Nearby Landmarks",
            placeholder="Enter nearby landmarks separated by commas (e.g., Metro Station 500m, School 1km, Hospital 2km)",
            height=80
        )
        
        st.markdown("**Note:** Properties marked with * are required fields.")
        
        submitted = st.form_submit_button("Submit Property for Inspection", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            if not all([seller_name, seller_email, property_address, city, state, pincode]):
                st.error("❌ Please fill all required fields!")
            elif '@' not in seller_email:
                st.error("❌ Please enter a valid email address!")
            else:
                # Generate property ID
                property_id = f"PROP_{uuid.uuid4().hex[:8].upper()}"
                
                # Prepare data
                property_data = {
                    'property_id': property_id,
                    'seller_name': seller_name,
                    'seller_email': seller_email,
                    'property_address': property_address,
                    'city': city,
                    'state': state,
                    'pincode': pincode,
                    'property_type': property_type,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'square_feet': square_feet,
                    'price': price,
                    'description': description if description else 'No description provided',
                    'nearby_landmarks': nearby_landmarks if nearby_landmarks else 'Not specified'
                }
                
                # Insert into database
                with st.spinner("Submitting property..."):
                    result = insert_property(property_data)
                    
                    if result and result.get('success'):
                        st.success("✅ Property submitted successfully!")
                        st.markdown(f"""
                        <div class="success-box">
                            <h4>Property ID: {property_id}</h4>
                            <p><strong>What's Next?</strong></p>
                            <ul>
                                <li>Your property is now <strong>pending inspection</strong></li>
                                <li>Our inspection team will review and inspect the property</li>
                                <li>Once inspected, it will be visible to buyers</li>
                                <li>You'll be notified via email at <strong>{seller_email}</strong></li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.balloons()
                    else:
                        st.error("❌ Failed to submit property. Please try again.")

# Tab 2: My Properties
with tab2:
    st.subheader("View Your Listed Properties")
    
    # Email input to fetch properties
    seller_email_lookup = st.text_input(
        "Enter your email to view your properties",
        placeholder="john@example.com"
    )
    
    if st.button("Fetch My Properties", type="primary"):
        if not seller_email_lookup or '@' not in seller_email_lookup:
            st.error("Please enter a valid email address!")
        else:
            with st.spinner("Fetching your properties..."):
                query = f"""
                SELECT property_id, property_address, city, property_type, 
                    price, status, created_at, risk_level
                FROM PROPERTIES 
                WHERE seller_email = '{seller_email_lookup}'
                ORDER BY created_at DESC
                """
                result = execute_query(query)
                
                if result and result.get('data'):
                    st.success(f"Found {len(result['data'])} properties")
                    
                    for row in result['data']:
                        prop_id, address, city, prop_type, price, status, created_at, risk_level = row
                        
                        with st.container():
                            col1, col2, col3 = st.columns([3, 2, 1])
                            
                            with col1:
                                st.markdown(f"**{address}**")
                                st.caption(f"📍 {city} | {prop_type} | ₹{price:,}")
                            
                            with col2:
                                if status == 'pending':
                                    st.warning(f"🕐 Status: Pending Inspection")
                                elif status == 'inspected':
                                    if risk_level == 'Low':
                                        st.success(f"✅ Status: Inspected | Risk: {risk_level}")
                                    elif risk_level == 'Medium':
                                        st.info(f"✅ Status: Inspected | Risk: {risk_level}")
                                    else:
                                        st.error(f"✅ Status: Inspected | Risk: {risk_level}")
                            
                            with col3:
                                st.caption(f"ID: {prop_id}")
                                st.caption(f"Listed: {created_at.strftime('%Y-%m-%d')}")
                            
                            st.markdown("---")
                else:
                    st.info("No properties found for this email address.")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    
    # Get total properties
    total_query = "SELECT COUNT(*) as total FROM PROPERTIES"
    total_result = execute_query(total_query)
    if total_result and total_result.get('data'):
        total_properties = total_result['data'][0][0]
        st.metric("Total Properties Listed", total_properties)
    
    # Get pending count
    pending_query = "SELECT COUNT(*) as pending FROM PROPERTIES WHERE status = 'pending'"
    pending_result = execute_query(pending_query)
    if pending_result and pending_result.get('data'):
        pending_count = pending_result['data'][0][0]
        st.metric("Pending Inspection", pending_count)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips for Sellers")
    st.info("""
    - Provide accurate property details
    - Be honest about property condition
    - Inspection helps build buyer trust
    - Properties with low risk sell faster
    """)

# Footer
st.markdown("---")
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")