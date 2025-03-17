from monkdb import client
import json

# MonkDB Connection Details
DB_HOST = "44.222.211.123"  # Replace with your instance IP address
DB_PORT = "4200"  # Default MonkDB port for HTTP connectivity
DB_USER = "testuser"
DB_PASSWORD = "testpassword"
DB_SCHEMA = "monkdb"
TABLE_NAME = "doc_json"

# Create a connection
connection = client.connect(
    f"http://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}", username=DB_USER
)
cursor = connection.cursor()

# Drop table if exists
cursor.execute(f"DROP TABLE IF EXISTS {DB_SCHEMA}.{TABLE_NAME}")
print(f"Dropped {DB_SCHEMA}.{TABLE_NAME} table")

# Create Table with JSON Object Storage
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.{TABLE_NAME} (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        metadata OBJECT(DYNAMIC)  -- JSON-like storage
    )""")
connection.commit()

# Insert Synthetic Data
users_data = [
    (1, "Alice", 30, {"city": "New York", "skills": ["Python", "SQL"]}),
    (2, "Bob", 25, {"city": "Berlin", "skills": ["Java", "AI"]}),
    (3, "Charlie", 35, {"city": "San Francisco",
     "profile": {"preferences": {"food": "Sushi"}}}),
]

for user in users_data:
    cursor.execute(
        f"INSERT INTO {DB_SCHEMA}.{TABLE_NAME} (id, name, age, metadata) VALUES (?, ?, ?, ?)", user)
connection.commit()

# Query Nested JSON Fields
cursor.execute(f"SELECT name, metadata['city'] FROM {DB_SCHEMA}.{TABLE_NAME}")
print("\nUsers and their Cities:")
print(json.dumps(cursor.fetchall(), indent=4))

# Query Using JSON Key Filtering
cursor.execute(
    f"SELECT * FROM {DB_SCHEMA}.{TABLE_NAME} WHERE metadata['city'] = 'New York'")
print("\nUsers from New York:")
print(json.dumps(cursor.fetchall(), indent=4))

# Query Nested Object Data
cursor.execute(
    f"SELECT name, metadata['profile']['preferences']['food'] FROM {DB_SCHEMA}.{TABLE_NAME} WHERE metadata['profile']['preferences']['food'] IS NOT NULL")
print("\nUsers with Food Preferences:")
print(json.dumps(cursor.fetchall(), indent=4))

# Query JSON Object Keys Dynamically
cursor.execute(
    f"SELECT name, object_keys(metadata) FROM {DB_SCHEMA}.{TABLE_NAME}")
print("\nUsers and Their JSON Keys:")
print(json.dumps(cursor.fetchall(), indent=4))

# Close connection
cursor.close()
connection.close()
