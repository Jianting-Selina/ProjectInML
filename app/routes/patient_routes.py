from flask import Blueprint, request, jsonify,render_template
from app.services.patient_service import (
    get_all_patients, get_patient_by_id, search_patients,
    create_patient, update_patient, delete_patient
)

patient_bp = Blueprint('patient_bp', __name__, template_folder='views')

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

@patient_bp.route('/form', methods=['GET'])
def patient_form():
    
    return render_template('form.html')

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