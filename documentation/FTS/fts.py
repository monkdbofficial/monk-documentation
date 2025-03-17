from monkdb import client
import random
import time

# MonkDB Connection Details
DB_HOST = "44.222.211.123"  # Replace with your instance IP address
DB_PORT = "4200"  # Default MonkDB port for HTTP connectivity
DB_USER = "testuser"
DB_PASSWORD = "testpassword"
DB_SCHEMA = "monkdb"
TABLE_NAME = "fts_demo"

# Create a connection
connection = client.connect(
    f"http://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}", username=DB_USER
)
cursor = connection.cursor()

# Drop table if exists
cursor.execute(f"DROP TABLE IF EXISTS {DB_SCHEMA}.{TABLE_NAME}")
connection.commit()

# Create table with a full-text index using the standard analyzer
cursor.execute(f'''
CREATE TABLE {DB_SCHEMA}.{TABLE_NAME} (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT INDEX USING FULLTEXT WITH (analyzer = 'standard')
)
''')
connection.commit()

# Generate synthetic data
titles = ["Machine Learning", "Deep Learning",
          "AI Ethics", "Vector Databases", "Big Data Analytics"]
contents = [
    "Machine learning algorithms power modern AI applications.",
    "Deep learning revolutionized image recognition and NLP.",
    "Ethical considerations in AI are crucial for fairness and bias mitigation.",
    "Vector databases optimize similarity search for high-dimensional data.",
    "Big data analytics transforms decision-making in businesses."
]

# Insert synthetic data (ensuring unique entries)
data = [(i, titles[i % len(titles)], contents[i % len(contents)])
        for i in range(1, 11)]
cursor.executemany(
    f"INSERT INTO {DB_SCHEMA}.{TABLE_NAME} (id, title, content) VALUES (?, ?, ?)", data)
connection.commit()

# Refresh the table to ensure changes are reflected in the index
cursor.execute(f"REFRESH TABLE {DB_SCHEMA}.{TABLE_NAME}")

time.sleep(1)  # Ensure data is indexed before querying

# GROUP BY content, title ensures each content value appears only once. Before, multiple rows for the same content could exist, leading to duplicate processing.
# Used MAX(_score) to Select the Highest Score. It finds the highest _score per unique content. This guarantees that only the most relevant version of the content appears.
# This ensures the most relevant results appear at the top.
search_term = "AI"
cursor.execute(f"""
SELECT title, content, MAX(_score) as max_score
FROM {DB_SCHEMA}.{TABLE_NAME}
WHERE MATCH(content, ?)
GROUP BY content, title
ORDER BY max_score DESC;
""", (search_term,))

# Fetch results
results = cursor.fetchall()

# Print unique results
for title, content, score in results:
    print(f"Title: {title}, Content: {content}, Score: {score}")


# Close connection
cursor.close()
connection.close()
