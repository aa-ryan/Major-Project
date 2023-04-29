from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("wiki").config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint").getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "click") \
  .option("failOnDataLoss", "false") \
  .option("startingOffsets", "earliest") \
  .load() \
  .selectExpr("CAST(value AS STRING)")

schema = "prev_title STRING, timestamp TIMESTAMP"
df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

watermarkedDF = df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(window("timestamp", "5 minutes"), "prev_title") \
    .agg(count("*").alias("count"), max("timestamp").alias("timestamp"))

watermarkedDF.createOrReplaceTempView("wiki")

sqlDF = spark.sql("SELECT prev_title as source, count, timestamp FROM wiki")

query = sqlDF.writeStream \
    .outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "wiki") \
    .option("table", "realtime") \
    .start()

query.awaitTermination()
