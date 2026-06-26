from confluent_kafka import Producer
import json
import random
import time
from datetime import datetime

conf = {
    'bootstrap.servers': 'pkc-619z3.us-east1.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'GSXQ54WCVVMLEPYK',
    'sasl.password': 'cflt0HFZqfAXw8mLTjMbVShtbbLtwGt/SxZTXFEiyEKqQOKQwsH/FyL4tB/f1cYA'
}
producer = Producer(conf)

topic = "topic_katana"

suppliers = [
    "IronWorks",
    "CircuitParts",
    "SteelCorp",
    "MicroTech",
    "ChipMakers"
]

materials = [
    "Microchips",
    "Steel",
    "Copper",
    "Plastic",
    "Aluminum"
]

try:
    while True:

        event = {
            "event_time": datetime.utcnow().isoformat(),
            "supplier": random.choice(suppliers),
            "material": random.choice(materials),
            "delay_days": random.randint(0, 15),
            "inventory_days": random.randint(1, 30),
            "shipment_status": random.choice(
                ["ON_TIME", "DELAYED", "IN_TRANSIT"]
            )
        }

        producer.produce(
            topic,
            key=event["supplier"],
            value=json.dumps(event)
        )

        producer.flush()

        print("Sent:", event)

        # Generate one event every 2 seconds
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped producer")
