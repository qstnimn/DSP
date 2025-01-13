import streamlit as st
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from jamaibase import JamAI, protocol as p
import time
import os
from dotenv import load_dotenv

# Load environment variables (optional)
load_dotenv()

# JamAI Configuration
PROJECT_ID = "proj_8d704451a1b1b274ce6fa450"  
PAT = "jamai_pat_3ccf690fb4e8030a00f8c3763a69fa628ffe61f4761239a5" 
TABLE_TYPE = p.TableType.chat
OPENER = "Hello! How can I help you with solar energy optimization?"

# Initialize JamAI
jamai = JamAI(project_id=PROJECT_ID, token=PAT)

# Helper function to create a new chat session
def create_new_chat():
    timestamp = int(time.time())
    new_table_id = f"Chat_{timestamp}"
    try:
        jamai.table.duplicate_table(
            table_type=TABLE_TYPE,
            table_id_src="AI_Chatbot",
            table_id_dst=new_table_id,
            include_data=True,
            create_as_child=True
        )
        return new_table_id
    except Exception as e:
        st.error(f"Error creating new chat: {str(e)}")
        return None

# Load the pre-trained models and scaler
rf_model_malaysia = joblib.load("tuned_random_forest_malaysia.pkl")
rf_model_thailand = joblib.load("tuned_random_forest_thailand.pkl")
scaler = joblib.load("scaler.pkl")

# Helper function to predict GHI
def predict_ghi(model, input_data, scaler):
    # Scale the input data
    scaled_input = scaler.transform([input_data])
    # Make prediction
    prediction = model.predict(scaled_input)
    return prediction[0]

# Helper function to generate actionable insights
def generate_insights(ghi, input_data):
    try:
        # Structure the input for JamAI
        structured_input = {
            "DNI": input_data[0],
            "DHI": input_data[1],
            "Temperature": input_data[2],
            "Humidity": input_data[3],
            "Wind Speed": input_data[4],
            "Precipitable Water": input_data[5],
            "GHI": ghi,
        }

        # Prepare a message for JamAI
        user_prompt = f"""
        Based on the predicted solar irradiance (GHI) of {ghi:.2f} W/m² and the following environmental conditions:
        - DNI: {structured_input["DNI"]} W/m²
        - DHI: {structured_input["DHI"]} W/m²
        - Temperature: {structured_input["Temperature"]} °C
        - Humidity: {structured_input["Humidity"]}%
        - Wind Speed: {structured_input["Wind Speed"]} m/s
        - Precipitable Water: {structured_input["Precipitable Water"]} cm

        Provide actionable suggestions for solar energy optimization, such as ideal panel configurations, expected power output, and energy cost savings.
        """

        # Call JamAI for suggestions
        response = ""
        for chunk in jamai.table.add_table_rows(
            table_type=TABLE_TYPE,
            request=p.RowAddRequest(
                table_id=st.session_state.table_id,
                data=[{"User": user_prompt}],
                stream=True
            )
        ):
            if isinstance(chunk, p.GenTableStreamChatCompletionChunk):
                if chunk.output_column_name == "AI":
                    response += chunk.choices[0].message.content

        return response.strip()

    except Exception as e:
        return f"Error generating insights: {str(e)}"

# Streamlit app
st.title("Solar Irradiance Prediction Tool with AI Assistance")

# Introduction Section
st.write(
    """
    Use this tool to predict the Global Horizontal Irradiance (GHI) based on key environmental parameters. Select your region, 
    input the values, and receive actionable insights to optimize solar energy usage.
    """
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Prediction (Malaysia)", "Prediction (Thailand)"])

# Initialize chat session state
if "table_id" not in st.session_state:
    new_table_id = create_new_chat()
    st.session_state.table_id = new_table_id

# Prediction for Malaysia
if page == "Prediction (Malaysia)":
    col1, col2 = st.columns([1, 2])  # Create two columns

    with col1:  # Left column for predictions
        st.header("Predict Solar Irradiance in Malaysia")

        # Input fields for prediction
        dni = st.number_input("DNI (Direct Normal Irradiance) [w/m²]", min_value=0.0, max_value=1000.0, value=200.0, step=0.1)
        st.caption("The amount of solar radiation received per unit area that comes directly from the sun.")

        dhi = st.number_input("DHI (Diffuse Horizontal Irradiance) [w/m²]", min_value=0.0, max_value=700.0, value=200.0, step=0.1)
        st.caption("The amount of solar radiation received per unit area that is scattered by the atmosphere and clouds.")

        temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=30.0, step=0.1)
        st.caption("The ambient air temperature in degrees Celsius.")

        humidity = st.number_input("Relative Humidity (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
        st.caption("The percentage of water vapor present in the air relative to its capacity at a given temperature.")

        wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
        st.caption("The speed of the wind near the surface, which can influence the cooling effect on solar panels.")

        precipitable_water = st.number_input("Precipitable Water (cm)", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
        st.caption("The depth of water in a column of the atmosphere, if all the water vapor were condensed into liquid.")

        # Prepare input data
        input_data = [dni, dhi, temperature, humidity, wind_speed, precipitable_water]
    
    with col2:
        # Predict button
        if st.button("Predict GHI (Malaysia)"):
            ghi = predict_ghi(rf_model_malaysia, input_data, scaler)
            st.success(f"Predicted GHI: {ghi:.2f} w/m²")

            # Generate insights
            insights = generate_insights(ghi, input_data)
            st.markdown("### Actionable Insights")
            st.write(insights)

# Prediction for Thailand
if page == "Prediction (Thailand)":
    col1, col2 = st.columns([1, 2])  # Create two columns

    with col1:  # Left column for predictions
        st.header("Predict Solar Irradiance in Thailand")

        # Input fields for prediction
        dni = st.number_input("DNI (Direct Normal Irradiance) [w/m²]", min_value=0.0, max_value=1000.0, value=200.0, step=0.1)
        st.caption("The amount of solar radiation received per unit area that comes directly from the sun.")

        dhi = st.number_input("DHI (Diffuse Horizontal Irradiance) [w/m²]", min_value=0.0, max_value=700.0, value=200.0, step=0.1)
        st.caption("The amount of solar radiation received per unit area that is scattered by the atmosphere and clouds.")

        temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=30.0, step=0.1)
        st.caption("The ambient air temperature in degrees Celsius.")

        humidity = st.number_input("Relative Humidity (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
        st.caption("The percentage of water vapor present in the air relative to its capacity at a given temperature.")

        wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
        st.caption("The speed of the wind near the surface, which can influence the cooling effect on solar panels.")

        precipitable_water = st.number_input("Precipitable Water (cm)", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
        st.caption("The depth of water in a column of the atmosphere, if all the water vapor were condensed into liquid.")

        # Prepare input data
        input_data = [dni, dhi, temperature, humidity, wind_speed, precipitable_water]

    with col2:
                # Predict button
        if st.button("Predict GHI (Thailand)"):
            ghi = predict_ghi(rf_model_thailand, input_data, scaler)
            st.success(f"Predicted GHI: {ghi:.2f} w/m²")

            # Generate insights
            insights = generate_insights(ghi, input_data)
            st.markdown("### Actionable Insights")
            st.write(insights)