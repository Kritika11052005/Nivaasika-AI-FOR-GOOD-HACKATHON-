import google.generativeai as genai
import os
import json
from PIL import Image
import io
import streamlit as st
from utils.rate_limiter import gemini_rate_limiter
import traceback

# Configure Gemini API
def get_gemini_api_key():
    """Get Gemini API key from Streamlit secrets"""
    try:
        if 'GEMINI_API_KEY' in st.secrets:
            return st.secrets['GEMINI_API_KEY']
        else:
            st.error("❌ GEMINI_API_KEY not found in .streamlit/secrets.toml")
            return None
    except Exception as e:
        st.error(f"❌ Failed to load API key: {str(e)}")
        return None

# Get API key and configure
api_key = get_gemini_api_key()

if api_key:
    try:
        genai.configure(api_key=api_key)
        st.success("✅ Gemini API configured successfully")
    except Exception as e:
        st.error(f"❌ Failed to configure Gemini: {str(e)}")

# Flag to enable/disable mock mode
USE_MOCK_MODE = False  # Set to True to use mock data instead of API

def analyze_property_image(image_file, room_name):
    """
    Analyze a property image using Gemini Vision API with rate limiting
    Returns: List of defects found
    """
    
    # Check if mock mode is enabled
    if USE_MOCK_MODE:
        st.write("🔍 Debug: Mock mode is ON")
        return _get_mock_defects(room_name)
    
    if not api_key:
        st.error("❌ Gemini API key not configured!")
        return _get_mock_defects(room_name)
    
    st.write("🔍 Debug: Starting API call...")
    
    try:
        # Check rate limit before making request
        remaining = gemini_rate_limiter.get_remaining_requests()
        
        if remaining <= 0:
            st.warning("⏳ Rate limit reached. Waiting for reset...")
            gemini_rate_limiter.wait_if_needed()
        else:
            st.info(f"ℹ️ API requests remaining: {remaining}")
        
        # Load image
        st.write("🔍 Debug: Loading image...")
        image = Image.open(image_file)
        st.write(f"🔍 Debug: Image loaded: {image.size}")
        
        # Create prompt for Gemini
        prompt = f"""
You are an expert property inspector analyzing a {room_name} image.

Identify ALL defects, issues, or concerns visible in this image.

For EACH defect found, provide:
1. defect_type: One of [crack, damp, wiring, leak, structural, finishing]
2. severity: Rate from 1-10 (1=minor, 10=critical)
3. description: Brief description of the issue

Return ONLY valid JSON in this exact format:
{{
    "defects": [
        {{
            "defect_type": "crack",
            "severity": 7,
            "description": "Large vertical crack on wall near ceiling"
        }}
    ]
}}

If NO defects found, return: {{"defects": []}}

Be thorough and detailed. Look for:
- Cracks in walls, ceiling, floor
- Water damage, damp patches, stains
- Exposed or damaged wiring
- Leaks or water seepage
- Structural issues
- Poor finishing or paint issues
"""
        
        # Record API request
        gemini_rate_limiter.record_request()
        
        st.info("🤖 Sending image to Gemini AI for analysis...")
        st.write("🔍 Debug: About to call API...")
        
        # Use the gemini-2.0-flash model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = model.generate_content([prompt, image])
        
        st.write("🔍 Debug: API call successful!")
        st.success("✅ AI analysis complete!")
        
        # Parse response
        response_text = response.text.strip()
        st.write(f"🔍 Debug: Response preview: {response_text[:200]}...")
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1]
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
        if response_text.endswith('```'):
            response_text = response_text.rsplit('```', 1)[0]
        
        response_text = response_text.strip()
        
        # Parse JSON
        result = json.loads(response_text)
        
        defects = result.get('defects', [])
        
        if defects:
            st.info(f"🔍 Found {len(defects)} defect(s) in {room_name}")
        else:
            st.success(f"✅ No defects found in {room_name}")
        
        return defects
        
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON parsing error: {e}")
        st.error(f"Response was: {response_text[:200]}...")
        return []
    except Exception as e:
        error_msg = str(e)
        
        # ADD DETAILED ERROR INFO
        st.error(f"❌ API Error: {error_msg}")
        st.error(f"Error type: {type(e).__name__}")
        st.write(f"🔍 Debug: Full error: {repr(e)}")
        
        # Print the full traceback
        st.code(traceback.format_exc())
        
        # Check for quota errors
        if '429' in error_msg or 'quota' in error_msg.lower():
            st.error("🚫 Gemini API quota exceeded!")
            st.warning("💡 Switching to mock mode for demo...")
            return _get_mock_defects(room_name)
        
        st.warning("⚠️ Falling back to mock data...")
        return _get_mock_defects(room_name)

