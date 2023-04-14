from __future__ import print_function
import sys
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession

# Lazily instantiated global instance of SparkSession
# def getSparkSessionInstance(sparkConf):
#     if ("sparkSessionSingletonInstance" not in globals()):
#         globals()["sparkSessionSingletonInstance"] = SparkSession \
#             .builder \
#             .config(conf=sparkConf) \
#             .getOrCreate()
#     return globals()["sparkSessionSingletonInstance"]

def process():
    try:
        # Get the singleton instance of SparkSession
        # spark = getSparkSessionInstance(rdd.context.getConf())
        spark = SparkSession.builder.appName("wiki").getOrCreate()
        rdd = spark \
            .readStream.format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "cs") \
            .option('startingOffsets', 'earliest') \
            .load()
        df = spark.read.json(rdd)

        # Creates a temporary view using the DataFrame
        df.createOrReplaceTempView("wiki")

        sqlDF = spark.sql("SELECT prev_title as source, count(*) as count, max(timestamp) as timestamp FROM wiki group by prev_title")
        
        sqlDF.show()
        
        sqlDF.write \
             .format("org.apache.spark.sql.cassandra") \
             .mode('append') \
             .options(table="realtime", keyspace="wiki") \
             .save()
        
    except:
        pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: streaming <bootstrap.servers>", file=sys.stderr)
        exit(-1)
    
    sc = SparkContext(appName="wiki")
    ssc = StreamingContext(sc, 1)

    process()
    
    ssc.start()
    ssc.awaitTermination()
    
