from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("SmartCityTraffic") \
    .getOrCreate()

schema = StructType([
    StructField("sensor_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("vehicle_count", IntegerType()),
    StructField("avg_speed", IntegerType())
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic-data") \
    .load()

parsed = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

windowed = parsed.groupBy(
    window(col("timestamp"), "5 minutes"),
    col("sensor_id")
).avg("avg_speed")

alerts = windowed.filter(col("avg(avg_speed)") < 10)

query = alerts.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
