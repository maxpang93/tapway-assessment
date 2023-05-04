import pika
import sys
import os
import csv
import json
from datetime import datetime


CSV_FILEPATH = "./data/data.csv"

def main():
    _init_csv()
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare('msg_queue')

    def callback(ch, method, properties, body):
        msg = json.loads(body.decode())
        _append_data_to_csv(msg)

    channel.basic_consume(
        queue='msg_queue',
        auto_ack=True,
        on_message_callback=callback
    )

    channel.start_consuming()

def _init_csv(csv_file=CSV_FILEPATH):
    # add header if file not exist
    if not os.path.exists(CSV_FILEPATH):
        header = [
            "device_id",
            "client_id",
            "created_at",
            "license_id",
            "image_frame",
            "prob",
            "tags"
        ]
        with open(csv_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(header)

def _append_data_to_csv(msg, csv_file=CSV_FILEPATH):
    with open(csv_file, 'a') as f:
        writer = csv.writer(f)
        rows = [
            [
                msg["device_id"],
                msg["client_id"],
                msg["created_at"],
                msg["data"]["license_id"],
                pred["image_frame"],
                pred["prob"],
                pred["tags"]
            ]
            for pred in msg["data"]["preds"]
        ]
        writer.writerows(rows)

if __name__ == "__main__":
    main()