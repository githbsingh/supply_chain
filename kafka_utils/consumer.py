from confluent_kafka import Consumer
import json
conf = {
    'bootstrap.servers': 'pkc-619z3.us-east1.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'GSXQ54WCVVMLEPYK',
    'sasl.password': 'cflt0HFZqfAXw8mLTjMbVShtbbLtwGt/SxZTXFEiyEKqQOKQwsH/FyL4tB/f1cYA',
    'group.id': 'supply-chain-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['risk_events_json'])

def get_latest_risk():

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(msg.error())
            continue

        value = msg.value()

        # Find start of JSON
        json_start = value.find(b'{')

        if json_start == -1:
            print("No JSON found")
            continue

        json_bytes = value[json_start:]

        risk = json.loads(json_bytes.decode('utf-8'))

        #print("🚨 RISK ALERT")
        #print(risk)
        return risk