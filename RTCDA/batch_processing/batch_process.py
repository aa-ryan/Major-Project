from __future__ import print_function
import sys
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: batch_process <without hdfs_path>", file=sys.stderr)
        sys.exit
    
    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("batch_processing")\
        .getOrCreate()

    # df = spark.read.json(sys.argv[1])
    # hdfs://localhost:8020/user/arx6363/user/*.dat
    df = spark.read.json('hdfs://localhost:8020/user/arx6363/user/*.dat')

    df.createOrReplaceTempView("wiki")
    sqlDF = spark.sql("SELECT prev_title as source, curr_title as topic, count(*) as count FROM wiki GROUP BY prev_title, curr_title ORDER BY count DESC LIMIT 10")
    sqlDF.show()
    
    # TABLE batch_source use source as partitionkey
    sqlDF.write \
         .format("org.apache.spark.sql.cassandra") \
         .mode('overwrite').option('confirm.truncate', 'true') \
         .options(table="batch_source", keyspace="wiki") \
         .save()
    
    # TABLE batch_topic use topic as partitionkey
    sqlDF.write \
         .format("org.apache.spark.sql.cassandra") \
         .mode('overwrite').option('confirm.truncate', 'true') \
         .options(table="batch_topic", keyspace="wiki") \
         .save()
    
    spark.stop()

  
