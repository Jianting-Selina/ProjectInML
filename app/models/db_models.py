from app import db
from datetime import datetime
from sqlalchemy.sql import func

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    detections = db.relationship('Detection', backref='patient', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'symptoms': self.symptoms,
            'registration_date': self.registration_date.strftime('%Y-%m-%d')
        }

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    has_tumor = db.Column(db.Boolean, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    tumor_type = db.Column(db.String(50), nullable=True)
    tumor_location = db.Column(db.String(50), nullable=True)
    tumor_size = db.Column(db.String(20), nullable=True)
    detection_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result_image_path = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'image_path': self.image_path,
            'has_tumor': self.has_tumor,
            'confidence': self.confidence,
            'tumor_type': self.tumor_type,
            'tumor_location': self.tumor_location,
            'tumor_size': self.tumor_size,
            'detection_date': self.detection_date.strftime('%Y-%m-%d %H:%M:%S'),
            'result_image_path': self.result_image_path
        }

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detection_id = db.Column(db.Integer, db.ForeignKey('detection.id'), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=True)
    comments = db.Column(db.Text, nullable=True)
    recommendation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    detection = db.relationship('Detection', backref='report', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'detection_id': self.detection_id,
            'doctor_name': self.doctor_name,
            'comments': self.comments,
            'recommendation': self.recommendation,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }