from flask import Blueprint, request, jsonify,render_template
import logging
import os
from datetime import datetime

def setup_logger(log_dir="logs"):
    """
    Sets up the logger for the NeuroScan Brain Tumor Detection application.
    
    Args:
        log_dir (str): Directory where log files will be stored
    
    Returns:
        logger: Configured logger object
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f"neuroscan_{timestamp}.log")
    
    # Create a logger
    logger = logging.getLogger("NeuroScan")
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("NeuroScan Brain Tumor Detection application initialized")
    
    return logger

# Example of how to use the logger in your main application file:

# At the beginning of your application
logger = setup_logger()
# end log

from app.services.patient_service import (
    get_all_patients, get_patient_by_id, search_patients,
    create_patient, update_patient, delete_patient
)

patient_bp = Blueprint('patient_bp', __name__, template_folder='../../views')


# front-end route start
@patient_bp.route('/form', methods=['GET'])
def patient_form():
    return render_template('form.html') 

@patient_bp.route('/list', methods=['GET'])
def get_patients_list():
    return render_template('list.html')

@patient_bp.route('/detection', methods=['GET'])
def patient_detection():
    return render_template('detection.html')

# front-end route end





@patient_bp.route('/', methods=['GET'])
@patient_bp.route('', methods=['GET'])
def get_patients():
    search_term = request.args.get('search', '')
    if search_term:
        patients = search_patients(search_term)
    else:
        patients = get_all_patients()
    return jsonify(patients)


@patient_bp.route('/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(patient)

@patient_bp.route('', methods=['POST'])
def add_patient():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    required_fields = ['name', 'age', 'gender', 'phone']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    patient = create_patient(data)
    return jsonify(patient), 201


@patient_bp.route('/<patient_id>', methods=['PUT'])
def update_patient_route(patient_id):
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    patient = update_patient(patient_id, data)
    
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    return jsonify(patient)

@patient_bp.route('/<patient_id>', methods=['DELETE'])
def remove_patient(patient_id):
    success = delete_patient(patient_id)
    if not success:
        return jsonify({"error": "Patient not found"}), 404
    
    return jsonify({"message": "Patient deleted successfully"})