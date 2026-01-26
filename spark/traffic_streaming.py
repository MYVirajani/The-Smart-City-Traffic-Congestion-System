# # from pyspark.sql import SparkSession
# # from pyspark.sql.functions import from_json, col, window
# # from pyspark.sql.types import *

# # spark = SparkSession.builder \
# #     .appName("SmartCityTraffic") \
# #     .getOrCreate()

# # schema = StructType([
# #     StructField("sensor_id", StringType()),
# #     StructField("timestamp", StringType()),
# #     StructField("vehicle_count", IntegerType()),
# #     StructField("avg_speed", IntegerType())
# # ])

# # df = spark.readStream \
# #     .format("kafka") \
# #     .option("kafka.bootstrap.servers", "localhost:9092") \
# #     .option("subscribe", "traffic-data") \
# #     .load()

# # parsed = df.select(
# #     from_json(col("value").cast("string"), schema).alias("data")
# # ).select("data.*")

# # windowed = parsed.groupBy(
# #     window(col("timestamp"), "5 minutes"),
# #     col("sensor_id")
# # ).avg("avg_speed")

# # alerts = windowed.filter(col("avg(avg_speed)") < 10)

# # query = alerts.writeStream \
# #     .outputMode("append") \
# #     .format("console") \
# #     .start()

# # query.awaitTermination()


# from pyspark.sql import SparkSession
# from pyspark.sql.functions import (
#     from_json, col, window, avg, count, sum as spark_sum,
#     to_timestamp, current_timestamp, expr, lit, when
# )
# from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
# import logging
# import os

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
# KAFKA_TOPIC = "traffic-data"
# POSTGRES_URL = "jdbc:postgresql://postgres:5432/traffic_db"
# POSTGRES_USER = "postgres"
# POSTGRES_PASSWORD = "postgres"
# CHECKPOINT_LOCATION = "./checkpoints"
# DATA_LOCATION = "./data/traffic_history"

# os.makedirs(CHECKPOINT_LOCATION, exist_ok=True)
# os.makedirs(DATA_LOCATION, exist_ok=True)

# class TrafficStreamProcessor:
#     def __init__(self):
#         self.spark = None
#         self.initialize_spark()
    
#     def initialize_spark(self):
#         logger.info("Initializing Spark Session...")
        
#         self.spark = SparkSession.builder \
#             .appName("SmartCityTrafficStreaming") \
#             .master("local[*]") \
#             .config("spark.jars.packages", 
#                     "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,"
#                     "org.postgresql:postgresql:42.6.0") \
#             .config("spark.sql.streaming.schemaInference", "true") \
#             .config("spark.sql.adaptive.enabled", "true") \
#             .config("spark.sql.shuffle.partitions", "4") \
#             .config("spark.streaming.stopGracefullyOnShutdown", "true") \
#             .getOrCreate()
        
#         self.spark.sparkContext.setLogLevel("WARN")
#         logger.info("Spark Session initialized successfully")
    
#     def get_kafka_stream(self):
#         logger.info(f"Connecting to Kafka topic: {KAFKA_TOPIC}")
        
#         schema = StructType([
#             StructField("sensor_id", StringType(), False),
#             StructField("timestamp", StringType(), False),
#             StructField("vehicle_count", IntegerType(), False),
#             StructField("avg_speed", IntegerType(), False)
#         ])
        
#         df = self.spark.readStream \
#             .format("kafka") \
#             .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
#             .option("subscribe", KAFKA_TOPIC) \
#             .option("startingOffsets", "latest") \
#             .option("failOnDataLoss", "false") \
#             .load()
        
#         parsed_df = df.select(
#             from_json(col("value").cast("string"), schema).alias("data")
#         ).select("data.*")
        
#         parsed_df = parsed_df.withColumn(
#             "event_time", 
#             to_timestamp(col("timestamp"))
#         )
        
#         logger.info("Kafka stream connected successfully")
#         return parsed_df
    
#     def process_windowed_aggregations(self, df):
#         logger.info("Applying windowed aggregations...")
        
#         windowed_df = df \
#             .withWatermark("event_time", "2 minutes") \
#             .groupBy(
#                 window(col("event_time"), "5 minutes"),
#                 col("sensor_id")
#             ).agg(
#                 avg("avg_speed").alias("avg_speed"),
#                 avg("vehicle_count").alias("avg_vehicle_count"),
#                 count("*").alias("reading_count"),
#                 spark_sum("vehicle_count").alias("total_vehicles")
#             )
        
