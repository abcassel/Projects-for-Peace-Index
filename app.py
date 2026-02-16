import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Projects for Peace | UN Global Index", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for the United Nations Aesthetic
st.markdown("""
    <style>
    /* Main background to clean white */
    .main { background-color: #FFFFFF; }
    
    /* Header styling in UN Blue */
    h1, h2, h3 { 
        color: #009EDB; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
        font-weight: 700;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E0E0E0;
    }

    /* Metric cards styling */
    div.stMetric {
        background-color: #F0F7FF;
        border-left: 5px solid #009EDB;
        padding: 15px;
        border-radius: 4px;
    }

    /* Table styling */
    .stDataFrame {
        border: 1px solid #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv('projects_for_peace_master_2007_2025_with_lonlat.csv')
    df = df.dropna(subset=['Latitude', 'Longitude'])
    # Ensure Year is a clean string
    df['Year'] = df['Year'].astype(str).str.replace(',', '')
    return df

df = load_data()

# 3. Sidebar (LEFT SIDE) - Search & Filters
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Flag_of_the_United_Nations.svg/640px-Flag_of_the_United_Nations.svg.png", width=120)
st.sidebar.title("Search Parameters")
st.sidebar.markdown("---")

# Year Multi-select
years = sorted(df['Year'].unique(), reverse=True)
selected_years = st.sidebar.multiselect("Reporting Periods", years, default=years)

# Institution Multi-select
institutions = sorted(df['Institution'].unique())
selected_inst = st.sidebar.multiselect("Educational Institutions", institutions)

# Country Multi-select
countries = sorted(df['Project Country'].dropna().unique())
selected_country = st.sidebar.multiselect("Project Countries", countries)

# Text Search
search_query = st.sidebar.text_input("Project Keyword Search", placeholder="e.g., Sustainability, Health...")

# --- Apply Filtering Logic ---
filtered_df = df[df['Year'].isin(selected_years)]
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
st.subheader("Global Peace and Security Initiative Index")

# Metric Row
m1, m2, m3 = st.columns(3)
m1.metric("Total Initiatives", f"{len(filtered_df)}")
m2.metric("Nations Impacted", f"{filtered_df['Project Country'].nunique()}")
m3.metric("University Partners", f"{filtered_df['Institution'].nunique()}")

# 5. The UN-Styled Globe
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
    template="plotly_white" # Clean white template
)

# Styling for the "Peace" vibe
fig.update_traces(
    marker=dict(
        size=8, 
        color="#009EDB", # UN Blue
        opacity=0.6, 
        line=dict(width=0.5, color="white")
    )
)

fig.update_geos(
    showcoastlines=True, coastlinecolor="#DADADA",
    showland=True, landcolor="#F2F2F2",
    showocean=True, oceancolor="#E8F4F8", # Soft water blue
    showlakes=True, lakecolor="#E8F4F8",
    showcountries=True, countrycolor="#DADADA"
)

fig.update_layout(
    height=750,
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig, use_container_width=True)

# 6. Detailed Project Ledger
st.markdown("### Official Project Record")
st.dataframe(
    filtered_df[['Year', 'Institution', 'Project Title', 'Project Country', 'Project Leader(s)']],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.caption("This index represents a collective effort to build sustainable peace across global borders. | © Projects for Peace")
