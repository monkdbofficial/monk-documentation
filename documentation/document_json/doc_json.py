from monkdb import client
import json

# MonkDB Connection Details
DB_HOST = "xx.xx.xx.xxx"  # Replace with your instance IP address
DB_PORT = "4200"  # Default MonkDB port for HTTP connectivity
DB_USER = "testuser"
DB_PASSWORD = "testpassword"
DB_SCHEMA = "monkdb"
TABLE_NAME = "doc_json"

# Create a MonkDB connection
connection = client.connect(
    f"http://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}", username=DB_USER
)
cursor = connection.cursor()

# Drop table if exists
cursor.execute(f"DROP TABLE IF EXISTS {DB_SCHEMA}.{TABLE_NAME}")
print(f"Dropped {DB_SCHEMA}.{TABLE_NAME} table")

# Create table with JSON storage and indexing
cursor.execute(f"""
    CREATE TABLE {DB_SCHEMA}.{TABLE_NAME} (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        metadata OBJECT(DYNAMIC) AS (
            city TEXT INDEX USING PLAIN
        )
    )
""")

print("✅ Table created successfully!")

# Insert sample users with nested JSON
users_data = [
    (1, "Alice", 30, {
        "city": "New York",
        "skills": ["Python", "SQL", "AI"],
        "profile": {
            "preferences": {
                "food": "Italian",
                "language": "English"
            }
        }
    }),
    (2, "Bob", 25, {
        "city": "San Francisco",
        "skills": ["JavaScript", "Node.js"],
        "profile": {
            "preferences": {
                "food": "Mexican",
                "language": "Spanish"
            }
        }
    }),
    (3, "Charlie", 35, {
        "city": "Berlin",
        "skills": ["Go", "Rust"],
        "profile": {}  # Empty profile (No food preference)
    }),
    (4, "David", 28, {
        "city": "London",
        "skills": ["Java", "Spring Boot"],
    }),
    (5, "Eve", 40, {
        "city": "Tokyo",
        "skills": ["AI", "Machine Learning"],
        "profile": {
            "preferences": {
                "food": "Sushi",
                "language": "Japanese"
            }
        }
    })
]

# Insert data
try:
    cursor.executemany(
        f"INSERT INTO {DB_SCHEMA}.{TABLE_NAME} (id, name, age, metadata) VALUES (?, ?, ?, ?)", users_data)
    connection.commit()  # ✅ Ensure the transaction is committed
    print("✅ Sample user data inserted successfully!")
except Exception as e:
    print(f"⚠️ Error during data insertion: {e}")

# ✅ Refresh table to ensure visibility of inserted records
cursor.execute(f"REFRESH TABLE {DB_SCHEMA}.{TABLE_NAME}")

# Fetch the number of records after commit
cursor.execute(f"SELECT COUNT(*) FROM {DB_SCHEMA}.{TABLE_NAME}")
print("\n🔍 Number of records in table:")
print(json.dumps(cursor.fetchall(), indent=4))

# Fetch all data to verify insertion
cursor.execute(f"SELECT id, name, metadata FROM {DB_SCHEMA}.{TABLE_NAME}")
print("\n🔍 Full User Data:")
print(json.dumps(cursor.fetchall(), indent=4))

# Query JSON field (metadata['city'])
cursor.execute(f"SELECT name, metadata['city'] FROM {DB_SCHEMA}.{TABLE_NAME}")
print("\n🌍 Users and Their Cities:")
print(json.dumps(cursor.fetchall(), indent=4))

# Query array elements inside JSON
cursor.execute(
    f"SELECT name, metadata['skills'] FROM {DB_SCHEMA}.{TABLE_NAME} WHERE metadata['skills'] IS NOT NULL")
print("\n💡 Users with Skills:")
print(json.dumps(cursor.fetchall(), indent=4))

# Check if a user has 'AI' in their skills (Array Filtering using ANY)
cursor.execute(
    f"SELECT name FROM {DB_SCHEMA}.{TABLE_NAME} WHERE 'AI' = ANY(metadata['skills'])")
print("\n🧠 Users with AI Skills:")
print(json.dumps(cursor.fetchall(), indent=4))

# Query Nested Object Data (Fix for NULL food preference issue)
cursor.execute(f"""
    SELECT name, metadata['profile']['preferences']['food'] 
    FROM {DB_SCHEMA}.{TABLE_NAME}
    WHERE metadata['profile']['preferences']['food'] IS NOT NULL
""")
print("\n🍔 Users with Food Preferences:")
food_prefs = cursor.fetchall()
if food_prefs:
    print(json.dumps(food_prefs, indent=4))
else:
    print("⚠️ No users with food preferences found!")

# Query JSON keys dynamically
cursor.execute(
    f"SELECT name, object_keys(metadata) FROM {DB_SCHEMA}.{TABLE_NAME}")
print("\n🔑 JSON Keys for Each User:")
print(json.dumps(cursor.fetchall(), indent=4))

# Update JSON field (Partial JSON Update)
cursor.execute(
    f"UPDATE {DB_SCHEMA}.{TABLE_NAME} SET metadata['city'] = 'Paris' WHERE name = 'Alice'")
print("\n✏️ Updated Alice's City to Paris!")

# Verify the update
cursor.execute(
    f"SELECT name, metadata['city'] FROM {DB_SCHEMA}.{TABLE_NAME} WHERE name = 'Alice'")
print("\n✅ Alice's Updated City:")
print(json.dumps(cursor.fetchall(), indent=4))

# Close connection
cursor.close()
connection.close()
print("\n🚀 MonkDB JSON Store Simulation Completed Successfully!")
