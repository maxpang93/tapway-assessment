from flask import Flask, request, jsonify
import pika
import json
from datetime import datetime
import jsonschema

app = Flask(__name__)

with open("schema.json") as f:
    schema = json.load(f)

@app.route('/', methods=['POST'])
def validate_and_pass_to_queue():
    payload = request.get_json()

    # validate payload
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.exceptions.ValidationError as err:
        return jsonify({"error": err.message}), 400

    for pred in payload["data"]["preds"]:
        pred["image_frame"] = None # TODO remove frame to display less data, remove later
        if pred["prob"] < 0.25:
            pred["tags"].append("low_prob")

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

    return jsonify({
        "success": True,
        "msg":f"Message published to Queue at {timestamp}"
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
