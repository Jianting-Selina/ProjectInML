import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

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

    DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite')
    DB_NAME = os.getenv('DB_NAME', 'brain_tumor_default_db.sqlite')
    DB_USERNAME = os.getenv('DB_USERNAME', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', '')
    DB_PORT = os.getenv('DB_PORT', '')

    if DB_ENGINE == 'sqlite':
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, DB_NAME)}'
    elif DB_ENGINE == 'postgresql':
        SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    elif DB_ENGINE == 'mysql':
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}




