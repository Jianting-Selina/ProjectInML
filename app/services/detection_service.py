from app import db
from app.models.db_models import Patient, Detection, Report
import os
from werkzeug.utils import secure_filename
from datetime import datetime
#from app.ml_model.model import predict_tumor

def get_patient_detections(patient_id):
    """Get all detections for a specific patient"""
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if not patient:
        return None
    
    detections = Detection.query.filter_by(patient_id=patient.id).order_by(
        Detection.detection_date.desc()).all()
    
    return [detection.to_dict() for detection in detections]

def get_detection_by_id(detection_id):
    """Get a specific detection by ID"""
    detection = Detection.query.get(detection_id)
    if detection:
        return detection.to_dict()
    return None

# def create_detection(patient_id, image_file, app):
#     """Create a new detection for a patient"""
#     patient = Patient.query.filter_by(patient_id=patient_id).first()
#     if not patient:
#          return {"error": "Patient not found"}, 404
    
#     # Save the uploaded image
#     filename = secure_filename(image_file.filename)
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     unique_filename = f"{patient_id}_{timestamp}_{filename}"
    
#     upload_folder = os.path.join(app.static_folder, 'uploads')
#     image_path = os.path.join(upload_folder, unique_filename)
#     image_file.save(image_path)
    
#     # Path for storing in database (relative path)
#     db_image_path = os.path.join('uploads', unique_filename)
    
#     # Process the image with ML model
#     result = predict_tumor(image_path, upload_folder, unique_filename)
    
#     # Create a new detection record
#     new_detection = Detection(
#          patient_id=patient.id,
#          image_path=db_image_path,
#          has_tumor=result['has_tumor'],
#          confidence=result['confidence'],
#          tumor_type=result.get('tumor_type'),
#          tumor_location=result.get('tumor_location'),
#          tumor_size=result.get('tumor_size'),
#          result_image_path=result.get('result_image_path')
#     )
    
#     db.session.add(new_detection) 
#     db.session.commit()
    
#     # Return the result
#     detection_dict = new_detection.to_dict()
#     return detection_dict

def create_report(detection_id, report_data):
    """Create a medical report for a detection"""
    detection = Detection.query.get(detection_id)
    if not detection:
        return None
    
    new_report = Report(
        detection_id=detection_id,
        doctor_name=report_data.get('doctor_name'),
        comments=report_data.get('comments'),
        recommendation=report_data.get('recommendation')
    )
    
    db.session.add(new_report)
    db.session.commit()
    
    return new_report.to_dict()

def get_report_by_detection(detection_id):
    """Get report for a specific detection"""
    report = Report.query.filter_by(detection_id=detection_id).first()
    if report:
        return report.to_dict()
    return None