from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class WeatherLog(Base):
    __tablename__ = 'weather_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)
    cloudiness = Column(Float)
    weather_condition = Column(String(100))
    searched_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserActivity(Base):
    __tablename__ = 'user_activity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_ip = Column(String(50))
    search_query = Column(String(200))
    country = Column(String(100))
    city = Column(String(100))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class WeatherForecast(Base):
    __tablename__ = 'weather_forecast'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100))
    forecast_date = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    weather_condition = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
