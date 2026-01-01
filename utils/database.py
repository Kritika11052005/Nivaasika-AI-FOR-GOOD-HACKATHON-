import streamlit as st
import snowflake.connector
import os

@st.cache_resource
def get_snowflake_connection():
    """Create and cache Snowflake connection"""
    try:
        # Try to get credentials from Streamlit secrets first (for cloud deployment)
        if hasattr(st, 'secrets') and 'snowflake' in st.secrets:
            conn = snowflake.connector.connect(
                account=st.secrets['snowflake']['account'],
                user=st.secrets['snowflake']['user'],
                password=st.secrets['snowflake']['password'],
                database=st.secrets['snowflake']['database'],
                schema=st.secrets['snowflake']['schema'],
                warehouse=st.secrets['snowflake']['warehouse'],
                role=st.secrets['snowflake']['role']
            )
        # Fall back to environment variables (for local development)
        else:
            from dotenv import load_dotenv
            load_dotenv()
            
            conn = snowflake.connector.connect(
                account=os.getenv('SNOWFLAKE_ACCOUNT'),
                user=os.getenv('SNOWFLAKE_USER'),
                password=os.getenv('SNOWFLAKE_PASSWORD'),
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                role=os.getenv('SNOWFLAKE_ROLE')
            )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None

def execute_query(query, params=None):
    """Execute a SQL query and return results"""
    conn = get_snowflake_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Check if it's a SELECT query
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return {'columns': columns, 'data': results}
        else:
            conn.commit()
            return {'success': True}
    except Exception as e:
        st.error(f"Query execution failed: {str(e)}")
        return None
    finally:
        cursor.close()

def insert_property(property_data):
    """Insert a new property into the database"""
    query = """
    INSERT INTO PROPERTIES (
        property_id, seller_name, seller_email, property_address, 
        city, state, pincode, property_type, bedrooms, bathrooms, 
        square_feet, price, description, nearby_landmarks, status
    ) VALUES (
        %(property_id)s, %(seller_name)s, %(seller_email)s, %(property_address)s,
        %(city)s, %(state)s, %(pincode)s, %(property_type)s, %(bedrooms)s, 
        %(bathrooms)s, %(square_feet)s, %(price)s, %(description)s, 
        %(nearby_landmarks)s, 'pending'
    )
    """
    return execute_query(query, property_data)

def get_pending_properties():
    """Get all properties with status='pending'"""
    query = "SELECT * FROM PROPERTIES WHERE status = 'pending' ORDER BY created_at DESC"
    return execute_query(query)

def get_inspected_properties():
    """Get all properties with status='inspected'"""
    query = """
    SELECT property_id, property_address, city, property_type, bedrooms, 
           bathrooms, square_feet, price, risk_score, risk_level, 
           total_renovation_cost_min, total_renovation_cost_max, nearby_landmarks
    FROM PROPERTIES 
    WHERE status = 'inspected' 
    ORDER BY inspected_at DESC
    """
    return execute_query(query)

def get_property_details(property_id):
    """Get detailed information about a specific property"""
    query = f"SELECT * FROM PROPERTIES WHERE property_id = '{property_id}'"
    return execute_query(query)

def get_property_findings(property_id):
    """Get all inspection findings for a property"""
    query = f"""
    SELECT room_name, defect_type, severity, description, source
    FROM INSPECTION_FINDINGS 
    WHERE property_id = '{property_id}'
    ORDER BY severity DESC
    """
    return execute_query(query)

def get_property_improvements(property_id):
    """Get improvement recommendations for a property"""
    query = f"""
    SELECT defect_type, improvement_action, estimated_cost_range, 
           priority, affected_rooms
    FROM PROPERTY_IMPROVEMENTS 
    WHERE property_id = '{property_id}'
    ORDER BY CASE priority 
        WHEN 'Critical' THEN 1 
        WHEN 'High' THEN 2 
        WHEN 'Medium' THEN 3 
        ELSE 4 
    END
    """
    return execute_query(query)

def get_inspection_summary(property_id):
    """Get AI-generated inspection summary"""
    query = f"""
    SELECT summary_text, total_defects, critical_issues, affected_rooms
    FROM INSPECTION_SUMMARY 
    WHERE property_id = '{property_id}'
    """
    return execute_query(query)