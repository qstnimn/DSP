import streamlit as st

st.set_page_config(
    page_title="Solar Irradiance in Malaysia and Thailand",
    page_icon="🌞☀",
    layout="wide",
    initial_sidebar_state="expanded")

pages = {
    'Navigation': [
        st.Page('about.py', title='About'),
        st.Page('dashboard.py', title='Dashboard'),
        st.Page('jamai.py', title='Prediction'),
        st.Page('map.py', title='Solar Power Map'),
    ]
}

pg = st.navigation(pages)
pg.run()