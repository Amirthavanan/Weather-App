import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .models import Base, WeatherLog, UserActivity, WeatherForecast

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "weather_dashboard")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

try:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Error connecting to MySQL: {e}. Falling back to SQLite.")
    engine = create_engine("sqlite:///./weather_fallback.db")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def log_search(db, query, country, city, ip="127.0.0.1"):
    activity = UserActivity(user_ip=ip, search_query=query, country=country, city=city)
    db.add(activity)
    db.commit()

def log_weather(db, weather_data):
    log = WeatherLog(**weather_data)
    db.add(log)
    db.commit()

def log_forecast(db, forecast_data_list):
    for data in forecast_data_list:
        forecast = WeatherForecast(**data)
        db.add(forecast)
    db.commit()
