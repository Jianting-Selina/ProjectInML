from flask import Blueprint, request, jsonify, current_app

from app.services.detection_service import (
    get_patient_detections, get_detection_by_id, create_detection,
    create_report, get_report_by_detection
)
import os

detection_bp = Blueprint('detection_bp', __name__)

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