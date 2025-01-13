import streamlit as st
import pandas as pd
import plotly.express as px

# Add the title and header
st.title("Interactive Dashboard for Solar Irradiance Data")

# Introduction Section
st.write(
    """
    Explore historical solar irradiance data and trends for Malaysia and Thailand. 
    Use the interactive charts to gain insights and make data-driven decisions.
    """
)

# Load the dataset (replace 'solar_data.csv' with the actual dataset file name)
data_path = 'solar_data.csv'  # Update with your file path
data = pd.read_csv(data_path)

# Ensure Datetime is parsed as a datetime object
data['Datetime'] = pd.to_datetime(data['Datetime'], format="%d/%m/%Y %H:%M")

# Display dataset summary
st.header("Dataset Overview")
st.write("This dataset contains key features for solar irradiance in Malaysia and Thailand.")
st.write(data.head())

# Provide filters for user interaction
st.sidebar.header("Filter Data")

region_filter = st.sidebar.multiselect(
    "Select Country:", options=data["Country"].unique(), default=data["Country"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range:", [data["Datetime"].min().date(), data["Datetime"].max().date()]
)

# Apply filters to the dataset
filtered_data = data[(data["Country"].isin(region_filter)) &
                     (data["Datetime"] >= pd.to_datetime(date_range[0])) &
                     (data["Datetime"] <= pd.to_datetime(date_range[1]))]

# Visualization Section
st.header("Visualizations")

# Line Chart: Solar Irradiance over Time
st.subheader("Solar Irradiance Over Time")
time_chart = px.line(
    filtered_data, x="Datetime", y="GHI (w/m2)", color="Country",
    title="Global Horizontal Irradiance (GHI) Over Time",
    labels={"Datetime": "Date and Time", "GHI (w/m2)": "GHI (W/m²)"}
)
st.plotly_chart(time_chart, use_container_width=True)

# Scatter Plot: Temperature vs GHI
st.subheader("Temperature vs Solar Irradiance")
temp_vs_ghi = px.scatter(
    filtered_data, x="Temperature (c)", y="GHI (w/m2)", color="Country",
    title="Relationship Between Temperature and GHI",
    labels={"Temperature (c)": "Temperature (°C)", "GHI (w/m2)": "GHI (W/m²)"}
)
st.plotly_chart(temp_vs_ghi, use_container_width=True)

# Heatmap: Average GHI by Month and Country
st.subheader("Heatmap of Solar Irradiance by Month")
filtered_data["Month"] = filtered_data["Datetime"].dt.month
heatmap_data = filtered_data.groupby(["Country", "Month"]).mean().reset_index()
ghi_heatmap = px.density_heatmap(
    heatmap_data, x="Month", y="Country", z="GHI (w/m2)", 
    color_continuous_scale=["blue", "white", "red"],
    title="Average Solar Irradiance by Month and Country",
    labels={"Month": "Month", "GHI (w/m2)": "GHI (W/m²)"}
)
st.plotly_chart(ghi_heatmap, use_container_width=True)

# Summary Insights Section
st.header("Key Insights")
st.write(
    """
    - Observe the temporal trends of solar irradiance to identify peak production times.
    - Analyze the relationship between temperature and solar irradiance to optimize solar panel efficiency.
    - Use the heatmap to understand hourly variations in solar irradiance for better scheduling.
    - Leverage geographic visualizations to pinpoint high-yield solar energy locations.
    """
)

# Footer
st.markdown("---")
st.write("Navigate to other sections using the menu on the left!")