#         congestion_df = windowed_df.withColumn(
#             "congestion_index",
#             expr("ROUND((avg_vehicle_count / (avg_speed + 1)) * 10, 2)")
#         )
        
#         congestion_df = congestion_df.withColumn(
#             "processing_time",
#             current_timestamp()
#         )
        
#         return congestion_df
    
#     def filter_critical_alerts(self, df):
#         logger.info("Setting up critical alert filtering...")
        
#         critical_alerts = df.filter(col("avg_speed") < 10) \
#             .select(
#                 col("sensor_id"),
#                 col("window.start").alias("window_start"),
#                 col("window.end").alias("window_end"),
#                 col("avg_speed"),
#                 col("avg_vehicle_count"),
#                 col("congestion_index"),
#                 col("reading_count"),
#                 current_timestamp().alias("alert_generated_at")
#             )
        
#         return critical_alerts
    
#     def write_to_postgres(self, batch_df, batch_id):
#         try:
#             if batch_df.count() > 0:
#                 batch_df.write \
#                     .format("jdbc") \
#                     .option("url", POSTGRES_URL) \
#                     .option("dbtable", "critical_traffic_alerts") \
#                     .option("user", POSTGRES_USER) \
#                     .option("password", POSTGRES_PASSWORD) \
#                     .option("driver", "org.postgresql.Driver") \
#                     .mode("append") \
#                     .save()
                
#                 logger.info(f"Batch {batch_id}: Wrote {batch_df.count()} critical alerts to PostgreSQL")
#         except Exception as e:
#             logger.error(f"Error writing batch {batch_id} to PostgreSQL: {str(e)}")
    
#     def write_history_to_postgres(self, batch_df, batch_id):
#         try:
#             if batch_df.count() > 0:
#                 history_df = batch_df.select(
#                     col("sensor_id"),
#                     col("window.start").alias("window_start"),
#                     col("window.end").alias("window_end"),
#                     col("avg_speed"),
#                     col("avg_vehicle_count"),
#                     col("reading_count"),
#                     col("congestion_index")
#                 )
                
#                 history_df.write \
#                     .format("jdbc") \
#                     .option("url", POSTGRES_URL) \
#                     .option("dbtable", "traffic_history") \
#                     .option("user", POSTGRES_USER) \
#                     .option("password", POSTGRES_PASSWORD) \
#                     .option("driver", "org.postgresql.Driver") \
#                     .mode("append") \
#                     .save()
                
#                 logger.info(f"Batch {batch_id}: Wrote {history_df.count()} records to traffic history")
#         except Exception as e:
#             logger.error(f"Error writing batch {batch_id} to traffic history: {str(e)}")
    
#     def start_streaming(self):
#         logger.info("Starting streaming queries...")
        
#         raw_stream = self.get_kafka_stream()
#         processed_stream = self.process_windowed_aggregations(raw_stream)
#         critical_alerts = self.filter_critical_alerts(processed_stream)
        
#         logger.info("Starting Parquet writer...")
#         parquet_query = processed_stream.writeStream \
#             .outputMode("append") \
#             .format("parquet") \
#             .option("path", DATA_LOCATION) \
#             .option("checkpointLocation", f"{CHECKPOINT_LOCATION}/traffic_parquet") \
#             .trigger(processingTime="30 seconds") \
#             .start()
        
#         logger.info("Starting PostgreSQL history writer...")
#         history_query = processed_stream.writeStream \
#             .outputMode("append") \
#             .foreachBatch(self.write_history_to_postgres) \
#             .option("checkpointLocation", f"{CHECKPOINT_LOCATION}/traffic_history") \
#             .trigger(processingTime="30 seconds") \
#             .start()
        
#         logger.info("Starting critical alerts writer...")
#         alerts_query = critical_alerts.writeStream \
#             .outputMode("append") \
#             .foreachBatch(self.write_to_postgres) \
#             .option("checkpointLocation", f"{CHECKPOINT_LOCATION}/critical_alerts") \
#             .trigger(processingTime="10 seconds") \
#             .start()
        
#         logger.info("Starting console monitor...")
#         console_query = critical_alerts.writeStream \
#             .outputMode("append") \
#             .format("console") \
#             .option("truncate", "false") \
#             .option("numRows", "20") \
#             .start()
        
