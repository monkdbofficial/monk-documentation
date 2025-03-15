import random
from monkdb import client
from shapely.geometry import Polygon, MultiPoint, LineString, MultiLineString, MultiPolygon, Point
from shapely.ops import unary_union

# Function to generate random points


def generate_random_point():
    return [round(random.uniform(-50, 50), 6), round(random.uniform(-50, 50), 6)]

# Function to generate a valid convex polygon


def generate_valid_convex_polygon(num_points=4):
    while True:
        coords = [generate_random_point() for _ in range(num_points)]
        poly = Polygon(coords).convex_hull  # Ensures convexity
        if poly.is_valid:
            return list(poly.exterior.coords)

# Function to generate various GeoJSON-compatible shapes


def generate_geo_shape(shape_type):
    if shape_type == "Point":
        shape = Point(generate_random_point())

    elif shape_type == "MultiPoint":
        shape = MultiPoint([Point(generate_random_point()) for _ in range(3)])

    elif shape_type == "LineString":
        shape = LineString([generate_random_point() for _ in range(4)])

    elif shape_type == "MultiLineString":
        shape = MultiLineString([
            LineString([generate_random_point() for _ in range(3)]),
            LineString([generate_random_point() for _ in range(3)])
        ])

    elif shape_type == "Polygon":
        coords = generate_valid_convex_polygon()
        shape = Polygon(coords)

    elif shape_type == "MultiPolygon":
        # Generate two valid polygons that do not overlap
        while True:
            poly1 = Polygon(generate_valid_convex_polygon())
            poly2 = Polygon(generate_valid_convex_polygon())

            if poly1.is_valid and poly2.is_valid and poly1.disjoint(poly2):
                break  # Only exit the loop if the polygons do not overlap

        shape = MultiPolygon([poly1, poly2])

    elif shape_type == "GeometryCollection":
        shape = unary_union([
            Point(generate_random_point()),
            LineString([generate_random_point() for _ in range(3)]),
            Polygon(generate_valid_convex_polygon())
        ])

    if not shape.is_valid:
        raise ValueError(f"Invalid shape generated for {shape_type}")

    return shape.__geo_interface__  # Convert to GeoJSON-compatible format


# Database Connection Details
DB_HOST = "xx.xx.xx.xxx"
DB_PORT = "4200"
DB_USER = "testuser"
DB_PASSWORD = "testpassword"
DB_SCHEMA = "monkdb"

# Connect to MonkDB
connection = client.connect(
    f"http://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}", username=DB_USER
)
cursor = connection.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.geo_shapes (
    id INTEGER PRIMARY KEY,
    area GEO_SHAPE
) WITH (number_of_replicas = 0);
""")
print(f"Table '{DB_SCHEMA}.geo_shapes' has been created.")

# Insert Synthetic Data for All GEO_SHAPE Types
geo_shape_types = ["Point", "MultiPoint", "LineString",
                   "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection"]

for i, shape_type in enumerate(geo_shape_types, start=1):
    try:
        shape_data = generate_geo_shape(shape_type)
        cursor.execute(
            f"INSERT INTO {DB_SCHEMA}.geo_shapes (id, area) VALUES (?, ?)",
            (i, shape_data),
        )
        print(
            f"Inserted {shape_type} with ID {i}: {shape_data} in {DB_SCHEMA}.")
    except Exception as e:
        print(f"Error inserting {shape_type} with ID {i}: {e}")

# Commit Changes
connection.commit()

# Query Data - Fetch All Inserted Shapes
cursor.execute(f"SELECT * FROM {DB_SCHEMA}.geo_shapes;")
geo_shapes = cursor.fetchall()
print("\nGeo Shapes:")
for row in geo_shapes:
    print(row)

# Close Connection
cursor.close()
connection.close()
