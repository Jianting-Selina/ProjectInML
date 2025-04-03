from flask import Blueprint, request, jsonify, current_app
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from io import BytesIO

from app.services.detection_service import (
    get_patient_detections, get_detection_by_id,
    create_report, get_report_by_detection
)
import os

#MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../training/samplecnn.h5')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../training/vgg16_final_model.h5')
model = load_model(MODEL_PATH)

CLASS_NAMES = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]

# Function to preprocess the image before making the prediction
def preprocess_image(img):
    """Preprocess the image so that the model can interpret it."""
    img = img.resize((160, 160)) 
    img = image.img_to_array(img)  
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  
    return img




detection_bp = Blueprint('detection_bp', __name__)

# POST route to predict tumor class on MRI image
#http://0.0.0.0:5001/api/detections/predict
@detection_bp.route('/predict', methods=['POST'])
def predict_mri():
    """Recibe una imagen de MRI y devuelve la predicción del modelo."""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        img = image.load_img(BytesIO(file.read()), color_mode="rgb")
        img_array = preprocess_image(img) 
        #img_array = process_image_for_vgg(img) 
        
        # Do the prediction
        prediction = model.predict(img_array)
        print("prediction")
        print(prediction)
        predicted_class = CLASS_NAMES[np.argmax(prediction)] 

        return jsonify({"prediction": predicted_class}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@detection_bp.route('/patient/<patient_id>', methods=['GET'])
def get_detections(patient_id):
    detections = get_patient_detections(patient_id)
    if detections is None:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(detections)

@detection_bp.route('/<detection_id>', methods=['GET'])
def get_detection(detection_id):
    detection = get_detection_by_id(detection_id)
    if not detection:
        return jsonify({"error": "Detection not found"}), 404
    return jsonify(detection)

@detection_bp.route('/patient/<patient_id>', methods=['POST'])
def add_detection(patient_id):
    # Check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check if file extension is allowed
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if ext not in current_app.config['ALLOWED_EXTENSIONS']:
        return jsonify({"error": f"File extension .{ext} not allowed"}), 400
    
    result = create_detection(patient_id, file, current_app)
    return jsonify(result), 201

@detection_bp.route('/<detection_id>/report', methods=['POST'])
def add_report(detection_id):
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    required_fields = ['doctor_name', 'comments', 'recommendation']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    report = create_report(detection_id, data)
    if not report:
        return jsonify({"error": "Detection not found"}), 404
    
    return jsonify(report), 201

@detection_bp.route('/<detection_id>/report', methods=['GET'])
def get_report(detection_id):
    report = get_report_by_detection(detection_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report)