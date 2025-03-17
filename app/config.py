import os
from datetime import timedelta

#class Config:
#    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-brain-tumor-detection'
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/brain_tumor_db'
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
#    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
#    UPLOAD_FOLDER = os.path.join('static', 'uploads')
#    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


#class Config:
#    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-brain-tumor-detection'
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://root:password@localhost/brain_tumor_db'
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
#    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
#    UPLOAD_FOLDER = os.path.join('static', 'uploads')
#    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-brain-tumor-detection'
    # Cambiar PostgreSQL a SQLite
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///brain_tumor_db.sqlite'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/marieth/Documents/Conestoga AI/Project_ML/ProjectInML/brain_tumor_db.sqlite'
    #test for base dir
    basedir = os.environ.get('DATABASE_BASE_DIR')  # Get base directory from environment variable
    if not basedir:
        basedir = os.path.abspath(os.path.dirname(__file__)) # Default to config.py's directory if not set
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'brain_tumor_db.sqlite')


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}