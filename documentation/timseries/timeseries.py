import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Float, TIMESTAMP
from datetime import datetime
import random

# Define the database URI (replace <username>, <password>, <host>, and <port> with your details)
DB_URI = "monkdb://testuser:testpassword@172.31.30.33:4200"

# Create an SQLAlchemy engine using monk-orm
engine = sa.create_engine(DB_URI, echo=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define the base for ORM models
Base = declarative_base()

# Define the ORM model for sensor_data (matches the created table schema)


class SensorData(Base):
    __tablename__ = "sensor_data"
    # Primary key for time series data
    timestamp = Column(TIMESTAMP(timezone=True), primary_key=True)
    location = Column(String, nullable=False)  # Location of the sensor
    # Temperature reading in Celsius
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)  # Humidity percentage
    wind_speed = Column(Float, nullable=False)  # Wind speed in km/h

# Function to insert sample data into the table


def insert_sample_data():
    now = datetime.now()
    data_points = [
        SensorData(
            timestamp=now,
            location="Station A",
            temperature=round(random.uniform(-10, 40), 2),
            humidity=round(random.uniform(30, 90), 2),
            wind_speed=round(random.uniform(0, 20), 2),
        )
        for _ in range(10)
    ]
    session.add_all(data_points)
    session.commit()

# Function to query and display data from the table


def query_data():
    results = session.query(SensorData).all()
    for row in results:
        print(f"{row.timestamp}, {row.location}, {row.temperature}°C, {row.humidity}%, {row.wind_speed} km/h")


# Run the functions to demonstrate functionality
insert_sample_data()
query_data()
