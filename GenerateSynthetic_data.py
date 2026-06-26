import pandas as pd
import random
from faker import Faker

fake = Faker()

categories = [
    ("Network", "WAN"),
    ("Application", "SAP"),
    ("Database", "Oracle"),
    ("Email", "Outlook"),
    ("Cloud", "Azure"),
    ("Security", "Malware")
]

records = []

for i in range(1000):
    category, subcategory = random.choice(categories)

    records.append({
        "incident_id": f"INC{100000+i}",
        "priority": random.choice(["P1", "P2", "P3", "P4"]),
        "category": category,
        "subcategory": subcategory,
        "opened_by": fake.name(),
        "description": fake.sentence(),
        "impact": random.choice(["Low", "Medium", "High"]),
        "urgency": random.choice(["Low", "Medium", "High"]),
        "state": random.choice([
            "Open",
            "In Progress",
            "Resolved",
            "Closed"
        ])
    })

df = pd.DataFrame(records)

df.to_csv(
    "servicenow_incidents.csv",
    index=False
)