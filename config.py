import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


class Config():
	SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_secret_key'

	# Mail configuration
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')