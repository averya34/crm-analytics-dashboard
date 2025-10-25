import streamlit as st
from auth import check_password
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# Password protection - must be first
if not check_password():
    st.stop()

# Page configuration
st.set_page_config(
    page_title="CRM Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_sample_data():
    """Load sample CRM data for demonstration"""
    data = {
        "Name": ["John Doe", "Jane Smith", "Bob Johnson", "Alice Williams", "Charlie Brown"],
        "Email": ["john@example.com", "jane@example.com", "bob@example.com", "alice@example.com", "charlie@example.com"],
        "Phone": ["555-0101", "555-0102", "555-0103", "555-0104", "555-0105"],
        "Date Added": ["2025-10-01", "2025-10-05", "2025-10-10", "2025-10-15", "2025-10-20"],
        "Stage": ["New", "Contacted", "Appointment Set", "Appointment Completed", "New"],
        "Source": ["Website", "Referral", "Facebook", "Google Ads", "Website"],
        "Agent": ["Agent A", "Agent B", "Agent A", "Agent C", "Agent B"],
        "Tags": ["Investor", "Lifestyle", "Investor", "Lifestyle", "Investor"],
        "Is Contacted": ["Yes", "Yes", "Yes", "Yes", "No"]
    }
    df = pd.DataFrame(data)
    df["Date Added"] = pd.to_datetime(df["Date Added"])
    return df

def clean_data(df):
    """Clean and standardize CRM data"""
    df = df.copy()
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()
    return df

# Main app
st.title("📊 CRM Analytics Dashboard")

# Load data
df = load_sample_data()
df = clean_data(df)

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Date Range", [df["Date Added"].min(), df["Date Added"].max()])

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Appointments", "Agents", "Sources", "Tags"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(df))
    with col2:
        st.metric("Contacted", len(df[df["Is Contacted"] == "Yes"]))
    with col3:
        st.metric("Appointments", len(df[df["Stage"].str.contains("Appointment", na=False)]))
    with col4:
        st.metric("Conversion Rate", "40%")
    
    st.plotly_chart(px.line(df.groupby("Date Added").size().reset_index(name="count"), 
                            x="Date Added", y="count", title="Lead Trend"), use_container_width=True)

with tab2:
    st.subheader("Appointment Analysis")
    appt_df = df[df["Stage"].str.contains("Appointment", na=False)]
    st.dataframe(appt_df, use_container_width=True)

with tab3:
    st.subheader("Agent Performance")
    agent_stats = df.groupby("Agent").size().reset_index(name="Leads")
    st.plotly_chart(px.bar(agent_stats, x="Agent", y="Leads", title="Leads by Agent"), use_container_width=True)

with tab4:
    st.subheader("Lead Sources")
    source_stats = df.groupby("Source").size().reset_index(name="Leads")
    st.plotly_chart(px.pie(source_stats, names="Source", values="Leads", title="Lead Distribution"), use_container_width=True)

with tab5:
    st.subheader("Tag Analysis")
    tag_stats = df.groupby("Tags").size().reset_index(name="Count")
    st.plotly_chart(px.bar(tag_stats, x="Tags", y="Count", title="Leads by Tag"), use_container_width=True)
