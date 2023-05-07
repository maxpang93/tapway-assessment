from flask import Flask, request, jsonify
import pika
import json
from datetime import datetime
from custom_validator import validate_data

app = Flask(__name__)

@app.route('/', methods=['POST'])
def validate_and_pass_to_queue():
    payload = request.get_json()

    # validate payload
    err = validate_data(payload, show_full_error=False)
    if err:
        return jsonify({
            "error": "Invalid JSON data",
            "details": ';  '.join(err)
        }), 400
    
    # append tag
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
    app.run(host='0.0.0.0', port=5000)
