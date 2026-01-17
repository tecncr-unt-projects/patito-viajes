"""
Patito Viajes - Travel Planning Assistant
A Streamlit frontend for the Patito Viajes n8n workflow.
"""

import streamlit as st
import requests
import os
from datetime import date, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")
APP_TITLE = os.getenv("APP_TITLE", "🦆 Patito Viajes")
REQUEST_TIMEOUT = 120  # 2 minute timeout for n8n workflow processing

# Page configuration
st.set_page_config(
    page_title="Patito Viajes - Travel Planner",
    page_icon="🦆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .result-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    .error-box {
        background-color: #fff5f5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #e53e3e;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fff4;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #38a169;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🦆 Patito Viajes</h1>
    <p>Your AI-Powered Travel Planning Assistant</p>
</div>
""", unsafe_allow_html=True)


def validate_webhook_url():
    """Validate that the webhook URL is configured."""
    if not N8N_WEBHOOK_URL:
        st.error("⚠️ N8N_WEBHOOK_URL is not configured. Please set it in your .env file.")
        st.markdown("""
        <div class="info-box">
            <strong>How to configure:</strong>
            <ol>
                <li>Copy <code>.env.example</code> to <code>.env</code></li>
                <li>Set <code>N8N_WEBHOOK_URL</code> to your n8n webhook URL</li>
                <li>Restart the Streamlit app</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        return False
    return True


def send_travel_request(origin: str, destination: str, departure_date: str, return_date: str = None):
    """Send a travel search request to the n8n webhook."""
    payload = {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date
    }
    
    if return_date:
        payload["return_date"] = return_date
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. The server took too long to respond."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Could not connect to the n8n workflow. Please check if the webhook URL is correct."}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP Error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {str(e)}"}


def main():
    """Main application logic."""
    
    # Sidebar for search inputs
    with st.sidebar:
        st.header("🔍 Search Parameters")
        
        # Origin input
        origin = st.text_input(
            "✈️ Origin",
            placeholder="e.g., SJO, New York, LAX",
            help="Enter city name or airport code"
        )
        
        # Destination input
        destination = st.text_input(
            "🎯 Destination",
            placeholder="e.g., MIA, Paris, NRT",
            help="Enter city name or airport code"
        )
        
        # Date inputs
        st.subheader("📅 Travel Dates")
        
        min_date = date.today()
        max_date = date.today() + timedelta(days=365)
        
        departure_date = st.date_input(
            "Departure Date",
            value=date.today() + timedelta(days=7),
            min_value=min_date,
            max_value=max_date,
            help="Select your departure date"
        )
        
        # Round trip toggle
        is_round_trip = st.checkbox("🔄 Round Trip", value=True)
        
        return_date = None
        if is_round_trip:
            return_date = st.date_input(
                "Return Date",
                value=departure_date + timedelta(days=7),
                min_value=departure_date + timedelta(days=1),
                max_value=max_date,
                help="Select your return date"
            )
        
        st.divider()
        
        # Search button
        search_clicked = st.button("🔍 Find My Trip", type="primary")
        
        st.divider()
        
        # Help section
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. **Enter Origin**: Your departure city or airport code
            2. **Enter Destination**: Where you want to travel
            3. **Select Dates**: Pick your travel dates
            4. **Search**: Click "Find My Trip" to get recommendations
            
            **Tips:**
            - Use airport codes (e.g., LAX, JFK) for more accurate results
            - Allow enough time for the AI to process your request
            - Results include flights, hotels, and activities
            """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <strong>Welcome to Patito Viajes!</strong><br>
            Enter your travel details in the sidebar and click "Find My Trip" to get personalized 
            recommendations for flights, hotels, and activities powered by AI.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        **Powered by:**
        - 🔍 SerpAPI (Google Flights, Hotels)
        - 🤖 Google Gemini AI
        - ⚡ n8n Workflow Automation
        """)
    
    # Handle search
    if search_clicked:
        # Validate webhook URL first
        if not validate_webhook_url():
            return
        
        # Validate inputs
        if not origin:
            st.error("❌ Please enter an origin city or airport code.")
            return
        
        if not destination:
            st.error("❌ Please enter a destination city or airport code.")
            return
        
        # Show loading state
        with st.spinner("🔍 Searching for the best travel options... This may take a minute."):
            # Format dates
            dep_date_str = departure_date.strftime("%Y-%m-%d")
            ret_date_str = return_date.strftime("%Y-%m-%d") if return_date else None
            
            # Send request
            result = send_travel_request(origin, destination, dep_date_str, ret_date_str)
        
        # Display results
        if result.get("success", False):
            st.markdown("""
            <div class="success-box">
                <strong>✅ Search completed successfully!</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Display the markdown response
            st.markdown("---")
            st.markdown("## 📋 Your Travel Summary")
            
            markdown_content = result.get("markdown", "No results available.")
            st.markdown(markdown_content)
            
            # Download option
            st.download_button(
                label="📥 Download Results as Markdown",
                data=markdown_content,
                file_name=f"travel_plan_{origin}_to_{destination}_{dep_date_str}.md",
                mime="text/markdown"
            )
            
        else:
            error_msg = result.get("error", "An unknown error occurred.")
            st.markdown(f"""
            <div class="error-box">
                <strong>❌ Search failed</strong><br>
                {error_msg}
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 **Tip:** Make sure your n8n workflow is active and the webhook URL is correct.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Made with ❤️ by <a href="https://github.com/tecncr" target="_blank" rel="noopener noreferrer">tecncr</a></p>
        <p style="font-size: 0.8rem;">
            🦆 Patito Viajes uses SerpAPI for real-time travel data and Google Gemini for AI-powered summaries.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
