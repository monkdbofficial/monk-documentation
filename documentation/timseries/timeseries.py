from monkdb import client
import random
from faker import Faker
from datetime import datetime, timedelta

# MonkDB Connection Details
DB_HOST = "44.222.211.123"
DB_PORT = "4200"  # Default MonkDB port for HTTP connectivity.
DB_USER = "testuser"
DB_PASSWORD = "testpassword"

# Create a connection
connection = client.connect(
    f"http://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}", username=DB_USER)
cursor = connection.cursor()

# Faker for generating locations
fake = Faker()

# Generate and Insert Time-Series Data


def insert_sensor_data(num_rows=10):
    base_time = datetime.utcnow()

    for _ in range(num_rows):
        timestamp = base_time - timedelta(minutes=random.randint(1, 1440))
        location = fake.city()
        temperature = round(random.uniform(10, 40), 2)
        humidity = round(random.uniform(20, 90), 2)
        wind_speed = round(random.uniform(0, 30), 2)

        query = """
        INSERT INTO monkdb.sensor_data (timestamp, location, temperature, humidity, wind_speed) 
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (timestamp, location,
                       temperature, humidity, wind_speed))

    connection.commit()
    print(f"Inserted {num_rows} sensor records.")

# Query Time-Series Data


def fetch_sensor_data():
    query = """
    SELECT timestamp, location, temperature, humidity, wind_speed 
    FROM monkdb.sensor_data 
    WHERE timestamp >= NOW() - INTERVAL '1 day'
    ORDER BY timestamp ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print("No recent data found.")
        return

    print("\nRecent Sensor Data (Last 24 Hours):")
    for row in rows:
        print(
            f"{row[0]} | {row[1]} | Temp: {row[2]}°C | Humidity: {row[3]}% | Wind Speed: {row[4]} km/h")


# Run the functions
insert_sensor_data(10)
fetch_sensor_data()

# Close connection
cursor.close()
connection.close()
