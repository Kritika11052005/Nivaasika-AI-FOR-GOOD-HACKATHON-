import streamlit as st
from utils.database import get_snowflake_connection
from utils.theme import init_theme, toggle_theme, apply_theme_styles
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Nivaasika - Your Trusted Platform to Buy and Sell Property",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme
init_theme()

# Apply theme styles
apply_theme_styles()

# Theme toggle button in top right
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, key="theme_toggle", help="Toggle theme"):
        toggle_theme()
        st.rerun()

# Main content with animations
st.markdown('<div class="main-header">🏠 Nivaasika</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Property Inspection Platform</div>', unsafe_allow_html=True)

# Connection test with animation
with st.spinner("🔄 Connecting to database..."):
    conn = get_snowflake_connection()
    if conn:
        st.success("Connected to Snowflake successfully!")
        
        # Trigger confetti effect
        if 'confetti_shown' not in st.session_state:
            st.session_state.confetti_shown = True
            st.balloons()
    else:
        st.error("Failed to connect. Please check configuration.")

st.markdown("---")

# Introduction with fade-in effect
st.markdown("""
<div style="animation: fadeIn 1s ease-out;">
    <h3 style="text-align: center; margin-bottom: 2rem;">Welcome to Nivaasika! 🏡</h3>
    <p style="text-align: center; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
        Nivaasika is an intelligent property inspection platform that helps buyers make informed decisions 
        by providing AI-powered defect detection and risk assessment for residential properties.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Feature boxes with staggered animation
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box" style="animation-delay: 0.1s;">
        <div class="feature-title">🏪 For Sellers</div>
        <div class="feature-desc">
            List your property with complete details. Get professional AI-powered 
            inspection before listing to buyers. Build trust and sell faster.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box" style="animation-delay: 0.2s;">
        <div class="feature-title">🔍 For Inspectors</div>
        <div class="feature-desc">
            Conduct efficient inspections with AI assistance. Upload images and 
            notes. Generate comprehensive reports automatically.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box" style="animation-delay: 0.3s;">
        <div class="feature-title">🏠 For Buyers</div>
        <div class="feature-desc">
            Browse properties with complete transparency. View AI-generated risk 
            assessments and make confident purchase decisions.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Features section
st.markdown("### 🌟 Key Features")

features = [
    ("🤖", "AI-Powered Detection", "Gemini Vision API analyzes property images"),
    ("📊", "Risk Assessment", "Comprehensive scoring based on defects"),
    ("💰", "Cost Estimation", "Renovation cost estimates for all issues"),
    ("📝", "Detailed Reports", "AI-generated plain-language summaries"),
    ("🔒", "Full Transparency", "Complete visibility into property conditions"),
    ("🎯", "Smart Recommendations", "Prioritized improvement suggestions")
]

col1, col2 = st.columns(2)

for i, (icon, title, desc) in enumerate(features):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div style="animation: slideUp 0.5s ease-out; animation-delay: {i * 0.1}s; animation-fill-mode: both;">
            {icon} <strong>{title}</strong> - {desc}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Call-to-action buttons
st.markdown("### 👥 Select Your Role to Get Started")

role_col1, role_col2, role_col3 = st.columns(3)

with role_col1:
    if st.button("🏪 I'm a Seller", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Seller_Dashboard.py")

with role_col2:
    if st.button("🔍 I'm an Inspector", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Inspector_Dashboard.py")

with role_col3:
    if st.button("🏠 I'm a Buyer", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Buyer_Dashboard.py")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; padding: 3rem 0; animation: fadeIn 2s ease-out;">
    <h3 style="background: linear-gradient(135deg, #FF6B35, #004E89); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Nivaasika
    </h3>
    <p style="font-size: 1.1rem; margin: 1rem 0;">Making Property Purchases Transparent & Safe</p>
    <p style="opacity: 0.7;">AI for Good Hackathon 2025 | Powered by Snowflake & Gemini AI</p>
    <p> Made by Kritika Benjwal</p>
</div>
""", unsafe_allow_html=True)