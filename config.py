import os

class Config():
	SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_secret_key'
	DEBUG = True