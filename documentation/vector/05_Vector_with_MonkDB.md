# Working with Vector Workloads Using MonkDB

## Simulation

In this demo, we are working with synthetic documents that would be embedded using a model and finally upserting the data into MonkDB.

We are executing `knn_match` to perform **KNN** and `vector_similarity` to perform **Similarity Search** on the upserted documents.

The steps followed in the scripted simulation are:

- Define database connection variables. 
- Connect to MonkDB. This creates a connection to the MonkDB instance. It opens a cursor for executing SQL queries.
- Load `sentence-transformer` model from huggingface. You may use an alternative to sentence transformer to embed text data such as `Cohere`, `OpenAI`, etc. The model which we have used in sentence transformers leverage 384 dimensions. The quality/accuracy of those dimensions would be low when compared with models that support 2048 dimensions. Hence, as mentioned before, use embedding and infer model based on your needs.
- Create a table in MonkDB if not already created. This will store the generated vector floats (embeddings) for downstream querying.
- The table that we have created has `id`, `context` and `embedding` columns. You may create tables according to your need.
- We are following the `upsert` approach. Vectors are inserted, and if it is an old document which is being inserted again, we are updating the entry. Otherwise, we would be bricked with `DuplicateKey` exception from MonkDB on data conflicts. It ensures duplicates are not inserted into the database.
- We have added five sample documents. 
- We are performing `knn_match` to find the top k nearest documents based on the vector embedding similarity. Here, we have utilized MonkDB's `knn_match` function.
- Next, we are finding similar documents using MonkDB's `vector_similarity()` function, which computes Euclidean distance. **Please note that we don't support cosine similarity and dot product as on today. They are in our roadmap.**
- In the next step, we are extending `VectorStore` class from LangChain.
- We then insert documents using LangChain and ensure duplicates are not inserted by passing `ON CONFLICT DO UPDATE` argument to the SQL statement.
- Search using LangChain
- Initialize LangChain vector store. This creates a MonkDB vector store and inserts sample documents.
- Retrieves similar documents using LangChain.

A user will receive a below output upon executing the [vector script](vector_ops.py).

```zsh  
✅ Table 'monkdb.documents' is ready.
Upserted document: doc_1
Upserted document: doc_2
Upserted document: doc_3
Upserted document: doc_4
Upserted document: doc_5
✅ Documents inserted into monkdb.documents.

🔍 KNN Search Results:
ID: doc_2, Content: Vector search in databases is important for AI applications., Score: 0.7389452
ID: doc_4, Content: Machine learning models can benefit from vector databases., Score: 0.59701025
ID: doc_1, Content: MonkDB is great for time-series and vector workloads., Score: 0.45875195
ID: doc_3, Content: MonkDB provides scalable distributed storage., Score: 0.39378193

🔍 Similarity Search Results:
ID: doc_2, Content: Vector search in databases is important for AI applications., Similarity: 0.7389452
ID: doc_4, Content: Machine learning models can benefit from vector databases., Similarity: 0.59701025
ID: doc_1, Content: MonkDB is great for time-series and vector workloads., Similarity: 0.45875195

🔍 LangChain Similarity Search Results:
MonkDB supports fast vector search.
Vector search in databases is important for AI applications.
MonkDB is great for time-series and vector workloads.

✅ MonkDB vector search with Sentence Transformers & LangChain completed successfully under schema 'monkdb'!
```
