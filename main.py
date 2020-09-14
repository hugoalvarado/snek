import base64
from datetime import datetime

import boto3
from flask import Flask, request, jsonify
app = Flask(__name__)

MAX_LABELS = 10
MIN_CONFIDENCE = 60
SNS_ARN = 'arn:aws:sns:us-east-1:511745405004:snek-watch'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/find', methods=['POST'])
def find_snek():
    if request.method == 'POST':
        rekognition = boto3.client('rekognition')
        response = rekognition.detect_labels(
            Image={
                "Bytes": base64.b64decode(request.form.get('image_blob'))
            },
            MaxLabels=MAX_LABELS,
            MinConfidence=MIN_CONFIDENCE,
        )

        if 'snake' in [label['Name'].lower() for label in response['Labels']]:
            sns = boto3.client('sns')
            # Publish a simple message to the specified SNS topic
            sns.publish(
                TopicArn=SNS_ARN,
                Message='Snake found at ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

        return jsonify(response['Labels'])
