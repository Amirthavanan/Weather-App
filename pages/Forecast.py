import streamlit as st
import plotly.express as px
from services.weather_service import get_forecast

st.set_page_config(page_title="Weather Forecast", page_icon="📈", layout="wide")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("assets/style.css")

st.title("📈 5-Day Weather Forecast")

search_city = st.text_input("Enter City for Forecast", placeholder="e.g., Tokyo", value=st.session_state.get("forecast_city", ""))

if st.button("Get Forecast", use_container_width=True):
    if search_city:
        st.session_state["forecast_active"] = True
        st.session_state["forecast_city"] = search_city
    else:
        st.warning("Please enter a city.")

if st.session_state.get("forecast_active"):
    city_to_search = st.session_state.get("forecast_city")
    with st.spinner("Fetching forecast data..."):
        forecast_data = get_forecast(city_to_search)
        if "error" in forecast_data:
            st.error(forecast_data["error"])
        else:
            lst = forecast_data.get("list", [])
            dates = [item["dt_txt"] for item in lst]
            temps = [item["main"]["temp"] for item in lst]
            humidities = [item["main"]["humidity"] for item in lst]
            
            tab1, tab2 = st.tabs(["Temperature Trend", "Humidity Trend"])
            
            with tab1:
                fig_temp = px.area(x=dates, y=temps, title="Temperature Trend (°C)", labels={'x': 'Date', 'y': 'Temperature (°C)'})
                fig_temp.update_traces(line_color='#667eea', fillcolor='rgba(102, 126, 234, 0.3)')
                st.plotly_chart(fig_temp, use_container_width=True)
            
            with tab2:
                fig_hum = px.bar(x=dates, y=humidities, title="Humidity Trend (%)", labels={'x': 'Date', 'y': 'Humidity (%)'})
                fig_hum.update_traces(marker_color='#764ba2')
                st.plotly_chart(fig_hum, use_container_width=True)

