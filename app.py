import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Projects for Peace | Global Impact", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for the "Boardroom" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stMetric { background-color: #1c1f26; border: 1px solid #31333f; padding: 20px; border-radius: 8px; }
    [data-testid="stExpander"] { border: 1px solid #31333f; background-color: #1c1f26; border-radius: 8px; }
    .stDataFrame { border: 1px solid #31333f; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv('projects_for_peace_master_2007_2025_with_lonlat.csv')
    df = df.dropna(subset=['Latitude', 'Longitude'])
    # Ensure Year is a string for filtering
    df['Year'] = df['Year'].astype(str)
    return df

df = load_data()

# 3. Header
st.title("🌎 PROJECTS FOR PEACE")
st.markdown("<h3 style='color: #808495; font-weight: 400;'>Global Strategic Impact Index</h3>", unsafe_allow_html=True)

# 4. Professional Filters
with st.expander("🔍 FILTERS & PARAMETERS", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        years = sorted(df['Year'].unique(), reverse=True)
        selected_years = st.multiselect("Reporting Periods", years, default=years)
    with col2:
        institutions = sorted(df['Institution'].unique())
        selected_inst = st.multiselect("Lead Institutions", institutions)
    with col3:
        search_query = st.text_input("Global Search", placeholder="Search project titles or leaders...")

# Apply Filtering
filtered_df = df[df['Year'].isin(selected_years)]
if selected_inst:
    filtered_df = filtered_df[filtered_df['Institution'].isin(selected_inst)]
if search_query:
    filtered_df = filtered_df[
        filtered_df['Project Title'].str.contains(search_query, case=False, na=False) | 
        filtered_df['Project Leader(s)'].str.contains(search_query, case=False, na=False)
    ]

# 5. Executive Metrics
m1, m2, m3 = st.columns(3)
m1.metric("TOTAL INITIATIVES", f"{len(filtered_df)}")
m2.metric("COUNTRIES REPRESENTED", f"{filtered_df['Project Country'].nunique()}")
m3.metric("INSTITUTIONAL PARTNERS", f"{filtered_df['Institution'].nunique()}")

# 6. The Interactive Globe
# Using "Plotly White" for a cleaner, high-finance look if you prefer, 
# but keeping "Plotly Dark" for the 'Cool' factor.
fig = px.scatter_geo(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Project Title",
    hover_data={
        "Institution": True,
        "Year": True,
        "Project Country": True,
        "Project Leader(s)": True,
        "Latitude": False,
        "Longitude": False
    },
    projection="orthographic",
    template="plotly_dark",
)

# Styling the Pins & Globe
fig.update_traces(
    marker=dict(
        size=7, 
        color="#00FFC8", # Glowing Mint
        opacity=0.8, 
        line=dict(width=0.5, color="white")
    )
)

fig.update_geos(
    showcoastlines=True, coastlinecolor="#444",
    showland=True, landcolor="#1a1a1a",
    showocean=True, oceancolor="#0a0a0a",
    showcountries=True, countrycolor="#444",
    lataxis_showgrid=False, lonaxis_showgrid=False
)

fig.update_layout(
    height=750,
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig, use_container_width=True)

# 7. The Project Ledger (Table)
st.subheader("Detailed Project Ledger")
st.dataframe(
    filtered_df[['Year', 'Institution', 'Project Title', 'Project Country', 'Project Leader(s)']],
    use_container_width=True,
    hide_index=True
)

st.caption("© Projects for Peace Index | 2007-2025")
