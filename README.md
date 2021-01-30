# SF-Crime-Statistics-with-Spark-Streaming
Udacity Data Streaming Nano Degree Project

## Project
### Project structure
```
.
├── config
│   ├── server.properties
│   └── zookeeper.properties
├── consumer_server.py
├── data_stream.py
├── kafka_server.py
├── producer_server.py
├── README.md
└── screenshots
    ├── kafka-consumer-console output.png
    ├── Progress reporter after executing a Spark job.png
    └── Spark Streaming UI as the streaming continues.png
```
### Environment

* Spark 2.3.4
* Kafka 0.10
* Python 3.7

## Instructions

### Producer
```
python kafka_server.py
```
### Data stream process
```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py
```
### Consumer
```
python consumer_server.py
```

## Questions and Answers?

1. How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

* The change of processedRowsPerSecond and maxOffsetsPerTrigger could affect the throughput and latency.

2. What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

* It was possible to optimize the results with the configuration values bellow, They were optimal because those increased the processedRowsPerSecond numbers, so it increased the general process performance. 

```
spark.streaming.backpressure.enabled : true
spark.streaming.kafka.maxRatePerPartition : 100
spark.sql.shuffle.partitions : 100
spark.default.parallelism : 100
```

