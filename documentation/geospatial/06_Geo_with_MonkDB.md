```bash
Let’s assume our database has the following points:
id	location (GEO_POINT)
1	[5, 5]
2	[-8, -8]
3	[15, 15]
4	[-12, 5]
Polygon Boundary

(-10,-10)      (10,-10)
     +------------+
     |            |
     |            |
     +------------+
(-10,10)        (10,10)

What Happens When the Query Runs?
id	location (GEO_POINT)	Inside Polygon?
1	[5, 5]	✅ YES
2	[-8, -8]	✅ YES
3	[15, 15]	❌ NO (outside boundary)
4	[-12, 5]	❌ NO (outside boundary)

Query Result:

id  | location
---------------
1   | [5,5]
2   | [-8,-8]
```

```bash
Table 'monkdb.geo_points' has been created.
Table 'monkdb.geo_shapes' has been created.
Inserted point ID 1 at location [-132.57216, -52.69326] in monkdb.
Inserted point ID 2 at location [151.582623, 54.153087] in monkdb.
Inserted point ID 3 at location [81.293244, -54.672008] in monkdb.
Inserted point ID 4 at location [102.959424, -79.185535] in monkdb.
Inserted point ID 5 at location [88.458914, -0.367918] in monkdb.
Inserted point ID 6 at location [-138.345894, -28.242759] in monkdb.
Inserted point ID 7 at location [-15.159242, -29.616913] in monkdb.
Inserted point ID 8 at location [5.006293, -5.374171] in monkdb.
Inserted point ID 9 at location [33.150474, -16.879792] in monkdb.
Inserted point ID 10 at location [-164.983769, -53.055628] in monkdb.
Inserted shape ID 1 with WKT: POLYGON ((-21.116987 -15.252228, 2.652011 47.669706, 5.365045 14.547793, -21.116987 -15.252228)) in monkdb.
Inserted shape ID 2 with WKT: POLYGON ((-36.985187 -34.572001, -32.654479 -15.555314, 36.435662 35.521955, 22.220096 11.627303, -36.985187 -34.572001)) in monkdb.
Inserted shape ID 3 with WKT: POLYGON ((15.89106 -43.386096, -39.814844 -28.742565, 9.352968 43.893455, 38.896167 -31.686455, 15.89106 -43.386096)) in monkdb.
Inserted shape ID 4 with WKT: POLYGON ((-15.772757 -7.411465, -34.427736 33.721657, 48.336815 45.988126, 39.783495 9.946578, -15.772757 -7.411465)) in monkdb.
Inserted shape ID 5 with WKT: POLYGON ((45.327418 -41.791533, -41.086429 18.729295, 30.275095 23.680088, 46.047848 0.456104, 45.327418 -41.791533)) in monkdb.

Geo Points:
[8, [5.0062929186969995, -5.37417100276798]]
[4, [102.95942394062877, -79.18553500436246]]
[5, [88.45891392789781, -0.36791802383959293]]
[7, [-15.159242022782564, -29.616913008503616]]
[1, [-132.57216003723443, -52.693260004743934]]
[2, [151.58262295648456, 54.15308696217835]]
[3, [81.29324393346906, -54.67200803104788]]
[6, [-138.3458940591663, -28.24275903403759]]
[9, [33.15047398209572, -16.8797920178622]]
[10, [-164.98376900330186, -53.055628035217524]]

Geo Shapes:
[4, {'coordinates': [[[-15.772757, -7.411465], [-34.427736, 33.721657], [48.336815, 45.988126], [39.783495, 9.946578], [-15.772757, -7.411465]]], 'type': 'Polygon'}]
[1, {'coordinates': [[[-21.116987, -15.252228], [2.652011, 47.669706], [5.365045, 14.547793], [-21.116987, -15.252228]]], 'type': 'Polygon'}]
[2, {'coordinates': [[[-36.985187, -34.572001], [-32.654479, -15.555314], [36.435662, 35.521955], [22.220096, 11.627303], [-36.985187, -34.572001]]], 'type': 'Polygon'}]
[3, {'coordinates': [[[15.89106, -43.386096], [-39.814844, -28.742565], [9.352968, 43.893455], [38.896167, -31.686455], [15.89106, -43.386096]]], 'type': 'Polygon'}]

Points within given polygon:
[8, [5.0062929186969995, -5.37417100276798]]
```