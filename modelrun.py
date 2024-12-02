from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io

# Load the YOLOv8 model
model = YOLO('final_train.pt')

# Initialize Flask app
app = Flask(__name__)

# Class labels
class_labels = {
    0: "Belalang",
    1: "Kumbang",
    2: "Kutu Daun",
    3: "Siput",
    4: "Ulat"
}

# Threshold per class (berdasarkan indeks kelas)
class_thresholds = {
    0: 0.3,  # Belalang
    1: 0.5,  # Kumbang
    2: 0.3,  # Kutu Daun
    3: 0.2,  # Siput
    4: 0.6   # Ulat
}

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read the image file
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

        # Make prediction (YOLO handles preprocessing internally)
        results = model(img)

        # Process predictions
        predictions = results[0]
        results_list = []
        
        for box, score, class_index in zip(predictions.boxes.xyxy, predictions.boxes.conf, predictions.boxes.cls):
            class_index = int(class_index)
            threshold = class_thresholds.get(class_index, 0.5)  # Default threshold is 0.5
            if score >= threshold:
                x1, y1, x2, y2 = box.tolist()
                class_name = class_labels.get(class_index, "Unknown")
                results_list.append({
                    'bounding_box': [x1, y1, x2, y2],
                    'class_label': class_name,
                    'confidence': float(score)  # Convert to float for JSON
                })
            else:
                results_list.append({
                    'bounding_box': None,
                    'class_label': "Unknown object",
                    'confidence': float(score)
                })

        return jsonify({'predictions': results_list})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
