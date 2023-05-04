from flask import Flask, request
import pika
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['POST'])
def validate_and_pass_to_queue():
    payload = request.get_json()

    # validate payload TODO
    require_fields = ["device_id", "client_id", "created_at"]
    for field in require_fields:
        print(payload[field])

    preds = payload["data"]["preds"]
    # for pred in preds:
    #     print(pred["prob"], pred["tags"])

    for pred in preds:
        pred["image_frame"] = None # remove frame to display less data, remove later
        if pred["prob"] < 0.25:
            pred["tags"].append("low_prob")

    # for pred in preds:
    #     print(pred["prob"], pred["tags"])

    # publish the msg to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare('msg_queue')

    timestamp = datetime.now()
    channel.basic_publish(
        exchange='',
        routing_key='msg_queue',
        body=json.dumps(payload)
    )

    connection.close()

    return f'Message published to Queue at {timestamp}'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
