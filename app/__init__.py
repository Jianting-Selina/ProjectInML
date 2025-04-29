from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../views')
    app.config.from_object(config_class)
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(app.static_folder, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Import and register blueprints

    #from app.routes import patient_bp, detection_bp
    #app.register_blueprint(patient_bp, url_prefix='/api/patients')
    #app.register_blueprint(detection_bp, url_prefix='/api/detections')

    from app.routes import patient_bp, detection_bp
    app.register_blueprint(patient_bp, url_prefix='/api/patients')
    app.register_blueprint(detection_bp, url_prefix='/api/detections')

    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app