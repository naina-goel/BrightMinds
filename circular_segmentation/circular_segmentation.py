import cv2
import numpy as np
from typing import Tuple, Dict
from flask import Flask, request, jsonify
import uuid
import os
import json

# Define dataclass for circular object
class CircularObject:
    def __init__(self, id: str, bounding_box: Tuple[int, int, int, int], centroid: Tuple[int, int], radius: int):
        self.id = id
        self.bounding_box = bounding_box
        self.centroid = centroid
        self.radius = radius

# Store circular objects
circular_objects: Dict[str, CircularObject] = {}

app = Flask(__name__)

# Endpoint to upload image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        return 'Image uploaded successfully', 200

# Endpoint to process and segment circular objects
@app.route('/segment', methods=['POST'])
def segment_image():
    file_path = request.json.get('file_path')
    if not file_path:
        return 'File path not provided', 400

    image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    if image is None:
        return 'Invalid image file', 400

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    edges = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        if radius > 10:
            id = str(uuid.uuid4())
            M = cv2.moments(contour)
            if M['m00'] == 0:
                continue
            centroid = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
            bounding_box = cv2.boundingRect(contour)
            circular_objects[id] = CircularObject(id, bounding_box, centroid, int(radius))

    return 'Segmentation completed', 200

# Endpoint to retrieve list of all circular objects
@app.route('/objects', methods=['GET'])
def get_objects():
    response = [{
        'id': obj.id,
        'bounding_box': obj.bounding_box
    } for obj in circular_objects.values()]
    return jsonify(response)

# Endpoint to get details of a particular circular object
@app.route('/object/<id>', methods=['GET'])
def get_object_details(id: str):
    if id in circular_objects:
        obj = circular_objects[id]
        return jsonify({
            'id': obj.id,
            'bounding_box': obj.bounding_box,
            'centroid': obj.centroid,
            'radius': obj.radius
        })
    return 'Object not found', 404

# Endpoint to load annotation file (_annotations.coco)
@app.route('/annotations', methods=['GET'])
def load_annotations():
    try:
        with open('uploads/_annotations.coco', 'r') as file:
            annotations = json.load(file)
        return jsonify(annotations)
    except FileNotFoundError:
        return 'Annotations file not found', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)