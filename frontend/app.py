"""
Streamlit Frontend for Zero-Click CRM
Main dashboard interface
"""
import streamlit as st
import requests
import os
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Zero-Click CRM",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎯 Zero-Click CRM</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered CRM That Updates Itself</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Navigation")
    page = st.radio(
        "Choose a view:",
        ["🏠 Dashboard", "🎤 Voice Input", "✉️ Text Input", "🔍 Smart Search", "📊 Analytics"]
    )
    
    st.divider()
    st.caption("Zero-Click CRM v1.0")
    st.caption("Built with FastAPI + Streamlit + Claude AI")

# Helper functions
def fetch_data(endpoint):
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

def format_currency(value):
    """Format value as currency"""
    if value is None:
        return "N/A"
    return f"${value:,.2f}"

def format_date(date_str):
    """Format date string"""
    if not date_str:
        return "N/A"
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date.strftime("%b %d, %Y")
    except:
        return date_str

# ==================== DASHBOARD PAGE ====================
if page == "🏠 Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Fetch data
    contacts_data = fetch_data("contacts")
    deals_data = fetch_data("deals")
    activities_data = fetch_data("activities")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        contact_count = len(contacts_data.get("contacts", [])) if contacts_data else 0
        st.metric("Total Contacts", contact_count)
    
    with col2:
        deal_count = len(deals_data.get("deals", [])) if deals_data else 0
        st.metric("Active Deals", deal_count)
    
    with col3:
        total_value = sum(d.get("deal_value", 0) or 0 for d in deals_data.get("deals", [])) if deals_data else 0
        st.metric("Pipeline Value", format_currency(total_value))
    
    with col4:
        activity_count = len(activities_data.get("activities", [])) if activities_data else 0
        st.metric("Recent Activities", activity_count)
    
    st.divider()
    
    # Recent Deals
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤝 Recent Deals")
        if deals_data and deals_data.get("deals"):
            for deal in deals_data["deals"][:5]:
                with st.container():
                    contact_name = deal.get("contacts", {}).get("name", "Unknown") if isinstance(deal.get("contacts"), dict) else "Unknown"
                    company = deal.get("contacts", {}).get("company", "") if isinstance(deal.get("contacts"), dict) else ""
                    
                    st.markdown(f"**{contact_name}** {f'@ {company}' if company else ''}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.caption(f"💰 {format_currency(deal.get('deal_value'))}")
                    with col_b:
                        st.caption(f"📅 {format_date(deal.get('follow_up_date'))}")
                    
                    if deal.get("next_step"):
                        st.caption(f"📋 {deal['next_step']}")
                    
                    st.divider()
        else:
            st.info("No deals yet. Upload a voice note or enter text to get started!")
    
    with col2:
        st.subheader("👥 Recent Contacts")
        if contacts_data and contacts_data.get("contacts"):
            for contact in contacts_data["contacts"][:5]:
                with st.container():
                    st.markdown(f"**{contact.get('name', 'Unknown')}**")
                    if contact.get('company'):
                        st.caption(f"🏢 {contact['company']}")
                    if contact.get('email'):
                        st.caption(f"📧 {contact['email']}")
                    st.divider()
        else:
            st.info("No contacts yet.")

# ==================== VOICE INPUT PAGE ====================
elif page == "🎤 Voice Input":
    st.header("🎤 Voice Note Processing")
    st.write("Upload or record a voice note, and watch it auto-populate your CRM!")
    
    uploaded_file = st.file_uploader(
        "Upload Audio File",
        type=["wav", "mp3", "m4a", "ogg"],
        help="Supported formats: WAV, MP3, M4A, OGG"
    )
    
    if uploaded_file:
        st.audio(uploaded_file)
        
        if st.button("🚀 Process Audio", type="primary"):
            with st.spinner("🎯 Transcribing and extracting CRM data..."):
                try:
                    # Send to API
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(f"{API_URL}/upload_audio", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("✅ Successfully processed!")
                        
                        # Display results
                        st.subheader("📝 Transcript")
                        st.text_area("", result.get("transcript", ""), height=100)
                        
                        st.subheader("🤖 AI Summary")
                        st.info(result.get("summary", ""))
                        
                        st.subheader("📊 Extracted CRM Data")
                        extracted = result.get("extracted_data", {})
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Contact:**", extracted.get("contact_name", "N/A"))
                            st.write("**Company:**", extracted.get("company", "N/A"))
                            st.write("**Email:**", extracted.get("email", "N/A"))
                        with col2:
                            st.write("**Deal Value:**", format_currency(extracted.get("deal_value")))
                            st.write("**Next Step:**", extracted.get("next_step", "N/A"))
                            st.write("**Follow-up Date:**", format_date(extracted.get("follow_up_date")))
                        
                        if extracted.get("notes"):
                            st.write("**Notes:**", extracted["notes"])
                        
                        # Auto-refresh to show new data
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error processing audio: {str(e)}")
    
    st.divider()
    st.info("💡 **Tip:** Say something like: 'Hey, I just spoke with Sarah from Acme Corp. She wants to proceed with the $5,000 deal next Thursday.'")

# ==================== TEXT INPUT PAGE ====================
elif page == "✉️ Text Input":
    st.header("✉️ Text & Email Processing")
    st.write("Paste email content, meeting notes, or any text to extract CRM data automatically.")
    
    # Add tab for manual input vs sample emails
    input_tab, samples_tab = st.tabs(["📝 Manual Input", "📧 Sample Emails"])
    
    with input_tab:
        text_input = st.text_area(
            "Enter text to process:",
            height=200,
            placeholder="Example: Had a great call with John from TechStart Inc. They're interested in our enterprise plan at $10,000. Need to follow up next Monday with a proposal."
        )
        
        source_type = st.selectbox(
            "Source Type:",
            ["email", "meeting", "text", "manual"]
        )
        
        if st.button("🚀 Extract CRM Data", type="primary"):
            if not text_input.strip():
                st.warning("Please enter some text to process.")
            else:
                with st.spinner("🎯 Extracting CRM data..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/process_text",
                            json={"text": text_input, "source": source_type}
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            st.success("✅ Successfully extracted CRM data!")
                            
                            st.subheader("🤖 AI Summary")
                            st.info(result.get("summary", ""))
                            
                            st.subheader("📊 Extracted Data")
                            extracted = result.get("extracted_data", {})
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Contact:**", extracted.get("contact_name", "N/A"))
                                st.write("**Company:**", extracted.get("company", "N/A"))
                                st.write("**Email:**", extracted.get("email", "N/A"))
                            with col2:
                                st.write("**Deal Value:**", format_currency(extracted.get("deal_value")))
                                st.write("**Next Step:**", extracted.get("next_step", "N/A"))
                                st.write("**Follow-up:**", format_date(extracted.get("follow_up_date")))
                            
                            if extracted.get("notes"):
                                st.write("**Notes:**", extracted["notes"])
                            
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"Error: {response.text}")
                        
                    except Exception as e:
                        st.error(f"Error processing text: {str(e)}")
    
    with samples_tab:
        st.subheader("📧 Sample Emails for Demo")
        st.write("Click any sample email below to process it automatically:")
        
        # Fetch sample emails from backend
        try:
            samples_response = requests.get(f"{API_URL}/sample_emails")
            if samples_response.status_code == 200:
                samples = samples_response.json().get("samples", [])
                
                for i, sample in enumerate(samples):
                    with st.expander(f"📧 {sample.get('subject', 'Email Sample')}"):
                        st.write(f"**From:** {sample.get('from')}")
                        st.write(f"**Subject:** {sample.get('subject')}")
                        st.write("**Body:**")
                        st.text_area(f"email_body_{i}", sample.get("body", ""), height=200, key=f"sample_{i}", label_visibility="collapsed")
                        
                        if st.button(f"🚀 Process This Email", key=f"btn_{i}"):
                            with st.spinner("Processing email..."):
                                try:
                                    # Format as email
                                    email_text = f"From: {sample.get('from')}\nSubject: {sample.get('subject')}\n\n{sample.get('body')}"
                                    
                                    response = requests.post(
                                        f"{API_URL}/process_email",
                                        json={"email_text": email_text}
                                    )
                                    
                                    if response.status_code == 200:
                                        result = response.json()
                                        st.success("✅ Email processed successfully!")
                                        
                                        st.subheader("📊 Extracted Data")
                                        extracted = result.get("extracted_data", {})
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.write("**Contact:**", extracted.get("contact_name", "N/A"))
                                            st.write("**Company:**", extracted.get("company", "N/A"))
                                            st.write("**Email:**", extracted.get("email", "N/A"))
                                        with col2:
                                            st.write("**Deal Value:**", format_currency(extracted.get("deal_value")))
                                            st.write("**Next Step:**", extracted.get("next_step", "N/A"))
                                            st.write("**Follow-up:**", format_date(extracted.get("follow_up_date")))
                                        
                                        time.sleep(2)
                                        st.rerun()
                                    else:
                                        st.error(f"Error: {response.text}")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"Could not load sample emails: {str(e)}")

# ==================== SMART SEARCH PAGE ====================
elif page == "🔍 Smart Search":
    st.header("🔍 Natural Language Search")
    st.write("Ask questions about your CRM data in plain English!")
    
    query = st.text_input(
        "Enter your query:",
        placeholder="Example: Show all deals over $5,000 closing this week"
    )
    
    if st.button("🔍 Search", type="primary"):
        if not query.strip():
            st.warning("Please enter a search query.")
        else:
            with st.spinner("🎯 Searching..."):
                try:
                    response = requests.post(
                        f"{API_URL}/query",
                        json={"query": query}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success(f"✅ Found {result.get('count', 0)} results")
                        
                        st.subheader("🎯 Search Results")
                        
                        results = result.get("results", [])
                        
                        if results:
                            for item in results:
                                with st.container():
                                    # Check if it's a deal or contact
                                    if "deal_value" in item:
                                        contact_name = item.get("contacts", {}).get("name", "Unknown") if isinstance(item.get("contacts"), dict) else "Unknown"
                                        company = item.get("contacts", {}).get("company", "") if isinstance(item.get("contacts"), dict) else ""
                                        
                                        st.markdown(f"**Deal: {contact_name}** {f'@ {company}' if company else ''}")
                                        st.write(f"💰 Value: {format_currency(item.get('deal_value'))}")
                                        st.write(f"📅 Follow-up: {format_date(item.get('follow_up_date'))}")
                                        if item.get("next_step"):
                                            st.write(f"📋 Next: {item['next_step']}")
                                    else:
                                        st.markdown(f"**Contact: {item.get('name', 'Unknown')}**")
                                        if item.get('company'):
                                            st.write(f"🏢 {item['company']}")
                                        if item.get('email'):
                                            st.write(f"📧 {item['email']}")
                                    
                                    st.divider()
                        else:
                            st.info("No results found for your query.")
                        
                        # Show filters applied
                        with st.expander("🔧 Filters Applied"):
                            st.json(result.get("filters_applied", {}))
                    else:
                        st.error(f"Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error searching: {str(e)}")
    
    st.divider()
    st.markdown("**💡 Example Queries:**")
    st.write("- Show all deals over $5,000")
    st.write("- Find contacts from Acme Corp")
    st.write("- Deals closing this week")
    st.write("- Show all contacts with follow-ups")

# ==================== ANALYTICS PAGE ====================
elif page == "📊 Analytics":
    st.header("📊 Analytics & Insights")
    
    deals_data = fetch_data("deals")
    
    if deals_data and deals_data.get("deals"):
        deals = deals_data["deals"]
        
        # Total pipeline value
        total_value = sum(d.get("deal_value", 0) or 0 for d in deals)
        avg_deal = total_value / len(deals) if deals else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Pipeline", format_currency(total_value))
        with col2:
            st.metric("Average Deal Size", format_currency(avg_deal))
        with col3:
            st.metric("Total Deals", len(deals))
        
        st.divider()
        
        # Upcoming follow-ups
        st.subheader("📅 Upcoming Follow-ups")
        upcoming = [d for d in deals if d.get("follow_up_date")]
        upcoming.sort(key=lambda x: x.get("follow_up_date", ""))
        
        if upcoming:
            for deal in upcoming[:10]:
                contact_name = deal.get("contacts", {}).get("name", "Unknown") if isinstance(deal.get("contacts"), dict) else "Unknown"
                st.write(f"**{format_date(deal.get('follow_up_date'))}** - {contact_name}: {deal.get('next_step', 'Follow up')}")
        else:
            st.info("No upcoming follow-ups scheduled.")
    else:
        st.info("No analytics data available yet. Start adding deals to see insights!")

# Auto-refresh button
st.divider()
if st.button("🔄 Refresh Data"):
    st.rerun()
