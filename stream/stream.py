import json
import logging
import os
import stream_setup
from argparse import ArgumentParser
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from time import sleep


log = logging.getLogger(__name__)

KAFKA_HOST = os.getenv("KAFKA_HOST", "kafka")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST", "memgraph-mage")
MEMGRAPH_PORT = int(os.getenv("MEMGRAPH_PORT", "7687"))


def parse_args():
    """
    Parse input command line arguments.
    """
    parser = ArgumentParser(
        description="A service that reads a CSV file and streams data to Kafka.")
    parser.add_argument("--file", help="CSV file with data to be streamed.")
    parser.add_argument(
        "--interval",
        type=int,
        help="Interval for sending data in seconds.")
    return parser.parse_args()


def create_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_HOST + ':' + KAFKA_PORT)
            return producer
        except NoBrokersAvailable:
            print("Failed to connect to Kafka")
            sleep(1)


def main():
    args = parse_args()

    stream_setup.create_topic(KAFKA_HOST, KAFKA_PORT)
    memgraph = stream_setup.connect_to_memgraph(MEMGRAPH_HOST, MEMGRAPH_PORT)
    stream_setup.create_stream(memgraph)

    producer = create_kafka_producer()
    with open(args.file) as f:
        for line in f.readlines():
            friendship_json = {
                "id_1": line[0],
                "id_2": line[1],
            }
            print(f"Sending data to topic 'friendships'")
            producer.send(topic='friendships', value=json.dumps(friendship_json).encode('utf8'))
            sleep(args.interval)


if __name__ == "__main__":
    main()
