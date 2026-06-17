import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_db
from database.models import WeatherLog

st.set_page_config(page_title="Weather Analytics", page_icon="📊", layout="wide")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("assets/style.css")

st.title("📊 Search & Weather Analytics")

db = get_db()
logs = db.query(WeatherLog).all()

if logs:
    df = pd.DataFrame([{
        "city": log.city,
        "country": log.country,
        "temperature": log.temperature,
        "humidity": log.humidity,
        "searched_at": log.searched_at
    } for log in logs])
    
    st.subheader("Data Overview")
    st.dataframe(df.tail(10), use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        city_counts = df['city'].value_counts().reset_index()
        city_counts.columns = ['city', 'count']
        fig_cities = px.pie(city_counts, names='city', values='count', title="Most Searched Cities", hole=0.4)
        st.plotly_chart(fig_cities, use_container_width=True)
        
    with col2:
        avg_temp = df.groupby('city')['temperature'].mean().reset_index()
        fig_temp = px.bar(avg_temp, x='city', y='temperature', title="Average Temperature by City (°C)", color='temperature', color_continuous_scale='bluered')
        st.plotly_chart(fig_temp, use_container_width=True)
        
    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='weather_analytics.csv',
        mime='text/csv',
        use_container_width=True
    )
else:
    st.info("No analytics data available yet. Try searching for some cities first!")
