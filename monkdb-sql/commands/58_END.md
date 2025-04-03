# MonkDB: `END` Statement

MonkDB does not support traditional transactions, as its focus is on scalable read/write performance and analytical capabilities rather than transactional use cases. Here's an expanded explanation of the `END` command and MonkDB's approach to transactions.

## SQL Statement

```sql
END [ WORK | TRANSACTION ]
```

## Description

The `END` statement in SQL is synonymous with `COMMIT`. In databases that support transactions, it marks the conclusion of a transaction and makes all changes permanent. However, in MonkDB:

- Transactions are not supported; thus, commands like `BEGIN`, `COMMIT`, and `ROLLBACK` are accepted for compatibility but are effectively ignored.
- The primary purpose of the `END` statement in MonkDB is to close all cursors without hold in the current session.

## Why MonkDB Doesn't Support Transactions

MonkDB prioritizes high performance, scalability, and ease of use for analytical workloads. Supporting transactions would significantly impact SQL performance. Instead:

- Every write operation is automatically committed and replicated across the cluster.
- MonkDB uses version numbers for rows to provide consistency. This allows for patterns like optimistic concurrency control (OCC), which can address some use cases requiring atomicity.

## Parameters

- `WORK | TRANSACTION`- Optional keywords. They have no effect.

## Alternatives for Transaction-like Behavior in MonkDB

For operations requiring transactional guarantees like **transfer X credits from User A to User B**, please follow the below:

- **Optimistic Concurrency Control (OCC)**: Use the `_version` system column to perform version-aware updates:

```sql
UPDATE accounts
SET balance = balance - 100
WHERE user_id = 'user_a' AND _version = 4;
```

If another process updated the row, the `_version` check fails and no row is updated.

- **Single Process Control**: Perform complex multi-step logic within one service/process to reduce race conditions.

- **Hybrid Approach**: Use MonkDB for analytics, logs, time series, and external transactional DB (like PostgreSQL) for things like money transfers.

## Examples

### Example 1. Basic Example: Committing a Transaction

```sql
BEGIN TRANSACTION;
INSERT INTO Customers (CustName, City, State, Country) 
VALUES ('John Doe', 'New York', 'NY', 'USA');
UPDATE Orders SET Product = 'Laptop' WHERE Id = 5;
END TRANSACTION;
```

This example begins a transaction, performs an `INSERT` and an `UPDATE`, and ends the transaction using `END TRANSACTION`. The changes are committed to the database.

### Example 2. Conditional Commit or Rollback

```sql
BEGIN TRANSACTION;
INSERT INTO Customers (CustName, City, State, Country) 
VALUES ('Jane Smith', 'Los Angeles', 'CA', 'USA');
IF @@ROWCOUNT = 0
    ROLLBACK TRANSACTION;
ELSE
    END TRANSACTION;
```

If the `INSERT` fails (e.g., no rows affected), the transaction is rolled back. Otherwise, it ends with a commit.

### Example 3. Using SAVEPOINT and ROLLBACK

```sql
BEGIN TRANSACTION;
SAVEPOINT SP1;
DELETE FROM Customers WHERE ID = 1;

SAVEPOINT SP2;
DELETE FROM Customers WHERE ID = 2;

ROLLBACK TO SP1; -- Undo changes after SP1
END TRANSACTION; -- Commit remaining changes
```

This example uses `SAVEPOINT` to create rollback points within a transaction. Changes after **SP1** are rolled back, while earlier changes are committed.

### Nested Transactions Example

```sql
BEGIN TRANSACTION MainTransaction;
INSERT INTO Customers (CustName, City, State, Country) 
VALUES ('Alice Brown', 'Chicago', 'IL', 'USA');

BEGIN TRANSACTION SubTransaction;
UPDATE Orders SET Product = 'Tablet' WHERE Id = 3;
END TRANSACTION; -- Commit SubTransaction

END TRANSACTION; -- Commit MainTransaction
```

Nested transactions allow specific portions of the transaction to be committed independently.


---

## See Also

- [Begin](./20_BEGIN.md)