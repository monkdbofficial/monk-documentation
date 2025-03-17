

```bash
Dropped monkdb.doc_json table
✅ Table created successfully!
✅ Sample user data inserted successfully!

🔍 Number of records in table:
[
    [
        5
    ]
]

🔍 Full User Data:
[
    [
        4,
        "David",
        {
            "skills": [
                "Java",
                "Spring Boot"
            ],
            "city": "London"
        }
    ],
    [
        5,
        "Eve",
        {
            "skills": [
                "AI",
                "Machine Learning"
            ],
            "city": "Tokyo",
            "profile": {
                "preferences": {
                    "language": "Japanese",
                    "food": "Sushi"
                }
            }
        }
    ],
    [
        1,
        "Alice",
        {
            "skills": [
                "Python",
                "SQL",
                "AI"
            ],
            "city": "New York",
            "profile": {
                "preferences": {
                    "language": "English",
                    "food": "Italian"
                }
            }
        }
    ],
    [
        2,
        "Bob",
        {
            "skills": [
                "JavaScript",
                "Node.js"
            ],
            "city": "San Francisco",
            "profile": {
                "preferences": {
                    "language": "Spanish",
                    "food": "Mexican"
                }
            }
        }
    ],
    [
        3,
        "Charlie",
        {
            "skills": [
                "Go",
                "Rust"
            ],
            "city": "Berlin",
            "profile": {}
        }
    ]
]

🌍 Users and Their Cities:
[
    [
        "David",
        "London"
    ],
    [
        "Eve",
        "Tokyo"
    ],
    [
        "Alice",
        "New York"
    ],
    [
        "Bob",
        "San Francisco"
    ],
    [
        "Charlie",
        "Berlin"
    ]
]

💡 Users with Skills:
[
    [
        "David",
        [
            "Java",
            "Spring Boot"
        ]
    ],
    [
        "Eve",
        [
            "AI",
            "Machine Learning"
        ]
    ],
    [
        "Alice",
        [
            "Python",
            "SQL",
            "AI"
        ]
    ],
    [
        "Bob",
        [
            "JavaScript",
            "Node.js"
        ]
    ],
    [
        "Charlie",
        [
            "Go",
            "Rust"
        ]
    ]
]

🧠 Users with AI Skills:
[
    [
        "Eve"
    ],
    [
        "Alice"
    ]
]

🍔 Users with Food Preferences:
[
    [
        "Eve",
        "Sushi"
    ],
    [
        "Alice",
        "Italian"
    ],
    [
        "Bob",
        "Mexican"
    ]
]

🔑 JSON Keys for Each User:
[
    [
        "David",
        [
            "skills",
            "city"
        ]
    ],
    [
        "Eve",
        [
            "skills",
            "city",
            "profile"
        ]
    ],
    [
        "Alice",
        [
            "skills",
            "city",
            "profile"
        ]
    ],
    [
        "Bob",
        [
            "skills",
            "city",
            "profile"
        ]
    ],
    [
        "Charlie",
        [
            "skills",
            "city",
            "profile"
        ]
    ]
]

✏️ Updated Alice's City to Paris!

✅ Alice's Updated City:
[
    [
        "Alice",
        "New York"
    ]
]

🚀 MonkDB JSON Store Simulation Completed Successfully!
```