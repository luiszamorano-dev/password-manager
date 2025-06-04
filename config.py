import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-valery-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///valery.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False