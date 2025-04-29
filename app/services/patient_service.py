from app import db
from app.models.db_models import Patient
import random
import string

def get_all_patients():
    """Get all patients from the database"""
    patients = Patient.query.order_by(Patient.registration_date.desc()).all()
    return [patient.to_dict() for patient in patients]

def get_patient_by_id(patient_id):
    """Get patient by patient_id"""
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        return patient.to_dict()
    return None

def search_patients(search_term):
    """Search patients by name or ID"""
    if not search_term:
        return get_all_patients()
    
    search_pattern = f"%{search_term}%"
    patients = Patient.query.filter(
        (Patient.name.like(search_pattern)) |
        (Patient.patient_id.like(search_pattern))
    ).all()
    return [patient.to_dict() for patient in patients]

def create_patient(patient_data):
    """Create a new patient record"""
    # Generate a unique patient ID (PT followed by 5 digits)
    patient_id = 'PT' + ''.join(random.choice(string.digits) for _ in range(5))
    
    # Check if ID already exists, regenerate if needed
    while Patient.query.filter_by(patient_id=patient_id).first():
        patient_id = 'PT' + ''.join(random.choice(string.digits) for _ in range(5))
    
    new_patient = Patient(
        patient_id=patient_id,
        name=patient_data.get('name'),
        age=patient_data.get('age'),
        gender=patient_data.get('gender'),
        phone=patient_data.get('phone'),
        symptoms=patient_data.get('symptoms')
    )
    
    db.session.add(new_patient)
    db.session.commit()
    
    return new_patient.to_dict()

def update_patient(patient_id, patient_data):
    """Update an existing patient record"""
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if not patient:
        return None
    
    patient.name = patient_data.get('name', patient.name)
    patient.age = patient_data.get('age', patient.age)
    patient.gender = patient_data.get('gender', patient.gender)
    patient.phone = patient_data.get('phone', patient.phone)
    patient.symptoms = patient_data.get('symptoms', patient.symptoms)
    
    db.session.commit()
    return patient.to_dict()

def delete_patient(patient_id):
    """Delete a patient record"""
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if not patient:
        return False
    
    db.session.delete(patient)
    db.session.commit()
    return True