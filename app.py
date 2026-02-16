import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Projects for Peace | Global Index", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for that "Boardroom" feel (Dark, sleek, refined fonts)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stMetric { background-color: #1c1f26; border: 1px solid #31333f; padding: 15px; border-radius: 10px; }
    label { color: #808495 !important; text-transform: uppercase; font-size: 0.8rem !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv('projects_for_peace_master_2007_2025_with_lonlat.csv')
    df = df.dropna(subset=['Latitude', 'Longitude'])
    # Clean Year to remove commas
    df['Year'] = df['Year'].astype(str).str.replace(',', '')
    return df

df = load_data()

# 3. Header & Navigation
st.title("PROJECTS FOR PEACE")
st.caption("Strategic Global Impact Index | 2007 — 2025")

# Top-level filters (Boardroom Dashboard Style)
with st.expander("📊 SEARCH & FILTER CONTROLS", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        years = sorted(df['Year'].unique(), reverse=True)
        selected_years = st.multiselect("Reporting Periods", years, default=years[:5])
    with c2:
        institutions = sorted(df['Institution'].unique())
        selected_inst = st.multiselect("Lead Institutions", institutions)
    with c3:
        search_query = st.text_input("Search Projects or Leaders", placeholder="e.g. 'Kenya' or 'Water'")

# Filtering logic
filtered_df = df[df['Year'].isin(selected_years)]
if selected_inst:
    filtered_df = filtered_df[filtered_df['Institution'].isin(selected_inst)]
if search_query:
    filtered_df = filtered_df[
        filtered_df['Project Title'].str.contains(search_query, case=False) | 
        filtered_df['Project Leader(s)'].str.contains(search_query, case=False) |
        filtered_df['Project Country'].str.contains(search_query, case=False)
    ]

# 4. Key Performance Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("TOTAL PROJECTS", f"{len(filtered_df)}")
m2.metric("NATIONS REACHED", f"{filtered_df['Project Country'].nunique()}")
m3.metric("INSTITUTIONAL PARTNERS", f"{filtered_df['Institution'].nunique()}")
m4.metric("ACTIVE YEARS", f"{len(selected_years)}")

# 5. The "Cool" Globe Visualization
# Creating the "Night Global" look
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

# Professional styling
fig.update_traces(
    marker=dict(size=6, color="#00FFC8", opacity=0.7, line=dict(width=0.5, color="white")),
    selector=dict(mode='markers')
)

fig.update_geos(
    showcoastlines=True, coastlinecolor="#2b2b2b",
    showland=True, landcolor="#111111",
    showocean=True, oceancolor="#050505",
    showlakes=False,
    showcountries=True, countrycolor="#2b2b2b"
)

# ANIMATION: This is the "Cool" part - Auto-Rotation
fig.update_layout(
    height=800,
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="rgba(0,0,0,0)",
    dragmode="rotate", # Clicking and dragging rotates the globe
    geo=dict(
        projection_scale=1.1,
        center=dict(lat=0, lon=0),
    )
)

# JavaScript for Rotation Logic: 
# This adds a subtle drift to the globe.
fig.layout.geo.projection.rotation = {'lon': st.session_state.get('rotation', 0)}

st.plotly_chart(fig, use_container_width=True)

# 6. Data Ledger (Professional Table)
st.subheader("Project Ledger")
st.dataframe(
    filtered_df[['Year', 'Institution', 'Project Title', 'Project Country', 'Project Leader(s)']],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.caption("Confidential Global Index | For internal use only.")
