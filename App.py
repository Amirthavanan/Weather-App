import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from streamlit_lottie import st_lottie
import folium
from streamlit_folium import st_folium
from services.weather_service import get_current_weather
from services.country_service import get_country_info
from database.db import get_db, log_search, log_weather

st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="wide")

# Load Custom CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("assets/style.css")

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie Animations mapping
lottie_urls = {
    "Clear": "https://assets1.lottiefiles.com/packages/lf20_stq51uhr.json",
    "Clouds": "https://assets1.lottiefiles.com/packages/lf20_k1xrco10.json",
    "Rain": "https://assets1.lottiefiles.com/packages/lf20_rpqozvwj.json",
    "Snow": "https://assets1.lottiefiles.com/packages/lf20_rhbwht1k.json",
    "Thunderstorm": "https://assets1.lottiefiles.com/packages/lf20_kuwz0q3h.json",
    "Default": "https://assets1.lottiefiles.com/packages/lf20_kkflmtur.json"
}

# Auto refresh
st_autorefresh(interval=60000, limit=None, key="weather_refresh")

st.title("🌤️ Global Real-Time Weather Analytics Dashboard")

# Search Section
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        search_city = st.text_input("Search City", placeholder="e.g., London", value=st.session_state.get("city_input", ""))
    with col2:
        search_country = st.text_input("Search Country", placeholder="e.g., UK", value=st.session_state.get("country_input", ""))
    
    get_weather_btn = st.button("Get Weather", use_container_width=True)

if get_weather_btn:
    if search_city or search_country:
        st.session_state["search_active"] = True
        st.session_state["city_input"] = search_city
        st.session_state["country_input"] = search_country
    else:
        st.warning("Please enter a city or country.")

if st.session_state.get("search_active"):
    city_to_search = st.session_state.get("city_input")
    country_to_search = st.session_state.get("country_input")
    with st.spinner("Fetching weather data..."):
        weather_data = get_current_weather(city_to_search, country_to_search)
        
        if "error" in weather_data:
            st.error(weather_data["error"])
        else:
            db = get_db()
            log_search(db, query=f"{city_to_search}, {country_to_search}", country=country_to_search, city=city_to_search)
            
            main = weather_data.get("main", {})
            wind = weather_data.get("wind", {})
            weather = weather_data.get("weather", [{}])[0]
            sys = weather_data.get("sys", {})
            coord = weather_data.get("coord", {})
            
            log_data = {
                "city": weather_data.get("name"),
                "country": sys.get("country"),
                "latitude": coord.get("lat"),
                "longitude": coord.get("lon"),
                "temperature": main.get("temp"),
                "feels_like": main.get("feels_like"),
                "humidity": main.get("humidity"),
                "pressure": main.get("pressure"),
                "wind_speed": wind.get("speed"),
                "cloudiness": weather_data.get("clouds", {}).get("all"),
                "weather_condition": weather.get("description")
            }
            log_weather(db, log_data)
            
            st.markdown("---")
            
            # Setup Tabs
            tab1, tab2, tab3 = st.tabs(["🌤️ Current Weather", "🌍 Location Map", "ℹ️ Country Info"])
            
            with tab1:
                col_lottie, col_info = st.columns([1, 2])
                
                with col_lottie:
                    condition = weather.get("main", "Default")
                    lottie_url = lottie_urls.get(condition, lottie_urls["Default"])
                    lottie_json = load_lottieurl(lottie_url)
                    if lottie_json:
                        st_lottie(lottie_json, height=200, key="weather_anim")
                
                with col_info:
                    st.header(f"{weather_data.get('name')}, {sys.get('country')}")
                    st.subheader(f"{weather.get('description').capitalize()}")
                    
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Temperature", f"{main.get('temp')} °C", delta=f"Feels {main.get('feels_like')} °C")
                col2.metric("Humidity", f"{main.get('humidity')}%")
                col3.metric("Wind Speed", f"{wind.get('speed')} m/s")
                col4.metric("Pressure", f"{main.get('pressure')} hPa")
            
            with tab2:
                st.markdown("### Location")
                m = folium.Map(location=[coord.get('lat'), coord.get('lon')], zoom_start=10)
                folium.Marker(
                    [coord.get('lat'), coord.get('lon')], 
                    popup=weather_data.get('name'), 
                    tooltip=weather_data.get('name'),
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
                st_folium(m, width=700, height=400)
            
            with tab3:
                country_name = sys.get("country")
                if country_name:
                    country_data = get_country_info(country_name)
                    if "error" not in country_data:
                        c_col1, c_col2 = st.columns([1, 2])
                        with c_col1:
                            flag_url = country_data.get("flags", {}).get("png")
                            if flag_url:
                                st.image(flag_url, width=200)
                        with c_col2:
                            st.write(f"**Capital:** {country_data.get('capital', ['N/A'])[0]}")
                            st.write(f"**Region:** {country_data.get('region', 'N/A')}")
                            st.write(f"**Population:** {country_data.get('population', 'N/A'):,}")
                            st.write(f"**Area:** {country_data.get('area', 'N/A'):,} sq km")
