import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry_convert as pc

# Page configuration for a "Friendly & Hopeful" look
st.set_page_config(page_title="Projects for Peace Global Map", layout="wide")

st.title("🌍 Projects for Peace: Global Impact")
st.markdown("Exploring student-led initiatives for peace across the globe (2007-2025).")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('projects_for_peace_master_2007_2025_with_lonlat.csv')
    
    # Clean data
    df = df.dropna(subset=['Latitude', 'Longitude'])
    
    # Helper to map country to continent (Global Region)
    def country_to_continent(country_name):
        try:
            # Handle common exceptions or aliases if necessary
            if country_name == "Palestine": return "Asia"
            if country_name == "Kosovo": return "Europe"
            
            country_code = pc.country_name_to_country_alpha2(country_name)
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            continent_map = {
                'AF': 'Africa', 'AS': 'Asia', 'EU': 'Europe', 
                'NA': 'North America', 'SA': 'South America', 'OC': 'Oceania', 'AN': 'Antarctica'
            }
            return continent_map.get(continent_code, "Other")
        except:
            return "Other"

    df['Global Region'] = df['Project Country'].apply(country_to_continent)
    return df

df = load_data()

# 2. Sidebar Filters
st.sidebar.header("Filter Projects")

# Year Filter
years = sorted(df['Year'].unique(), reverse=True)
selected_year = st.sidebar.multiselect("Select Year(s)", years, default=years)

# Institution Filter
institutions = sorted(df['Institution'].unique())
selected_inst = st.sidebar.multiselect("Select Institution", institutions)

# Region Filter
regions = sorted(df['Global Region'].unique())
selected_region = st.sidebar.multiselect("Select Global Region", regions, default=regions)

# Search Boxes
search_project = st.sidebar.text_input("Search Project Name")
search_leader = st.sidebar.text_input("Search Student Leader")

# 3. Apply Filters
filtered_df = df[df['Year'].isin(selected_year)]
filtered_df = filtered_df[filtered_df['Global Region'].isin(selected_region)]

if selected_inst:
    filtered_df = filtered_df[filtered_df['Institution'].isin(selected_inst)]
if search_project:
    filtered_df = filtered_df[filtered_df['Project Title'].str.contains(search_project, case=False, na=False)]
if search_leader:
    filtered_df = filtered_df[filtered_df['Project Leader(s)'].str.contains(search_leader, case=False, na=False)]

# 4. Display Stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Projects", len(filtered_df))
col2.metric("Countries Represented", filtered_df['Project Country'].nunique())
col3.metric("Institutions", filtered_df['Institution'].nunique())

# 5. Create the Globe Map
# We use scatter_geo with orthographic projection for the "Globe" look
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
    projection="orthographic", # This makes it a 3D Globe
    color="Global Region",
    template="plotly_dark", # Hopeful/Modern look
    size_max=15,
)

# Update layout for a friendlier aesthetic
fig.update_geos(
    showcountries=True, countrycolor="RebeccaPurple",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    projection_type="orthographic",
    coastlinecolor="white"
)

fig.update_layout(
    height=700,
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig, use_container_width=True)

# 6. Detailed Project View (Pop-up replacement)
if not filtered_df.empty:
    st.subheader("Project Details")
    st.dataframe(
        filtered_df[['Year', 'Institution', 'Project Title', 'Project Country', 'Project Leader(s)']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No projects found matching your filters. Try broadening your search!")
