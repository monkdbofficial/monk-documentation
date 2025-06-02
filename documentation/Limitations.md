# Limitations of MonkDB

## Note

MonkDB is designed for horizontally scalable, distributed SQL (OLAP) on large volumes of structured, semi-structured or unstructured data. To achieve high performance and scalability, especially on distributed nodes, MonkDB omits some traditional relational database features that are hard to implement efficiently in distributed systems.

If you need strict relational integrity or procedural logic inside the database, a traditional RDBMS like PostgreSQL may be more suitable. However, please note that databases like PostgreSQL, MySQL, and the likes are OLAP databases whose purposes are different when compared with OLAP databases. 

The below section aims to list out complete set limitations of MonkDB to root out wrong expectations.

- MonkDB is an OLAP database and **not** an OLTP database. It is neither a HTAP database. It is an OLAP database fronted by a PgWire interface.
- **Stored Procedures**- Stored procedures are precompiled collections of SQL statements stored in the database. They can be executed repeatedly, often used to encapsulate business logic, reduce client-server communication, and improve performance. MonkDB does not support stored procedures. Instead, logic should be implemented at the application layer or via custom functions using external tools (like Python or Java apps).
- **Triggers**- Triggers are automatic actions executed in response to certain events on a table (e.g., `INSERT`, `UPDATE`, `DELETE`). They’re often used for auditing, validation, or automation. MonkDB does not support triggers. Any reactive logic must be managed by the application or through external stream processing (like Kafka).
- **Sequences**- Sequences generate a series of unique numeric values, commonly used for auto-incrementing primary keys. MonkDB does not support sequences. Instead, you can rely on client-side logic for generating unique values.
- **Table Inheritance**- Table inheritance allows one table to inherit columns from another table, useful for object-relational mapping and polymorphic queries. MonkDB does not support table inheritance. All tables must be defined independently, and shared fields must be duplicated or handled in application logic.
- **Constraints**- MonkDB lacks several types of data integrity constraints that are standard in SQL databases.
    - **Unique Constraints**- They ensure that values in a column or set of columns are unique across rows. MonkDB does not enforce uniqueness constraints, even if you define them, they end being ignored. Uniqueness must be maintained at the application level.
    - **Foreign Key Constraints**- This is used to ensure referential integrity between tables, i.e., values in one table must match those in another. MonkDB does not support foreign keys. Relationships must be managed manually or by application logic. 
        - Moreover, FK constraints are apt for OLTP databases and OLAP databases as the underlying architecture is completely different. Syncing FK relationsips across a distributed cluster having multiple nodes will be heavy resource intensive operation and directly affects latency. Hence, MonkDB doesn't support FK constraints.
    - **Exclusion Constraints**- It prevents rows from having overlapping values in specified columns, often used with geometric or range types. These constraints are not supported. There’s no native way to enforce exclusivity beyond simple value matching.
- In many traditional relational databases (especially PostgreSQL), network address types such as `inet` and `cidr` are supported. These types allow you to store and manipulate IP addresses and network blocks directly in SQL. Functions and operators on these types include:
    - Comparison of IP addresses
    - Checking if an IP belongs to a subnet
    - Bitwise operations on IPs
    - Conversion between formats (e.g., text to inet)
    - Network math (e.g., incrementing addresses)
MonkDB does not support these network-specific data types (`inet`, `cidr`) or the related functions and operators. This means you cannot natively store an IP address as a special network type—only as a string (e.g., '192.168.0.1'). You cannot use network operators like:
    - << (contains)
    - >> (is contained by)
    - ~ (bitwise NOT)
    - & (bitwise AND)
    - Functions like `inet_same_family()`, `inet_merge()`, or `host()`
Instead, any logic involving IP addresses must be done manually in application code.
- A **set-returning function (SRF)** is a type of SQL function that returns multiple rows (a set of rows) instead of just a single scalar value. This is in contrast to standard SQL functions, which typically return a single value (e.g., `LENGTH('hello') → 5`). MonkDB does not support SRFs which means
    - You cannot write or use functions that return multiple rows.
    - You cannot expand arrays or JSON arrays into rows using SQL alone.
    - You cannot use PostgreSQL-like SRFs such as `unnest()`, `generate_series()`, `json_array_elements()`.
