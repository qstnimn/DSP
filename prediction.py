import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from jamaibase import JamAI, protocol as p
import time
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Solar Irradiance in Malaysia and Thailand",
    page_icon="🌞🌅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["About", "Dashboard", "Prediction", "Solar Power Map"])

# About Page
if page == "About":
    st.title("Solar Irradiance in Malaysia and Thailand 🌞🌅")

    st.header("About the Dashboard")
    st.write(
        """
        This dashboard presents the outcomes of a data-driven approach to forecasting solar irradiance in Malaysia and Thailand. 
        By leveraging advanced machine learning techniques, the tool offers accurate predictions and insights to optimize solar energy utilization.
        """
    )

    st.subheader("Who Can Benefit?")
    st.write(
        """
        - **Solar Energy Providers**: Optimize site selection and solar panel installation.
        - **Policymakers**: Design effective incentives for renewable energy adoption.
        - **Researchers**: Gain insights into solar energy patterns and trends.
        - **Investors**: Evaluate the potential of solar energy projects.
        """
    )

    st.subheader("How to Use this Dashboard")
    st.write(
        """
        Navigate through the following sections:
        - **Prediction Tool**: Input key environmental features to predict solar irradiance (GHI) and gain actionable insights.
        - **Interactive Dashboard**: Explore historical data trends, visualizations, and comparisons for Malaysia and Thailand.
        - **Solar Power Map**: Explore the locations of solar power farms in these regions, along with their capacity and operational status.
        
        Use the sidebar menu to switch between sections and interact with the tools provided.
        """
    )

    st.subheader("Why This Matters")
    st.write(
        """
        Solar energy is a crucial component of the global transition to renewable energy. Accurate forecasting of solar irradiance can help:
        - Optimize energy production.
        - Reduce reliance on fossil fuels.
        - Increase efficiency in energy planning.
        
        This dashboard aims to make these insights accessible to all stakeholders.
        """
    )

    st.image("solarfarm.jpg", use_container_width=True)

# Dashboard Page
elif page == "Dashboard":
    st.title("Interactive Dashboard for Solar Irradiance Data")

    st.write(
        """
        Explore historical solar irradiance data and trends for Malaysia and Thailand. 
        Use the interactive charts to gain insights and make data-driven decisions.
        """
    )

    data_path = 'solar_data.csv'
    data = pd.read_csv(data_path)
    data['Datetime'] = pd.to_datetime(data['Datetime'], format="%d/%m/%Y %H:%M")

    st.header("Dataset Overview")
    st.write("This dataset contains key features for solar irradiance in Malaysia and Thailand.")
    st.write(data.head())

    st.sidebar.header("Filter Data")

    region_filter = st.sidebar.multiselect(
        "Select Country:", options=data["Country"].unique(), default=data["Country"].unique()
    )

    date_range = st.sidebar.date_input(
        "Select Date Range:", [data["Datetime"].min().date(), data["Datetime"].max().date()]
    )

    filtered_data = data[(data["Country"].isin(region_filter)) &
                         (data["Datetime"] >= pd.to_datetime(date_range[0])) &
                         (data["Datetime"] <= pd.to_datetime(date_range[1]))]

    st.header("Visualizations")

    st.subheader("Solar Irradiance Over Time")
    time_chart = px.line(
        filtered_data, x="Datetime", y="GHI (w/m2)", color="Country",
        title="Global Horizontal Irradiance (GHI) Over Time",
        labels={"Datetime": "Date and Time", "GHI (w/m2)": "GHI (W/m²)"}
    )
    st.plotly_chart(time_chart, use_container_width=True)

    st.subheader("Temperature vs Solar Irradiance")
    temp_vs_ghi = px.scatter(
        filtered_data, x="Temperature (c)", y="GHI (w/m2)", color="Country",
        title="Relationship Between Temperature and GHI",
        labels={"Temperature (c)": "Temperature (°C)", "GHI (w/m2)": "GHI (W/m²)"}
    )
    st.plotly_chart(temp_vs_ghi, use_container_width=True)

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

    st.header("Key Insights")
    st.write(
        """
        - Observe the temporal trends of solar irradiance to identify peak production times.
        - Analyze the relationship between temperature and solar irradiance to optimize solar panel efficiency.
        - Use the heatmap to understand hourly variations in solar irradiance for better scheduling.
        - Leverage geographic visualizations to pinpoint high-yield solar energy locations.
        """
    )

# Prediction Page
elif page == "Prediction":
    st.title("Solar Irradiance Prediction Tool with AI Assistance")

    st.write(
        """
        Use this tool to predict the Global Horizontal Irradiance (GHI) based on key environmental parameters. Select your region, 
        input the values, and receive actionable insights to optimize solar energy usage.
        """
    )

    rf_model_malaysia = joblib.load("tuned_random_forest_malaysia.pkl")
    rf_model_thailand = joblib.load("tuned_random_forest_thailand.pkl")
    scaler = joblib.load("scaler.pkl")

    def predict_ghi(model, input_data, scaler):
        scaled_input = scaler.transform([input_data])
        prediction = model.predict(scaled_input)
        return prediction[0]

    def generate_insights(ghi, input_data):
        return f"With a GHI of {ghi:.2f}, optimize panel tilt and consider energy storage for peak periods."

    st.sidebar.title("Region Selection")
    region = st.sidebar.radio("Choose Region", ["Malaysia", "Thailand"])

    dni = st.number_input("DNI (Direct Normal Irradiance)", min_value=0.0, max_value=1000.0, value=200.0)
    dhi = st.number_input("DHI (Diffuse Horizontal Irradiance)", min_value=0.0, max_value=700.0, value=200.0)
    temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=30.0)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)
    wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=20.0, value=5.0)
    precipitable_water = st.number_input("Precipitable Water (cm)", min_value=0.0, max_value=10.0, value=2.5)

    input_data = [dni, dhi, temperature, humidity, wind_speed, precipitable_water]

    if st.button("Predict GHI"):
        if region == "Malaysia":
            ghi = predict_ghi(rf_model_malaysia, input_data, scaler)
        else:
            ghi = predict_ghi(rf_model_thailand, input_data, scaler)

        st.success(f"Predicted GHI: {ghi:.2f} W/m²")
        insights = generate_insights(ghi, input_data)
        st.write(insights)

# Solar Power Map Page
elif page == "Solar Power Map":
    st.title("Interactive Solar Power Map: Malaysia and Thailand")

    solar_data = pd.read_excel("Global-Solar-Power-Tracker-June-2024-v2.xlsx")
    filtered_data = solar_data[solar_data['Country'].isin(['Malaysia', 'Thailand'])]

    st.sidebar.header("Filter Options")
    selected_country = st.sidebar.multiselect("Select Country", options=filtered_data['Country'].unique())
    selected_status = st.sidebar.multiselect("Select Project Status", options=filtered_data['Status'].unique())

    filtered_data = filtered_data[
        (filtered_data['Country'].isin(selected_country)) &
        (filtered_data['Status'].isin(selected_status))
    ]

    m = folium.Map(location=[4.2105, 101.9758], zoom_start=5)

    for _, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Project Name']} ({row['Status']})",
        ).add_to(m)

    st_folium(m, width=800, height=600)
