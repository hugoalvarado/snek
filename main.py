import base64

import boto3
from flask import Flask, request, jsonify
app = Flask(__name__)

MAX_LABELS = 10
MIN_CONFIDENCE = 60

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
        return jsonify(response['Labels'])
