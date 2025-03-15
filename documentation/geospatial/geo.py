import random
from monkdb import client

# MonkDB Connection Details
DB_HOST = "44.222.211.123"  # Your instance IP address (that's reachable)
DB_PORT = "4200"  # Default MonkDB port for HTTP connectivity.
DB_USER = "testuser"
DB_PASSWORD = "testpassword"
DB_SCHEMA = "monkdb"

# Create a connection
connection = client.connect(
    f"http://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}", username=DB_USER)
cursor = connection.cursor()

# Create Tables
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.geo_points (
    id INTEGER PRIMARY KEY,
    location GEO_POINT
) WITH (number_of_replicas = 0);
""")
print(f"Table '{DB_SCHEMA}.geo_points' has been created.")

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.geo_shapes (
    id INTEGER PRIMARY KEY,
    area GEO_SHAPE
) WITH (number_of_replicas = 0);
""")
print(f"Table '{DB_SCHEMA}.geo_shapes' has been created.")

# Insert Synthetic Data
num_points = 10
num_shapes = 5

# Insert GEO_POINT data
for i in range(1, num_points + 1):
    lon, lat = round(random.uniform(-180, 180),
                     6), round(random.uniform(-90, 90), 6)
    cursor.execute(
        f"INSERT INTO {DB_SCHEMA}.geo_points (id, location) VALUES (?, ?)", (i, [lon, lat]))
    print(f"Inserted point ID {i} at location [{lon}, {lat}] in {DB_SCHEMA}.")

# Insert GEO_SHAPE data using WKT format
for i in range(1, num_shapes + 1):
    # Generate valid polygon coordinates within valid ranges
    coords = [
        [round(random.uniform(-50, 50), 6), round(random.uniform(-50, 50), 6)]
        for _ in range(4)
    ]
    # Ensure the polygon is closed by repeating the first coordinate
    coords.append(coords[0])

    # Create WKT string for the polygon
    wkt_polygon = f'POLYGON ((' + \
        ', '.join([f"{lon} {lat}" for lon, lat in coords]) + '))'

    try:
        # Insert into CrateDB as a WKT string
        cursor.execute(
            f"INSERT INTO {DB_SCHEMA}.geo_shapes (id, area) VALUES (?, ?)",
            (i, wkt_polygon)
        )
        print(f"Inserted shape ID {i} with WKT: {wkt_polygon} in {DB_SCHEMA}.")
    except Exception as e:
        print(f"Error inserting shape ID {i}: {e}")

# Query Data - Fetch all points and shapes
cursor.execute(f"SELECT * FROM {DB_SCHEMA}.geo_points;")
geo_points = cursor.fetchall()
print("\nGeo Points:")
for row in geo_points:
    print(row)

cursor.execute(f"SELECT * FROM {DB_SCHEMA}.geo_shapes;")
geo_shapes = cursor.fetchall()
print("\nGeo Shapes:")
for row in geo_shapes:
    print(row)

# Example Spatial Query - Find points within a polygon using WKT syntax
polygon_wkt = 'POLYGON ((-10 -10, 10 -10, 10 10, -10 10, -10 -10))'
cursor.execute(f"""
    SELECT id, location FROM {DB_SCHEMA}.geo_points
    WHERE within(location, ?);
""", (polygon_wkt,))
print("\nPoints within given polygon:")
for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
connection.close()
