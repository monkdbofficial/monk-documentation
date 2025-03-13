```bash
$ psql -h localhost -p 5432 -U testuser -d monkdb -W
```

```psql
CREATE TABLE IF NOT EXISTS sensor_data (timestamp TIMESTAMP WITH TIME ZONE PRIMARY KEY, location TEXT NOT NULL, temperature FLOAT NOT NULL, humidity FLOAT NOT NULL, wind_speed FLOAT NOT NULL);
```

```text
SQLAlchemy==2.0.39
monk-orm==1.0.1
```

```python

```


