import streamlit as st

def init_theme():
    """Initialize theme in session state"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

def toggle_theme():
    """Toggle between light and dark theme"""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

def get_theme_colors():
    """Get color scheme based on current theme"""
    if st.session_state.theme == 'dark':
        return {
            'primary': '#FF6B35',
            'secondary': '#4ECDC4',
            'background': '#0E1117',
            'surface': '#262730',
            'text': '#FAFAFA',
            'text_secondary': '#B8B8B8',
            'success': '#00D9A5',
            'warning': '#FFB020',
            'error': '#FF6B6B',
            'card_bg': '#1E1E1E',
            'card_hover': '#33343F',
            'gradient_start': '#FF6B35',
            'gradient_end': '#4ECDC4',
            'border': '#404040',
            'input_bg': '#262730',
            'input_text': '#FAFAFA'
        }
    else:
        return {
            'primary': '#FF6B35',
            'secondary': '#4ECDC4',
            'background': '#FFFFFF',
            'surface': '#F8F9FA',
            'text': '#1A1A1A',
            'text_secondary': '#6C757D',
            'success': '#28A745',
            'warning': '#FFC107',
            'error': '#DC3545',
            'card_bg': '#FFFFFF',
            'card_hover': '#F0F2F6',
            'gradient_start': '#FF6B35',
            'gradient_end': '#4ECDC4',
            'border': '#DEE2E6',
            'input_bg': '#FFFFFF',
            'input_text': '#1A1A1A'
        }

def apply_theme_styles():
    """Apply CSS styles based on current theme"""
    colors = get_theme_colors()
    
    # Different background animation for dark vs light
    if st.session_state.theme == 'dark':
        bg_animation = f"""
        background: linear-gradient(-45deg, #0E1117, #1A1B26, #0E1117, #1A1B26);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        """
    else:
        bg_animation = f"""
        background: linear-gradient(-45deg, #FFFFFF, #F8F9FA, #FFFFFF, #F0F2F6);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        """
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* ===== GLOBAL RESETS ===== */
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        .main {{
            background: {colors['background']} !important;
            color: {colors['text']} !important;
        }}
        
        .stApp {{
            {bg_animation}
        }}
        
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* ===== AGGRESSIVE INPUT FIXES ===== */
        
        /* ALL inputs - nuclear option */
        input,
        textarea,
        select,
        [data-baseweb="input"] input,
        [data-baseweb="base-input"] input,
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox select,
        div[data-baseweb="select"] input {{
            background-color: {colors['input_bg']} !important;
            background: {colors['input_bg']} !important;
            color: {colors['input_text']} !important;
            border: 2px solid {colors['border']} !important;
            border-radius: 8px !important;
        }}
        
        /* ===== FILE UPLOADER FIX ===== */
        [data-testid="stFileUploader"],
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploadDropzone"],
        [data-testid="stFileUploader"] > div,
        section[data-testid="stFileUploadDropzone"] {{
            background-color: {colors['input_bg']} !important;
            background: {colors['input_bg']} !important;
            border: 2px dashed {colors['border']} !important;
            border-radius: 12px !important;
        }}
        
        /* File uploader text and labels */
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploadDropzone"] span,
        [data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] p {{
            color: {colors['text']} !important;
        }}
        
        /* File uploader buttons */
        [data-testid="stFileUploader"] button,
        [data-testid="stFileUploadDropzone"] button {{
            background-color: {colors['surface']} !important;
            background: {colors['surface']} !important;
            color: {colors['text']} !important;
            border: 2px solid {colors['border']} !important;
        }}
        
        [data-testid="stFileUploader"] button:hover,
        [data-testid="stFileUploadDropzone"] button:hover {{
            background-color: {colors['primary']} !important;
            color: white !important;
            border-color: {colors['primary']} !important;
        }}
        
        /* Input containers */
        [data-baseweb="input"],
        [data-baseweb="base-input"],
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stTextArea > div > div,
        .stTextArea > div {{
            background-color: {colors['input_bg']} !important;
            background: {colors['input_bg']} !important;
        }}
        
        /* Textarea specific - more aggressive */
        .stTextArea textarea,
        textarea[aria-label*="notes"],
        textarea[placeholder*="observations"] {{
            background-color: {colors['input_bg']} !important;
            background: {colors['input_bg']} !important;
            color: {colors['input_text']} !important;
            border: 2px solid {colors['border']} !important;
            border-radius: 8px !important;
        }}
        
        /* Number input buttons - CRITICAL FIX */
        .stNumberInput button,
        button[kind="tertiary"],
        button[data-testid="stNumberInput-StepUp"],
        button[data-testid="stNumberInput-StepDown"],
        [data-baseweb="input"] button {{
            background-color: {colors['surface']} !important;
            background: {colors['surface']} !important;
            color: {colors['text']} !important;
            border: 2px solid {colors['border']} !important;
            border-radius: 6px !important;
            min-width: 36px !important;
            min-height: 36px !important;
        }}
        
        .stNumberInput button:hover,
        button[kind="tertiary"]:hover {{
            background-color: {colors['primary']} !important;
            background: {colors['primary']} !important;
            color: white !important;
            border-color: {colors['primary']} !important;
        }}
        
        /* Button SVG icons */
        .stNumberInput button svg,
        button[kind="tertiary"] svg {{
            fill: {colors['text']} !important;
        }}
        
        .stNumberInput button:hover svg {{
            fill: white !important;
        }}
        
        /* Multiselect - FIXED */
        .stMultiSelect > div > div,
        [data-baseweb="select"] {{
            background-color: {colors['input_bg']} !important;
            background: {colors['input_bg']} !important;
            border: 2px solid {colors['border']} !important;
            border-radius: 10px !important;
        }}
        
        .stMultiSelect [data-baseweb="tag"] {{
            background: linear-gradient(135deg, {colors['gradient_start']}, {colors['gradient_end']}) !important;
            color: white !important;
            border: none !important;
        }}
        
        .stMultiSelect [data-baseweb="tag"] span,
        .stMultiSelect [data-baseweb="tag"] button {{
            color: white !important;
        }}
        
        /* Selectbox */
        .stSelectbox > div > div,
        [data-baseweb="select"] > div {{
            background-color: {colors['input_bg']} !important;
            background: {colors['input_bg']} !important;
            color: {colors['text']} !important;
            border: 2px solid {colors['border']} !important;
        }}
        
        /* Dropdown menus */
        [data-baseweb="popover"],
        [role="listbox"] {{
            background-color: {colors['surface']} !important;
            background: {colors['surface']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        [role="option"] {{
            background-color: {colors['surface']} !important;
            background: {colors['surface']} !important;
            color: {colors['text']} !important;
        }}
        
        [role="option"]:hover {{
            background-color: {colors['card_hover']} !important;
            background: {colors['card_hover']} !important;
        }}
        
        /* Placeholder text */
        input::placeholder,
        textarea::placeholder {{
            color: {colors['text_secondary']} !important;
            opacity: 0.7 !important;
        }}
        
        /* Labels */
        .stTextInput label,
        .stTextArea label,
        .stNumberInput label,
        .stSelectbox label,
        .stMultiSelect label,
        .stFileUploader label,
        label {{
            color: {colors['text']} !important;
            font-weight: 600 !important;
        }}
        
        /* ===== STREAMLIT EXPANDER FIX - MAXIMUM SPECIFICITY ===== */
        /* Force on ALL details elements in the app */
        div[data-testid="stExpander"] details,
        div[data-testid="stExpander"] details summary,
        div[data-testid="stExpander"] details[open] summary,
        .main div[data-testid="stExpander"] details summary,
        section.main div[data-testid="stExpander"] details summary {{
            background-color: {colors['surface']} !important;
            background: {colors['surface']} !important;
            color: {colors['text']} !important;
            border-color: {colors['border']} !important;
        }}
        
        /* Force background on wrapper divs */
        div[data-testid="stExpander"] details > div,
        div[data-testid="stExpander"] > div {{
            background-color: {colors['surface']} !important;
        }}
        
        /* All text content */
        div[data-testid="stExpander"] details summary p,
        div[data-testid="stExpander"] details summary span,
        div[data-testid="stExpander"] details summary div,
        div[data-testid="stExpander"] details summary * {{
            color: {colors['text']} !important;
            background-color: transparent !important;
        }}
        
        /* SVG icons */
        div[data-testid="stExpander"] details summary svg,
        div[data-testid="stExpander"] svg {{
            fill: {colors['text']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Expander content area */
        [data-testid="stExpander"] > div,
        .streamlit-expanderContent,
        details[open] {{
            background-color: {colors['background']} !important;
        }}
        
        /* All elements inside expanders */
        [data-testid="stExpander"] *,
        .streamlit-expanderContent *,
        details * {{
            color: {colors['text']} !important;
        }}
        
        /* File uploaders inside expanders */
        [data-testid="stExpander"] [data-testid="stFileUploader"],
        [data-testid="stExpander"] [data-testid="stFileUploader"] section,
        [data-testid="stExpander"] [data-testid="stFileUploadDropzone"],
        details [data-testid="stFileUploader"],
        details [data-testid="stFileUploadDropzone"] {{
            background-color: {colors['input_bg']} !important;
            border: 2px dashed {colors['border']} !important;
        }}
        
        /* Textareas inside expanders */
        [data-testid="stExpander"] textarea,
        details textarea {{
            background-color: {colors['input_bg']} !important;
            color: {colors['input_text']} !important;
            border: 2px solid {colors['border']} !important;
        }}
        
        /* ===== HEADERS ===== */
        .main-header {{
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, {colors['gradient_start']}, {colors['gradient_end']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 1rem;
            animation: fadeInDown 0.8s ease-out;
        }}
        
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .sub-header {{
            font-size: 1.4rem;
            text-align: center;
            color: {colors['text_secondary']};
            margin-bottom: 2rem;
            animation: fadeIn 1s ease-out 0.3s both;
            font-weight: 500;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        /* ===== FEATURE BOXES ===== */
        .feature-box {{
            background: {colors['card_bg']};
            padding: 2rem;
            border-radius: 20px;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            animation: slideUp 0.6s ease-out;
            border: 1px solid {colors['border']};
            position: relative;
            overflow: hidden;
        }}
        
        .feature-box::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, {colors['gradient_start']}, {colors['gradient_end']});
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }}
        
        .feature-box:hover::before {{
            transform: scaleX(1);
        }}
        
        .feature-box:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(255, 107, 53, 0.2);
            border-color: {colors['primary']};
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .feature-title {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {colors['primary']};
            margin-bottom: 1rem;
        }}
        
        .feature-desc {{
            color: {colors['text']};
            line-height: 1.8;
            font-size: 1rem;
        }}
        
        /* ===== RISK BADGES ===== */
        .risk-low {{
            background: linear-gradient(135deg, #00D9A5, #00B386);
            color: white !important;
            padding: 0.6rem 1.5rem;
            border-radius: 30px;
            font-weight: 700;
            font-size: 0.95rem;
            box-shadow: 0 4px 15px rgba(0, 217, 165, 0.3);
            display: inline-block;
        }}
        
        .risk-medium {{
            background: linear-gradient(135deg, #FFB020, #FF8C00);
            color: white !important;
            padding: 0.6rem 1.5rem;
            border-radius: 30px;
            font-weight: 700;
            font-size: 0.95rem;
            box-shadow: 0 4px 15px rgba(255, 176, 32, 0.3);
            display: inline-block;
        }}
        
        .risk-high {{
            background: linear-gradient(135deg, #FF6B6B, #EE5A52);
            color: white !important;
            padding: 0.6rem 1.5rem;
            border-radius: 30px;
            font-weight: 700;
            font-size: 0.95rem;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
            display: inline-block;
        }}
        
        /* ===== BUTTONS ===== */
        .stButton > button {{
            background: linear-gradient(135deg, {colors['gradient_start']}, {colors['gradient_end']}) !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 1rem 2.5rem !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 8px 20px rgba(255, 107, 53, 0.3) !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 28px rgba(255, 107, 53, 0.4) !important;
        }}
        
        /* ===== SIDEBAR ===== */
        [data-testid="stSidebar"] {{
            background: {colors['surface']} !important;
            border-right: 1px solid {colors['border']};
        }}
        
        [data-testid="stSidebar"] * {{
            color: {colors['text']} !important;
        }}
        
        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: transparent !important;
            border-bottom: 2px solid {colors['border']} !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: {colors['surface']} !important;
            color: {colors['text']} !important;
            border: 2px solid {colors['border']} !important;
            border-bottom: none !important;
            border-radius: 12px 12px 0 0 !important;
            padding: 14px 28px !important;
            font-weight: 600 !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {colors['gradient_start']}, {colors['gradient_end']}) !important;
            color: white !important;
            border-color: transparent !important;
        }}
        
        /* ===== DATAFRAMES / TABLES ===== */
        /* Dataframe container */
        [data-testid="stDataFrame"],
        .stDataFrame,
        div[data-testid="stDataFrame"] > div {{
            background-color: {colors['card_bg']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Table elements */
        [data-testid="stDataFrame"] table,
        .stDataFrame table,
        table {{
            background-color: {colors['card_bg']} !important;
            color: {colors['text']} !important;
            border-color: {colors['border']} !important;
        }}
        
        /* Table headers */
        [data-testid="stDataFrame"] thead,
        [data-testid="stDataFrame"] th,
        .stDataFrame thead,
        .stDataFrame th,
        table thead,
        table th {{
            background-color: {colors['surface']} !important;
            color: {colors['text']} !important;
            border-color: {colors['border']} !important;
            font-weight: 700 !important;
        }}
        
        /* Table body */
        [data-testid="stDataFrame"] tbody,
        [data-testid="stDataFrame"] td,
        .stDataFrame tbody,
        .stDataFrame td,
        table tbody,
        table td {{
            background-color: {colors['card_bg']} !important;
            color: {colors['text']} !important;
            border-color: {colors['border']} !important;
        }}
        
        /* Table rows - alternate colors */
        [data-testid="stDataFrame"] tbody tr:nth-child(even),
        .stDataFrame tbody tr:nth-child(even),
        table tbody tr:nth-child(even) {{
            background-color: {colors['surface']} !important;
        }}
        
        /* Table row hover */
        [data-testid="stDataFrame"] tbody tr:hover,
        .stDataFrame tbody tr:hover,
        table tbody tr:hover {{
            background-color: {colors['card_hover']} !important;
        }}
        
        /* All text inside tables */
        [data-testid="stDataFrame"] *,
        .stDataFrame *,
        table * {{
            color: {colors['text']} !important;
        }}
        
        /* Dataframe toolbar/controls */
        [data-testid="stDataFrame"] button,
        .stDataFrame button {{
            background-color: {colors['surface']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        [data-testid="stDataFrame"] button:hover,
        .stDataFrame button:hover {{
            background-color: {colors['card_hover']} !important;
        }}
        
        /* ===== METRICS ===== */
        [data-testid="stMetricValue"] {{
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            color: {colors['primary']} !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {colors['text']} !important;
            font-weight: 600 !important;
        }}
        
        /* ===== TEXT ELEMENTS ===== */
        p, span, div, label, h1, h2, h3, h4, h5, h6 {{
            color: {colors['text']} !important;
        }}
        
        /* ===== IMPROVEMENTS ===== */
        .improvement-critical,
        .improvement-high,
        .improvement-medium,
        .improvement-low {{
            padding: 1.5rem;
            margin: 1rem 0;
            background: {colors['card_bg']};
            border-radius: 12px;
            color: {colors['text']};
        }}
        
        .improvement-critical {{ border-left: 5px solid #FF6B6B; }}
        .improvement-high {{ border-left: 5px solid #FFB020; }}
        .improvement-medium {{ border-left: 5px solid #FFC107; }}
        .improvement-low {{ border-left: 5px solid #00D9A5; }}
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {{
            width: 12px;
            height: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {colors['surface']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, {colors['gradient_start']}, {colors['gradient_end']});
            border-radius: 10px;
        }}
        
        /* ===== EXPANDERS ===== */
        [data-testid="stExpander"],
        .streamlit-expanderHeader {{
            background: {colors['surface']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        /* Expander details element - this is the actual container */
        [data-testid="stExpander"] details,
        [data-testid="stExpander"] details summary,
        details[data-testid] {{
            background-color: {colors['surface']} !important;
            background: {colors['surface']} !important;
        }}
        
        /* All text inside expander headers */
        [data-testid="stExpander"] details summary *,
        [data-testid="stExpander"] summary * {{
            color: {colors['text']} !important;
        }}
        
        /* ===== ALERTS ===== */
        .stSuccess, .stWarning, .stError, .stInfo {{
            background: {colors['card_bg']} !important;
            color: {colors['text']} !important;
        }}
        
        /* ===== PROPERTY CARDS - DARK MODE FIX ===== */
        .property-card {{
            background-color: {colors['card_bg']} !important;
            border: 1px solid {colors['border']} !important;
            color: {colors['text']} !important;
        }}
        
        .property-card * {{
            color: {colors['text']} !important;
        }}
        
        .property-card h3 {{
            color: {colors['primary']} !important;
        }}
        
        .property-card strong {{
            color: {colors['text']} !important;
            font-weight: 700 !important;
        }}
    </style>
    """, unsafe_allow_html=True)