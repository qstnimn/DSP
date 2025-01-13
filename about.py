import streamlit as st


# Add the title and header
st.title("Solar Irradiance in Malaysia and Thailand 🌞☀")

# Introduction Section
st.header("About the Dashboard")
st.write(
    """
    This dashboard presents the outcomes of a data-driven approach to forecasting solar irradiance in Malaysia and Thailand. 
    By leveraging advanced machine learning techniques, the tool offers accurate predictions and insights to optimize solar energy utilization.
    """
)

# Who Benefits Section
st.subheader("Who Can Benefit?")
st.write(
    """
    - **Solar Energy Providers**: Optimize site selection and solar panel installation.
    - **Policymakers**: Design effective incentives for renewable energy adoption.
    - **Researchers**: Gain insights into solar energy patterns and trends.
    - **Investors**: Evaluate the potential of solar energy projects.
    """
)

# How to Use Section
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

# Visuals and Impact
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

# image placeholder
st.image("solarfarm.jpg", use_container_width=True)