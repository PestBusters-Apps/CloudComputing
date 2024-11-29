from flask import Flask, request, jsonify
from ultralytics import YOLO
from torchvision import transforms
from PIL import Image
import io
from waitress import serve

# Load the YOLOv11 model
model = YOLO('final_train.pt')  # Load your YOLOv11 model
model.eval()  # Set the model to evaluation mode

# Initialize Flask app
app = Flask(__name__)

# Define a transform to preprocess the input image
transform = transforms.Compose([
    transforms.Resize((640, 640)),  # Resize to the input size of the model
    transforms.ToTensor(),
])

# Class labels
class_labels = {
    0: "Belalang",
    1: "Kumbang",
    2: "Siput",
    3: "Ulat",
    4: "Kutu Daun"
}

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read the image file
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    
    # Preprocess the image
    img_tensor = transform(img).unsqueeze(0)  # Add batch dimension

    # Make prediction
    results = model(img_tensor)  # Use the model to make predictions

    # Process predictions
    predictions = results[0]  # Get the first result (assuming batch size of 1)
    results_list = []
    
    for box, score, class_index in zip(predictions.boxes.xyxy, predictions.boxes.conf, predictions.boxes.cls):
        if score > 0.5:  # Confidence threshold
            x1, y1, x2, y2 = box.tolist()
            class_name = class_labels.get(int(class_index), "Unknown")  # Get class name or "Unknown"
            results_list.append({
                'bounding_box': [x1, y1, x2, y2],
                'class_label': class_name,
                'confidence': score.item()  # Add confidence score
            })

    return jsonify({'predictions': results_list})

if __name__ == '__main__':
    serve(host='0.0.0.0', port=8888)
