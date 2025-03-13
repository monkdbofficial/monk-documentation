import asyncio
from monkdb import client
from datetime import datetime
import random

# Database connection details
DB_URI = "http://xx.xx.xx.xxx:4200"
DB_USER = "testuser"
DB_PASSWORD = "testpassword"

# Connect to MonkDB
connection = client.connect(DB_URI, username=DB_USER, password=DB_PASSWORD)

# Generate random weather data


def generate_weather_data(location):
    return {
        "timestamp": datetime.utcnow(),
        "location": location,
        "temperature": round(random.uniform(-10, 40), 2),
        "humidity": round(random.uniform(20, 100), 2),
        "wind_speed": round(random.uniform(0, 20), 2),
    }

# Insert data into MonkDB and execute queries


async def insert_data():
    locations = ["New York", "London", "Berlin", "Tokyo"]
    while True:
        cursor = connection.cursor()
        try:
            # Insert data for each location
            for location in locations:
                data = generate_weather_data(location)
                query = """
                    INSERT INTO monkdb.sensor_data (timestamp, location, temperature, humidity, wind_speed)
                    VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(query, [data["timestamp"], data["location"],
                               data["temperature"], data["humidity"], data["wind_speed"]])
                print(f"Inserted: {data}")

            # Example Query 1: Average temperature per location
            cursor.execute(
                "SELECT location, AVG(temperature) AS avg_temp FROM monkdb.sensor_data GROUP BY location")
            avg_temps = cursor.fetchall()
            print("\nAverage Temperatures:")
            for row in avg_temps:
                print(f"Location: {row[0]}, Avg Temp: {row[1]}")

            # Example Query 2: Retrieve recent readings
            cursor.execute(
                "SELECT * FROM monkdb.sensor_data ORDER BY timestamp DESC LIMIT 5")
            recent_readings = cursor.fetchall()
            print("\nRecent Readings:")
            for row in recent_readings:
                print(
                    f"Timestamp: {row[0]}, Location: {row[1]}, Temperature: {row[2]}, Humidity: {row[3]}, Wind Speed: {row[4]}")

        finally:
            # Close the cursor explicitly
            cursor.close()

        await asyncio.sleep(5)  # Wait for 5 seconds before the next batch

# Main async function to run the simulation


async def main():
    try:
        await insert_data()
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        connection.close()

# Run the async simulation
if __name__ == "__main__":
    asyncio.run(main())
