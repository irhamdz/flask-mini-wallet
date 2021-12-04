import os

APP_NAME = os.environ.get('APP_NAME', 'miniwallet')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///miniwallet')
SQLALCHEMY_TRACK_MODIFICATIONS = False