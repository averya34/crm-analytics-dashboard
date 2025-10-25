import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

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
    # This will be replaced with Google Drive integration
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
    
    # Replace blanks with standard values
    df = df.fillna("Unassigned")
    
    # Parse dates
    date_columns = ["Date Added", "Last Assigned", "Appointment Date"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    
    # Standardize text fields
    text_columns = ["Stage", "Source", "Agent", "Tags"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    return df

def calculate_kpis(df):
    """Calculate key performance indicators"""
    kpis = {}
    
    # Total leads
    kpis["total_leads"] = len(df)
    
    # Contacted rate
    if "Is Contacted" in df.columns:
        contacted = df[df["Is Contacted"] == "Yes"].shape[0]
        kpis["contact_rate"] = (contacted / kpis["total_leads"] * 100) if kpis["total_leads"] > 0 else 0
    else:
        kpis["contact_rate"] = 0
    
    # Appointment metrics
    if "Stage" in df.columns:
        appt_set = df[df["Stage"].str.contains("Appointment", case=False, na=False)].shape[0]
        kpis["appointment_rate"] = (appt_set / kpis["total_leads"] * 100) if kpis["total_leads"] > 0 else 0
        kpis["appointments_set"] = appt_set
    else:
        kpis["appointment_rate"] = 0
        kpis["appointments_set"] = 0
    
    # New leads this week
    if "Date Added" in df.columns:
        week_ago = datetime.now() - timedelta(days=7)
        new_this_week = df[df["Date Added"] >= week_ago].shape[0]
        kpis["new_this_week"] = new_this_week
    else:
        kpis["new_this_week"] = 0
    
    return kpis

# Main app
st.title("📊 CRM Analytics Dashboard")
st.markdown("### Real-time insights from Follow Up Boss")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Data refresh
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Data Source:** Google Drive")
    st.markdown("**Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))

# Load and clean data
df = load_sample_data()
df = clean_data(df)

# Calculate KPIs
kpis = calculate_kpis(df)

# Overview Tab
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "📅 Appointments", "👥 Agents", "🎯 Sources", "🏷️ Tags"])

with tab1:
    st.header("Performance Overview")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Leads", kpis["total_leads"], delta=kpis["new_this_week"])
    
    with col2:
        st.metric("Contact Rate", str(round(kpis["contact_rate"], 1)) + "%")
    
    with col3:
        st.metric("Appointments Set", kpis["appointments_set"])
    
    with col4:
        st.metric("Appointment Rate", str(round(kpis["appointment_rate"], 1)) + "%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Leads by Stage")
        if "Stage" in df.columns:
            stage_counts = df["Stage"].value_counts()
            fig = px.pie(values=stage_counts.values, names=stage_counts.index, 
                        color_discrete_sequence=px.colors.sequential.Purples)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Leads by Source")
        if "Source" in df.columns:
            source_counts = df["Source"].value_counts()
            fig = px.bar(x=source_counts.index, y=source_counts.values,
                        color=source_counts.values,
                        color_continuous_scale="Purples")
            fig.update_layout(xaxis_title="Source", yaxis_title="Count", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Appointment Analytics")
    
    # Filter for appointments
    appt_df = df[df["Stage"].str.contains("Appointment", case=False, na=False)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Appointments", len(appt_df))
    
    with col2:
        completed = appt_df[appt_df["Stage"].str.contains("Completed", case=False, na=False)].shape[0]
        st.metric("Completed", completed)
    
    # Appointment timeline
    if "Date Added" in appt_df.columns and len(appt_df) > 0:
        st.subheader("Appointments Over Time")
        appt_timeline = appt_df.groupby(appt_df["Date Added"].dt.date).size().reset_index()
        appt_timeline.columns = ["Date", "Count"]
        fig = px.line(appt_timeline, x="Date", y="Count", markers=True)
        fig.update_traces(line_color="#667eea")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Agent Performance")
    
    if "Agent" in df.columns:
        agent_stats = df.groupby("Agent").agg({
            "Name": "count",
            "Is Contacted": lambda x: (x == "Yes").sum()
        }).reset_index()
        agent_stats.columns = ["Agent", "Total Leads", "Contacted"]
        agent_stats["Contact Rate"] = (agent_stats["Contacted"] / agent_stats["Total Leads"] * 100).round(1)
        
        st.dataframe(agent_stats, use_container_width=True)
        
        # Agent comparison chart
        fig = px.bar(agent_stats, x="Agent", y="Total Leads", 
                    color="Contact Rate",
                    color_continuous_scale="Purples")
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Lead Source Analysis")
    
    if "Source" in df.columns:
        source_stats = df.groupby("Source").agg({
            "Name": "count"
        }).reset_index()
        source_stats.columns = ["Source", "Total Leads"]
        source_stats = source_stats.sort_values("Total Leads", ascending=False)
        
        st.dataframe(source_stats, use_container_width=True)
        
        # Source performance
        fig = px.treemap(source_stats, path=["Source"], values="Total Leads",
                        color="Total Leads",
                        color_continuous_scale="Purples")
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("Tag Analysis")
    
    if "Tags" in df.columns:
        tag_counts = df["Tags"].value_counts().reset_index()
        tag_counts.columns = ["Tag", "Count"]
        
        st.dataframe(tag_counts, use_container_width=True)
        
        # Tag distribution
        fig = px.bar(tag_counts, x="Tag", y="Count",
                    color="Count",
                    color_continuous_scale="Purples")
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**CRM Analytics Dashboard** | Built with Streamlit | Data from Follow Up Boss")
