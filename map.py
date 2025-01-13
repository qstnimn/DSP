import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load the dataset
solar_data = pd.read_excel("Global-Solar-Power-Tracker-June-2024-v2.xlsx")

# Filter data for Malaysia and Thailand
filtered_data = solar_data[solar_data['Country'].isin(['Malaysia', 'Thailand'])]

# Status category descriptions
status_descriptions = {
    "Announced": "Proposed projects that have been described in corporate or government plans or media releases but have not yet taken concrete steps such as applying for permits.\n",
    "Pre-construction": "Projects that are actively moving forward in seeking governmental approvals, land rights, or financing.\n",
    "Construction": "Site preparation and equipment installation are underway.\n",
    "Operating": "The project has been formally commissioned; commercial operation has begun.\n",
    "Shelved": "Suspension of the project has been announced.\n",
    "Cancelled": "A cancellation announcement has been made."
}

# Color mapping for project statuses
status_colors = {
    "Announced": "purple",
    "Pre-construction": "orange",
    "Construction": "blue",
    "Operating": "green",
    "Shelved": "yellow",
    "Cancelled": "red"
}

# Streamlit App
st.title("Interactive Solar Power Map: Malaysia and Thailand")

# Sidebar Filters
with st.sidebar:
    st.header("Filter Options")
    selected_country = st.multiselect(
        "Select Country",
        options=filtered_data['Country'].unique(),
        default=['Malaysia', 'Thailand']
    )
    selected_status = st.multiselect(
        "Select Project Status (Hover for Description)",
        options=filtered_data['Status'].unique(),
        default=filtered_data['Status'].unique(),
        help="\n".join([f"{key}: {value}" for key, value in status_descriptions.items()])
    )
    selected_technology = st.multiselect(
        "Select Technology Type",
        options=filtered_data['Technology Type'].unique(),
        default=filtered_data['Technology Type'].unique()
    )

    # Filter data based on selections
    filtered_data = filtered_data[
        (filtered_data['Country'].isin(selected_country)) &
        (filtered_data['Status'].isin(selected_status)) &
        (filtered_data['Technology Type'].isin(selected_technology))
    ]

    # Sidebar summary
    st.markdown("### Summary")
    total_projects = len(filtered_data)
    total_capacity = filtered_data['Capacity (MW)'].sum()
    st.metric("Total Projects", total_projects)
    st.metric("Total Capacity (MW)", f"{total_capacity:.2f} MW")

# Main Section
st.write("### Solar Power Project Map")

# Map View Selector
map_view = st.radio(
    "Choose Map View",
    ["Normal View", "Earth View"],
    index=0
)

# Create Map
m = folium.Map(location=[4.2105, 101.9758], zoom_start=5)  # Center on Malaysia and Thailand

# Add map layers for toggling
if map_view == "Earth View":
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri, Maxar, Earthstar Geographics, and the GIS User Community",
        name="Satellite View",
        overlay=False
    ).add_to(m)
else:
    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="© OpenStreetMap contributors",
        name="OpenStreetMap",
        overlay=False
    ).add_to(m)

# Add CircleMarkers for each project
for _, row in filtered_data.iterrows():
    color = status_colors.get(row['Status'], "gray")  # Default to gray if status is not mapped
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,  # Adjust radius for smaller size
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"<b>Project Name:</b> {row['Project Name']}<br>"
              f"<b>Country:</b> {row['Country']}<br>"
              f"<b>Capacity:</b> {row['Capacity (MW)']} MW<br>"
              f"<b>Status:</b> {row['Status']}<br>"
              f"<b>Description:</b> {status_descriptions.get(row['Status'], 'No description available')}<br>"
              f"<b>Technology:</b> {row['Technology Type']}<br>"
              f"<b>Wikipedia:</b> <a href='{row['Wiki URL']}' target='_blank'>Learn more</a>",
    ).add_to(m)

# Display the map
st_folium(m, width=800, height=600)
