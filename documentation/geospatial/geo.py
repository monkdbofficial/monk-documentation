import random
from monkdb import client
from shapely.geometry import Polygon, MultiPoint
from shapely.validation import explain_validity

# Function to generate a valid convex polygon using Shapely's convex hull


def generate_valid_convex_polygon(num_points=4):
    """Generates a convex polygon using Shapely's convex hull to ensure validity."""
    while True:
        coords = [
            [round(random.uniform(-50, 50), 6),
             round(random.uniform(-50, 50), 6)]
            for _ in range(num_points)
        ]
        multipoint = MultiPoint(coords)
        poly = multipoint.convex_hull  # Creates a convex polygon

        if poly.is_valid:
            break  # Only return if the polygon is valid

    coords = list(poly.exterior.coords)  # Extract WKT-compatible coords
    return coords


# MonkDB Connection Details
DB_HOST = "44.222.211.123"  # Replace with your instance IP address
DB_PORT = "4200"  # Default MonkDB port for HTTP connectivity
DB_USER = "testuser"
DB_PASSWORD = "testpassword"
DB_SCHEMA = "monkdb"

# Create a connection
connection = client.connect(
    f"http://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}", username=DB_USER
)
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
        f"INSERT INTO {DB_SCHEMA}.geo_points (id, location) VALUES (?, ?)",
        (i, [lon, lat]),
    )
    print(f"Inserted point ID {i} at location [{lon}, {lat}] in {DB_SCHEMA}.")

# Insert GEO_SHAPE data using WKT format
for i in range(1, num_shapes + 1):
    # Generate a valid convex polygon
    coords = generate_valid_convex_polygon()

    # Convert to WKT format
    wkt_polygon = f'POLYGON ((' + \
        ', '.join([f"{lon} {lat}" for lon, lat in coords]) + '))'

    try:
        cursor.execute(
            f"INSERT INTO {DB_SCHEMA}.geo_shapes (id, area) VALUES (?, ?)",
            (i, wkt_polygon),
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
cursor.execute(
    f"""
    SELECT id, location FROM {DB_SCHEMA}.geo_points
    WHERE within(location, ?);
""",
    (polygon_wkt,),
)
print("\nPoints within given polygon:")
for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
connection.close()
