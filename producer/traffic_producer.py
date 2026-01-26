# import json
# import time
# import random
# from kafka import KafkaProducer
# from datetime import datetime

# producer = KafkaProducer(
#     bootstrap_servers="localhost:9092",
#     value_serializer=lambda v: json.dumps(v).encode("utf-8")
# )

# junctions = ["Junction_A", "Junction_B", "Junction_C", "Junction_D"]

# while True:
#     record = {
#         "sensor_id": random.choice(junctions),
#         "timestamp": datetime.utcnow().isoformat(),
#         "vehicle_count": random.randint(20, 150),
#         "avg_speed": random.choice([5, 8, 12, 20, 30])
#     }

#     producer.send("traffic-data", record)
#     print("Sent:", record)
#     time.sleep(1)

import json
import time
import random
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from datetime import datetime, timedelta
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

JUNCTIONS = ["Junction_A", "Junction_B", "Junction_C", "Junction_D"]
KAFKA_TOPIC = "traffic-data"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

class TrafficDataProducer:
    def __init__(self):
        self.producer = None
        self.connect_to_kafka()
        self.iteration = 0
        
    def connect_to_kafka(self, max_retries=5):
        for attempt in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    acks=1,
                    compression_type='gzip',
                    max_in_flight_requests_per_connection=5
                )
                logger.info(f"Successfully connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}")
                return
            except NoBrokersAvailable:
                logger.warning(f"Attempt {attempt + 1}/{max_retries}: Kafka broker not available. Retrying in 5 seconds...")
                time.sleep(5)
        
        logger.error("Failed to connect to Kafka after multiple attempts")
        sys.exit(1)
    
    def get_realistic_traffic(self, hour, minute):
        if 7 <= hour < 9 or (hour == 9 and minute < 30):
            vehicle_count = random.randint(100, 150)
            avg_speed = random.choices(
                [5, 8, 12, 20, 25, 30, 35], 
                weights=[10, 15, 15, 25, 20, 10, 5]
            )[0]
        elif 17 <= hour < 19 or (hour == 19 and minute < 30):
            vehicle_count = random.randint(110, 160)
            avg_speed = random.choices(
                [5, 8, 12, 20, 25, 30, 35], 
                weights=[15, 20, 15, 20, 15, 10, 5]
            )[0]
        elif 12 <= hour < 14:
            vehicle_count = random.randint(70, 110)
            avg_speed = random.choices(
                [12, 20, 25, 30, 35, 40], 
                weights=[10, 20, 25, 25, 15, 5]
            )[0]
        elif hour >= 22 or hour < 5:
            vehicle_count = random.randint(10, 40)
            avg_speed = random.choices(
                [30, 35, 40, 45], 
                weights=[20, 30, 30, 20]
            )[0]
        else:
            vehicle_count = random.randint(40, 90)
            avg_speed = random.choices(
                [20, 25, 30, 35, 40], 
                weights=[15, 25, 30, 20, 10]
            )[0]
        
        return vehicle_count, avg_speed
    
    def inject_critical_congestion(self):
        vehicle_count = random.randint(120, 160)
        avg_speed = random.choice([3, 5, 7, 9])
        return vehicle_count, avg_speed
    
    def generate_and_send_data(self):
        try:
            while True:
                current_time = datetime.now()
                hour = current_time.hour
                minute = current_time.minute
                
                vehicle_count, avg_speed = self.get_realistic_traffic(hour, minute)
                
                if self.iteration % random.randint(25, 35) == 0 and random.random() < 0.4:
                    vehicle_count, avg_speed = self.inject_critical_congestion()
                    junction = random.choice(JUNCTIONS)
                    logger.warning(f"CRITICAL CONGESTION INJECTED at {junction}: {avg_speed} km/h")
                else:
                    junction = random.choice(JUNCTIONS)
                
                record = {
                    "sensor_id": junction,
                    "timestamp": current_time.isoformat(),
                    "vehicle_count": vehicle_count,
                    "avg_speed": avg_speed
                }
                
                future = self.producer.send(KAFKA_TOPIC, record)
                
                status_icon = "ALERT" if avg_speed < 10 else "OK"
                logger.info(
                    f"[{status_icon}] [{record['timestamp'][:19]}] {record['sensor_id']}: "
                    f"{record['vehicle_count']} vehicles @ {record['avg_speed']} km/h"
                )
                
                self.iteration += 1
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Shutting down producer...")
            self.cleanup()
        except Exception as e:
            logger.error(f"Error in producer: {str(e)}")
            self.cleanup()
            raise
    
    def cleanup(self):
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Producer closed successfully")

def main():
    logger.info("=" * 70)
    logger.info("Smart City Traffic Data Producer Starting...")
    logger.info("=" * 70)
    logger.info(f"Junctions: {', '.join(JUNCTIONS)}")
    logger.info(f"Kafka Topic: {KAFKA_TOPIC}")
    logger.info(f"Kafka Broker: {KAFKA_BOOTSTRAP_SERVERS}")
    logger.info("=" * 70)
    
    producer = TrafficDataProducer()
    producer.generate_and_send_data()

if __name__ == "__main__":
    main()