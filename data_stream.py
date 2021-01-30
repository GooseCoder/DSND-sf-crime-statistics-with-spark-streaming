import logging

from pyspark.sql import SparkSession
from pyspark.sql.types import *

import pyspark.sql.functions as psf

schema = StructType([
    StructField('crime_id', StringType()),
    StructField('original_crime_type_name', StringType()),
    StructField('report_date', StringType()),
    StructField('call_date', StringType()),
    StructField('offense_date', StringType()),
    StructField('call_time', StringType()),
    StructField('call_date_time', StringType()),
    StructField('disposition', StringType()),
    StructField('address', StringType()),
    StructField('city', StringType()),
    StructField('state', StringType()),
    StructField('agency_id', StringType()),
    StructField('address_type', StringType()),
    StructField('common_location', StringType())
])


def run_spark_job(spark):

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "department.call.service.log") \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", "100") \
        .option("maxRatePerPartition", "2") \
        .option("stopGracefullyOnShutdown", "true") \
        .load()
    df.printSchema()

    kafka_df = df.selectExpr("CAST(value AS STRING)")

    service_table = kafka_df\
        .select(psf.from_json(psf.col('value'), schema).alias("DF_TABLE"))\
        .select("DF_TABLE.*")
    service_table.printSchema()

    distinct_table = service_table \
        .select("original_crime_type_name", "disposition") \
        .distinct()
    distinct_table.printSchema()

    agg_df = distinct_table \
        .dropna() \
        .select("original_crime_type_name") \
        .withWatermark("call_datetime", "60 minutes") \
        .groupby("original_crime_type_name") \
        .agg({"original_crime_type_name" : "count"}) \
        .orderBy("count(original_crime_type_name)", ascending=False)

    query = agg_df \
        .writeStream \
        .format('console') \
        .outputMode('Complete') \
        .trigger(processingTime="10 seconds") \
        .start()
    query.awaitTermination()

    radio_code_json_filepath = "radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition").collect()
    
    join_query = agg_df.join(radio_code_df, col("agg_df.disposition") == col("radio_code_df.disposition"), "left_outer")
    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    spark = SparkSession \
        .builder \
        .config("spark.ui.port", 3000) \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .getOrCreate()

    logger.info("Start Spark Job")

    run_spark_job(spark)

    logger.info("End Spark Job")
    spark.stop()
