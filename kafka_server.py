import producer_server


def run_kafka_server():

    logs_file = "police-department-calls-for-service.json"
    producer = producer_server.ProducerServer(
        input_file=logs_file,
        client_id="pd-call",
        topic="department.call.service.log",
        bootstrap_servers="localhost:9092"
    )
    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
