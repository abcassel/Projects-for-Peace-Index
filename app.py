import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Projects for Peace | Global Impact Index", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for a Clean, Professional "International Organization" Aesthetic
st.markdown("""
    <style>
    /* Clean white background */
    .main { background-color: #FFFFFF; }
    
    /* Professional Typography */
    h1, h2, h3 { 
        color: #2c3e50; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #fcfcfc;
        border-right: 1px solid #eeeeee;
    }

    /* Soft Blue Metric Cards */
    div.stMetric {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #d0e1f9;
    }

    /* Legend styling fix for spacing */
    .legendtext { font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv('projects_for_peace_master_2007_2025_with_lonlat.csv')
    # Clean coordinates
    df = df.dropna(subset=['Latitude', 'Longitude'])
    # Keep Year as numeric for sorting, and string for categorical coloring
    df['Year_Str'] = df['Year'].astype(str).str.replace(',', '')
    return df

df = load_data()

# 3. Sidebar (LEFT SIDE) - Search & Filters with Emojis
st.sidebar.title("🔍 Filter Database")
st.sidebar.markdown("Explore the global reach of student-led peace initiatives.")

# Year Multi-select
all_years = sorted(df['Year_Str'].unique(), key=int, reverse=True)
selected_years = st.sidebar.multiselect("📅 Select Years", all_years, default=all_years)

# Institution Multi-select
all_institutions = sorted(df['Institution'].unique())
selected_inst = st.sidebar.multiselect("🎓 Select Institutions", all_institutions)

# Country Multi-select
all_countries = sorted(df['Project Country'].dropna().unique())
selected_country = st.sidebar.multiselect("📍 Select Countries", all_countries)

# Text Search
search_query = st.sidebar.text_input("⌨️ Keyword Search", placeholder="Search titles or leaders...")

# --- Apply Filtering Logic ---
filtered_df = df[df['Year_Str'].isin(selected_years)]
if selected_inst:
    filtered_df = filtered_df[filtered_df['Institution'].isin(selected_inst)]
if selected_country:
    filtered_df = filtered_df[filtered_df['Project Country'].isin(selected_country)]
if search_query:
    filtered_df = filtered_df[
        filtered_df['Project Title'].str.contains(search_query, case=False, na=False) | 
        filtered_df['Project Leader(s)'].str.contains(search_query, case=False, na=False)
    ]

# 4. Main Content Header
st.title("Projects for Peace")
st.markdown("### 🌎 A Global Registry of Student-Led Peace Initiatives")

# Metrics with Emojis
m1, m2, m3 = st.columns(3)
m1.metric("🕊️ Total Projects", f"{len(filtered_df)}")
m2.metric("🗺️ Nations Impacted", f"{filtered_df['Project Country'].nunique()}")
m3.metric("🏫 University Partners", f"{filtered_df['Institution'].nunique()}")

# 5. The Multi-Color Globe
# FIX: Sort the dataframe by Year (numerical) before plotting.
# This ensures the legend (2007, 2008... 2025) is in perfect chronological order.
filtered_df = filtered_df.sort_values("Year")

fig = px.scatter_geo(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color="Year_Str", 
    hover_name="Project Title",
    hover_data={
        "Institution": True,
        "Project Country": True,
        "Project Leader(s)": True,
        "Year": True,
        "Year_Str": False, # Hide the string version from popup
        "Latitude": False,
        "Longitude": False
    },
    # EMOJI-ONLY LABELS: Removes the text "Institution", "Year", etc.
    labels={
        "Institution": "🏫",
        "Project Country": "📍",
        "Project Leader(s)": "👤",
        "Year": "📅"
    },
    projection="orthographic",
    template="plotly_white",
    # Using 'Alphabet' palette for high contrast between adjacent years
    color_discrete_sequence=px.colors.qualitative.Alphabet 
)

# Stylize the Points & Globe
fig.update_traces(
    marker=dict(
        size=8, 
        opacity=0.85, 
        line=dict(width=0.5, color='white')
    )
)

fig.update_geos(
    showcoastlines=True, coastlinecolor="#cccccc",
    showland=True, landcolor="#fcfcfc",
    showocean=True, oceancolor="#eef8ff",
    showcountries=True, countrycolor="#eeeeee",
    lataxis_showgrid=False, lonaxis_showgrid=False
)

# Legend and Layout Adjustments
fig.update_layout(
    height=750,
    margin={"r":0,"t":20,"l":0,"b":0},
    legend_title_text='Select Year to Highlight',
    legend=dict(
        orientation="h", 
        yanchor="bottom", 
        y=1.02, 
        xanchor="right", 
        x=1,
        traceorder="normal" # Respects the sorted order of the dataframe
    ),
    paper_bgcolor="rgba(0,0,0,0)",
)

# Instructions for the interactive legend
st.info("💡 **Tip:** Double-click a year in the legend to isolate those projects; click single years to toggle them on/off.")

st.plotly_chart(fig, use_container_width=True)

# 6. Detailed Project Ledger
st.markdown("### 📋 Detailed Project Ledger")
st.dataframe(
    filtered_df[['Year', 'Institution', 'Project Title', 'Project Country', 'Project Leader(s)']],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.caption("Data source: Projects for Peace Master Database 2007-2025. This platform celebrates the creativity and commitment of young peacebuilders globally.")
