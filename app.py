import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Projects for Peace | Global Impact Index", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for a Clean, Professional Aesthetic
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    h1, h2, h3 { 
        color: #2c3e50; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }
    section[data-testid="stSidebar"] {
        background-color: #fcfcfc;
        border-right: 1px solid #eeeeee;
    }
    /* Styling the metric cards to be softer */
    div.stMetric {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #d0e1f9;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv('projects_for_peace_master_2007_2025_with_lonlat.csv')
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df['Year_Str'] = df['Year'].astype(str).str.replace(',', '')
    return df

df = load_data()

# 3. Sidebar (LEFT SIDE) - Filters with Emojis
st.sidebar.title("🔍 Filter Database")
st.sidebar.markdown("Refine the global view using the parameters below.")

# Year Multi-select
all_years = sorted(df['Year_Str'].unique(), reverse=True)
selected_years = st.sidebar.multiselect("📅 Select Years", all_years, default=all_years)

# Institution Multi-select
all_institutions = sorted(df['Institution'].unique())
selected_inst = st.sidebar.multiselect("🎓 Select Institutions", all_institutions)

# Country Multi-select
all_countries = sorted(df['Project Country'].dropna().unique())
selected_country = st.sidebar.multiselect("📍 Select Countries", all_countries)

# Text Search
search_query = st.sidebar.text_input("⌨️ Keyword Search", placeholder="Search titles or leaders...")

# Filtering Logic
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

# 4. Main Content (RIGHT SIDE)
st.title("Projects for Peace")
st.markdown("### 🌎 A Global Registry of Student-Led Peace Initiatives")

# Metrics with Emojis
m1, m2, m3 = st.columns(3)
m1.metric("🕊️ Total Projects", f"{len(filtered_df)}")
m2.metric("🗺️ Nations Impacted", f"{filtered_df['Project Country'].nunique()}")
m3.metric("🏫 University Partners", f"{filtered_df['Institution'].nunique()}")

# 5. The Multi-Color Globe
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
        "Year_Str": False,
        "Latitude": False,
        "Longitude": False
    },
    projection="orthographic",
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Alphabet 
)

fig.update_traces(
    marker=dict(size=7, opacity=0.85, line=dict(width=0.5, color='white'))
)

fig.update_geos(
    showcoastlines=True, coastlinecolor="#cccccc",
    showland=True, landcolor="#fcfcfc",
    showocean=True, oceancolor="#eef8ff",
    showcountries=True, countrycolor="#eeeeee"
)

fig.update_layout(
    height=700,
    margin={"r":0,"t":20,"l":0,"b":0},
    legend_title_text='Year',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)

# 6. Data Ledger
st.markdown("### 📋 Detailed Project Ledger")
st.dataframe(
    filtered_df[['Year', 'Institution', 'Project Title', 'Project Country', 'Project Leader(s)']],
    use_container_width=True,
    hide_index=True
)

st.caption("Data source: Projects for Peace Master Database 2007-2025")