MonkDB encourages a flattened, document-style data model (like in Elasticsearch), where nested data is either kept as arrays and filtered via scalar functions, or flattened and normalized before ingestion.
- A trigger function is a special kind of function that is automatically executed (or "triggered") in response to certain events on a table. Trigger functions are called by a trigger, and they are used to define the logic that should run when a trigger fires. In PostgreSQL, for example, you create a trigger function using `CREATE FUNCTION` with a special signature, then bind it to a trigger using `CREATE TRIGGER`. MonkDB does not support trigger functions which means 
    - You cannot define trigger functions or use triggers at all.
    - There is no native mechanism to automatically run logic inside MonkDB when data changes.
    - Event-driven workflows must be managed outside of MonkDB. For example, Apache Kafka, Apache Pulsar, Debezium, and the likes.
Triggers, which involve row-level logic can *reduce performance in distributed systems*, *complicate parallel inserts/updates*, and *add complexity for distributed consistency*.
- **XML functions** in SQL are built-in functions and operators used to store, query, generate, and manipulate XML data. These functions are common in traditional relational databases like PostgreSQL, Oracle, and SQL Server, which support the XML data type and allow working with structured XML documents directly in SQL. MonkDB does not support XML functions, and it means
    - MonkDB does not support the XML data type.
    - It does not include any XML-related functions, operators, or XPath querying.
    - You cannot parse, generate, or query XML within MonkDB's SQL layer.
    - XML data may be treated as a plain string (`TEXT`), without structure awareness.
However, you may use client-side XML handling or convert XMLs to JSON based structures and leverage `OBJECT` data type of MonkDB that handles JSON workloads. 
- In traditional OLTP (Online Transaction Processing) databases like PostgreSQL, MySQL, or Oracle, transaction control is a foundational feature. It allows you to group multiple operations into a single atomic unit using commands like `BEGIN`, `COMMIT`, `ROLLBACK`. These ensure ACID compliance on the data involved. However, MonkDB is designed for analytical workloads, not transactional ones. Therefore,
    - No `BEGIN`, `COMMIT`, or `ROLLBACK`. Even if these are applied, there won't be any effect.
    - No multi-statement atomic operations.
    - Every SQL statement is auto-committed immediately
    - Changes are replicated across the cluster for durability and availability.
- This nature allows MonkDB to *high write throughput*, *scalability across nodes*, *better performance for OLAP*. However, please note that every row in MonkDB includes a hidden version number that is automatically:
    - Initialized when the row is created
    - Incremented each time the row is updated
This version number can be used to detect changes between reads and writes, which is the key to optimistic concurrency control. Optimistic Concurrency Control is a method to prevent conflicts in concurrent updates without locking rows. It works on the assumption that most updates won’t conflict. So you can *read the data and remember its version*, *modify the data*, *update the row only if the version hasn’t changed, *abort or retry if another process modified it first*.
- In traditional relational databases, system information tables (often found in the `INFORMATION_SCHEMA`) are read-only views into the metadata of the database. These tables let you query things like:
    - Available tables and columns
    - Index definitions
    - User privileges
    - Data types
    - Constraints
    - Storage engine details
These schemas are part of the SQL standard and are used for introspection understanding the structure of the database. MonkDB offers read-only system tables and an information schema, but with some important differences:
- MonkDB's `information_schema`
    - Follows the SQL standard partially, with modifications and extensions. Provides metadata about:
        - Tables, columns, constraints
        - Indexes
        - Schemas and catalogs
        - Views
- MonkDB's `sys` schema
    - MonkDB-specific, read-only schema. Offers real-time information on the cluster's internal state, including:
        - Nodes
        - Shards
        - Tables
        - Jobs (queries)
        - Health metrics
        - Cluster-wide statistics
        - Licenses information_schema
- MonkDB extends the typical SQL introspection model to support distributed and analytical workloads. Here’s a refined comparison
| Area                               | Standard SQL (Traditional RDBMS)              | MonkDB                                                      |
|-------------------------------------|-----------------------------------------------|--------------------------------------------------------------|
| Compliance with INFORMATION_SCHEMA  | High — follows ANSI/ISO SQL                   | Partial — adapted for MonkDB's distributed engine           |
| Schema structure                    | Flat, relational metadata only                | Adds `sys` schema for cluster-level and shard visibility     |
| Cluster statistics                  | ❌ Not available                              | ✅ Real-time data in `sys.nodes`, `sys.jobs`, `sys.cluster`, etc. |
| Shards and nodes                    | ❌ Not applicable in centralized DBs           | ✅ First-class entities (e.g., `sys.shards`, `sys.nodes`)    |
| Query/job visibility                | Limited or external tools (e.g., `pg_stat_activity`) | ✅ Native in `sys.jobs` and `sys.jobs_log`                  |
| License info                        | Usually external tooling                      | ✅ `sys.license` provides built-in access                    |