def parse_inspector_notes(notes_text, room_name):
    """
    Parse inspector's text notes using Gemini with rate limiting
    Returns: List of defects mentioned in notes
    """
    if not notes_text or notes_text.strip() == "":
        return []
    
    # Check if mock mode
    if USE_MOCK_MODE:
        return []
    
    if not api_key:
        return []
    
    try:
        # Check rate limit
        if gemini_rate_limiter.get_remaining_requests() <= 0:
            gemini_rate_limiter.wait_if_needed()
        
        prompt = f"""
You are analyzing inspector notes for a {room_name}.

Inspector's notes: "{notes_text}"

Extract defects mentioned and classify them.

For EACH defect, provide:
1. defect_type: One of [crack, damp, wiring, leak, structural, finishing]
2. severity: Estimate from 1-10 based on description
3. description: The defect description from notes

Return ONLY valid JSON:
{{
    "defects": [
        {{
            "defect_type": "crack",
            "severity": 5,
            "description": "Minor crack on wall"
        }}
    ]
}}

If no defects mentioned, return: {{"defects": []}}
"""
        
        # Record request
        gemini_rate_limiter.record_request()
        
        st.info("🤖 Analyzing inspector notes with AI...")
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        
        # Clean response
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1]
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
        if response_text.endswith('```'):
            response_text = response_text.rsplit('```', 1)[0]
        
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        defects = result.get('defects', [])
        
        if defects:
            st.success(f"✅ Extracted {len(defects)} defect(s) from notes")
        
        return defects
        
    except Exception as e:
        st.warning(f"⚠️ Could not parse notes with AI: {str(e)}")
        st.write(f"🔍 Debug: Full error: {repr(e)}")
        st.code(traceback.format_exc())
        return []

def generate_inspection_summary(property_data, findings):
    """
    Generate plain-language inspection summary using Gemini with rate limiting
    """
    
    # Check if mock mode
    if USE_MOCK_MODE:
        return _get_mock_summary(property_data, findings)
    
    if not api_key:
        return _get_mock_summary(property_data, findings)
    
    try:
        # Check rate limit
        if gemini_rate_limiter.get_remaining_requests() <= 0:
            gemini_rate_limiter.wait_if_needed()
        
        findings_text = "\n".join([
            f"- {f['room_name']}: {f['defect_type']} (severity {f['severity']}) - {f['description']}"
            for f in findings
        ])
        
        prompt = f"""
Generate a concise, plain-language property inspection summary for home buyers.

Property: {property_data['address']}
Total defects found: {len(findings)}
Risk score: {property_data.get('risk_score', 'N/A')}

Findings:
{findings_text}

Write a 3-4 sentence summary that:
1. States overall property condition
2. Highlights critical issues (if any)
3. Mentions affected rooms
4. Gives honest assessment for buyers

Be professional, clear, and honest. Don't sugarcoat serious issues.
"""
        
        # Record request
        gemini_rate_limiter.record_request()
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return response.text.strip()
        
    except Exception as e:
        st.warning("⚠️ Using fallback summary generation")
        st.write(f"🔍 Debug: Full error: {repr(e)}")
        st.code(traceback.format_exc())
        return _get_mock_summary(property_data, findings)

# Mock data functions for when API is unavailable
def _get_mock_defects(room_name):
    """Return mock defects for demo purposes"""
    mock_defects = {
        'Kitchen': [
            {'defect_type': 'damp', 'severity': 6, 'description': 'Water stains visible near sink area'},
            {'defect_type': 'finishing', 'severity': 3, 'description': 'Minor paint peeling on ceiling'}
        ],
        'Bathroom 1': [
            {'defect_type': 'leak', 'severity': 7, 'description': 'Active water seepage from ceiling'},
            {'defect_type': 'damp', 'severity': 5, 'description': 'Mold growth in corner'}
        ],
        'Bathroom 2': [
            {'defect_type': 'wiring', 'severity': 8, 'description': 'Exposed wiring near shower area - safety hazard'}
        ],
        'Living Room': [
            {'defect_type': 'crack', 'severity': 4, 'description': 'Hairline crack on wall near window'}
        ],
        'Master Bedroom': [
            {'defect_type': 'finishing', 'severity': 2, 'description': 'Minor cosmetic issues'}
        ],
        'Bedroom 2': [
            {'defect_type': 'crack', 'severity': 3, 'description': 'Small crack near door frame'}
        ],
        'Bedroom 3': [
            {'defect_type': 'finishing', 'severity': 2, 'description': 'Paint touch-up needed'}
        ],
        'Balcony': [
            {'defect_type': 'structural', 'severity': 5, 'description': 'Minor weathering on railing'}
        ],
        'Other': [
            {'defect_type': 'finishing', 'severity': 2, 'description': 'General wear and tear'}
        ]
    }
    
    return mock_defects.get(room_name, [])

def _get_mock_summary(property_data, findings):
    """Generate mock summary"""
    risk_score = property_data.get('risk_score', 0)
    
    if risk_score < 20:
        return f"The property at {property_data['address']} is in good overall condition with minor cosmetic issues. {len(findings)} defects were identified, primarily low-severity items that can be addressed with routine maintenance. This property represents a safe purchase with minimal renovation requirements."
    elif risk_score < 50:
        return f"The property at {property_data['address']} shows moderate wear and requires attention in several areas. {len(findings)} defects were found, including some plumbing and electrical concerns. While habitable, buyers should budget for necessary repairs estimated between the provided cost ranges. Professional contractors should assess critical items before purchase."
    else:
        return f"The property at {property_data['address']} has significant issues requiring immediate attention. {len(findings)} defects were identified, including critical structural, electrical, or water damage concerns. Substantial renovation is needed before the property is safe for occupancy. Buyers should proceed with caution and obtain detailed contractor assessments."