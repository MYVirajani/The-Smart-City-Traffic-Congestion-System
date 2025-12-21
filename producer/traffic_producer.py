import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

junctions = ["Junction_A", "Junction_B", "Junction_C", "Junction_D"]

while True:
    record = {
        "sensor_id": random.choice(junctions),
        "timestamp": datetime.utcnow().isoformat(),
        "vehicle_count": random.randint(20, 150),
        "avg_speed": random.choice([5, 8, 12, 20, 30])
    }

    producer.send("traffic-data", record)
    print("Sent:", record)
    time.sleep(1)