#         logger.info("=" * 70)
#         logger.info("All streaming queries started successfully!")
#         logger.info("=" * 70)
#         logger.info("Monitoring console for critical alerts...")
#         logger.info("Writing data to PostgreSQL and Parquet...")
#         logger.info("Window: 5 minutes | Watermark: 2 minutes")
#         logger.info("Alert Threshold: Speed < 10 km/h")
#         logger.info("=" * 70)
        
#         self.spark.streams.awaitAnyTermination()

# def main():
#     logger.info("=" * 70)
#     logger.info("Smart City Traffic Stream Processor Starting...")
#     logger.info("=" * 70)
    
#     processor = TrafficStreamProcessor()
#     processor.start_streaming()

# if __name__ == "__main__":
#     main()

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, avg, count, sum as spark_sum,
    to_timestamp, current_timestamp, expr, lit, when
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "traffic-data"
POSTGRES_URL = "jdbc:postgresql://postgres:5432/traffic_db"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
CHECKPOINT_LOCATION = "./checkpoints"
DATA_LOCATION = "./data/traffic_history"

os.makedirs(CHECKPOINT_LOCATION, exist_ok=True)
os.makedirs(DATA_LOCATION, exist_ok=True)

class TrafficStreamProcessor:
    def __init__(self):
        self.spark = None
        self.initialize_spark()
    
    def initialize_spark(self):
        logger.info("Initializing Spark Session...")
        
        self.spark = SparkSession.builder \
            .appName("SmartCityTrafficStreaming") \
            .master("local[*]") \
            .config("spark.jars.packages", 
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,"
                    "org.postgresql:postgresql:42.6.0") \
            .config("spark.sql.streaming.schemaInference", "true") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.shuffle.partitions", "4") \
            .config("spark.streaming.stopGracefullyOnShutdown", "true") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        logger.info("Spark Session initialized successfully")
    
    def get_kafka_stream(self):
        logger.info(f"Connecting to Kafka topic: {KAFKA_TOPIC}")
        
        schema = StructType([
            StructField("sensor_id", StringType(), False),
            StructField("timestamp", StringType(), False),
            StructField("vehicle_count", IntegerType(), False),
            StructField("avg_speed", IntegerType(), False)
        ])
        
        df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
            .option("subscribe", KAFKA_TOPIC) \
            .option("startingOffsets", "latest") \
            .option("failOnDataLoss", "false") \
            .load()
        
        parsed_df = df.select(
            from_json(col("value").cast("string"), schema).alias("data"),
            col("timestamp").alias("kafka_timestamp")
        ).select("data.*", "kafka_timestamp")
        
        # Use Kafka timestamp instead of event timestamp for more reliable processing
        parsed_df = parsed_df.withColumn(
            "event_time", 
            col("kafka_timestamp").cast("timestamp")
        )
        
        logger.info("Kafka stream connected successfully")
        return parsed_df
    
    def process_windowed_aggregations(self, df):
        logger.info("Applying windowed aggregations...")
        
        # Reduced watermark from 2 minutes to 30 seconds for faster processing
        windowed_df = df \
            .withWatermark("event_time", "30 seconds") \
            .groupBy(
                window(col("event_time"), "2 minutes"),  # Reduced from 5 to 2 minutes
                col("sensor_id")
            ).agg(
                avg("avg_speed").alias("avg_speed"),
                avg("vehicle_count").alias("avg_vehicle_count"),
                count("*").alias("reading_count"),
                spark_sum("vehicle_count").alias("total_vehicles")
            )
        
        congestion_df = windowed_df.withColumn(
            "congestion_index",
            expr("ROUND((avg_vehicle_count / (avg_speed + 1)) * 10, 2)")
        )
        
        congestion_df = congestion_df.withColumn(
            "processing_time",
            current_timestamp()
        )
        
        return congestion_df
    
    def filter_critical_alerts(self, df):
        logger.info("Setting up critical alert filtering...")
        
        critical_alerts = df.filter(col("avg_speed") < 10) \
            .select(
                col("sensor_id"),
                col("window.start").alias("window_start"),
                col("window.end").alias("window_end"),
                col("avg_speed"),
                col("avg_vehicle_count"),
                col("congestion_index"),
                col("reading_count"),
                current_timestamp().alias("alert_generated_at")
            )
        
        return critical_alerts
    
    def write_to_postgres(self, batch_df, batch_id):
        try:
            if batch_df.count() > 0:
                batch_df.write \
                    .format("jdbc") \
                    .option("url", POSTGRES_URL) \
                    .option("dbtable", "critical_traffic_alerts") \
                    .option("user", POSTGRES_USER) \
                    .option("password", POSTGRES_PASSWORD) \
                    .option("driver", "org.postgresql.Driver") \
                    .mode("append") \
                    .save()
                
                logger.info(f"Batch {batch_id}: Wrote {batch_df.count()} critical alerts to PostgreSQL")
            else:
                logger.info(f"Batch {batch_id}: No critical alerts to write")
        except Exception as e:
            logger.error(f"Error writing batch {batch_id} to PostgreSQL: {str(e)}")
    
    def write_history_to_postgres(self, batch_df, batch_id):
        try:
            record_count = batch_df.count()
            if record_count > 0:
                history_df = batch_df.select(
                    col("sensor_id"),
                    col("window.start").alias("window_start"),
                    col("window.end").alias("window_end"),
                    col("avg_speed"),
                    col("avg_vehicle_count"),
                    col("reading_count"),
                    col("congestion_index")
                )
                
                history_df.write \
                    .format("jdbc") \
                    .option("url", POSTGRES_URL) \
                    .option("dbtable", "traffic_history") \
                    .option("user", POSTGRES_USER) \
                    .option("password", POSTGRES_PASSWORD) \
                    .option("driver", "org.postgresql.Driver") \
                    .mode("append") \
                    .save()
                
                logger.info(f"✅ Batch {batch_id}: Wrote {record_count} records to traffic_history")
            else:
                logger.info(f"⚠️  Batch {batch_id}: No records to write (empty batch)")
        except Exception as e:
            logger.error(f"❌ Error writing batch {batch_id} to traffic history: {str(e)}")
    
    def start_streaming(self):
        logger.info("Starting streaming queries...")
        
        raw_stream = self.get_kafka_stream()
        processed_stream = self.process_windowed_aggregations(raw_stream)
        critical_alerts = self.filter_critical_alerts(processed_stream)
        
        logger.info("Starting Parquet writer...")
        parquet_query = processed_stream.writeStream \
            .outputMode("append") \
            .format("parquet") \
            .option("path", DATA_LOCATION) \
            .option("checkpointLocation", f"{CHECKPOINT_LOCATION}/traffic_parquet") \
            .trigger(processingTime="15 seconds") \
            .start()
        
        logger.info("Starting PostgreSQL history writer...")
        history_query = processed_stream.writeStream \
            .outputMode("append") \
            .foreachBatch(self.write_history_to_postgres) \
            .option("checkpointLocation", f"{CHECKPOINT_LOCATION}/traffic_history") \
            .trigger(processingTime="15 seconds") \
            .start()
        
        logger.info("Starting critical alerts writer...")
        alerts_query = critical_alerts.writeStream \
            .outputMode("append") \
            .foreachBatch(self.write_to_postgres) \
            .option("checkpointLocation", f"{CHECKPOINT_LOCATION}/critical_alerts") \
            .trigger(processingTime="10 seconds") \
            .start()
        
        logger.info("Starting console monitor...")
        console_query = processed_stream.writeStream \
            .outputMode("append") \
            .format("console") \
            .option("truncate", "false") \
            .option("numRows", "20") \
            .trigger(processingTime="15 seconds") \
            .start()
        
        logger.info("=" * 70)
        logger.info("All streaming queries started successfully!")
        logger.info("=" * 70)
        logger.info("Monitoring console for traffic data...")
        logger.info("Writing data to PostgreSQL and Parquet...")
        logger.info("Window: 2 minutes | Watermark: 30 seconds")
        logger.info("Alert Threshold: Speed < 10 km/h")
        logger.info("Processing Interval: 15 seconds")
        logger.info("=" * 70)
        
        self.spark.streams.awaitAnyTermination()

def main():
    logger.info("=" * 70)
    logger.info("Smart City Traffic Stream Processor Starting...")
    logger.info("=" * 70)
    
    processor = TrafficStreamProcessor()
    processor.start_streaming()

if __name__ == "__main__":
    main()