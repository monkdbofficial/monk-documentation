from monkdb import client

DB_HOST = "xx.xx.xx.xxx"  # Your instance IP address
DB_PORT = "4200"  # Default MonkDB port for HTTP connectivity.
DB_USER = "testuser"
DB_PASSWORD = "testpassword"
TABLE_NAME = "blobs_demo"

connection = client.connect(
    f"http://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}", username=DB_USER)
cursor = connection.cursor()

# Create a BLOB table
# BLOB tables in MonkDB do not support schemas. Unlike regular tables, BLOB tables exist at the cluster level and are not associated with a schema (such as doc, myschema, etc.).
cursor.execute(f"""
    CREATE BLOB TABLE {TABLE_NAME}
    CLUSTERED INTO 3 SHARDS
""")

print(f"BLOB table {TABLE_NAME} created successfully!")
connection.close()
