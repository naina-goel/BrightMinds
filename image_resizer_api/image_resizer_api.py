import os
import csv
from flask import Flask, request, send_file
from PIL import Image

app = Flask(__name__)
DATA_FILE = 'csv_files/Challenge2.csv'

# Utility function to load metadata from CSV
def load_metadata():
    metadata = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                metadata[row['depth']] = row
    return metadata

# Utility function to save metadata to CSV
def save_metadata(metadata):
    fieldnames = ['depth', 'original_filename', 'width', 'height', 'file_path']
    with open(DATA_FILE, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for data in metadata.values():
            writer.writerow(data)

@app.route('/resize', methods=['POST'])
def resize_image():
    if 'image' not in request.files:
        return {"error": "No image file provided"}, 400
    
    image = request.files['image']
    width = int(request.form.get('width', 0))
    height = int(request.form.get('height', 0))
    depth = request.form.get('depth', '')
    
    if width <= 0 or height <= 0 or not depth:
        return {"error": "Invalid width, height, or depth"}, 400
    
    try:
        img = Image.open(image)
        img_resized = img.resize((width, height))
        
        # Save resized image locally
        output_path = f"resized_{image.filename}"
        img_resized.save(output_path)
        
        # Update metadata
        metadata = load_metadata()
        metadata[depth] = {
            "depth": depth,
            "original_filename": image.filename,
            "width": width,
            "height": height,
            "file_path": output_path
        }
        save_metadata(metadata)
        
        return {"message": "Image resized successfully", "file_path": output_path}, 200
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/image/<depth>', methods=['GET'])
def get_image(depth):
    metadata = load_metadata()
    if depth in metadata and os.path.exists(metadata[depth]['file_path']):
        return send_file(metadata[depth]['file_path'], mimetype='image/jpeg')
    else:
        return {"error": "File not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)