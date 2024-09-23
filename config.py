import os
from dotenv import load_dotenv

# Load the environment variable
load_dotenv()


class Config():
	SQLALCHEMY_DATABASE_URI = 'postgres://u9ncj702d6l168:p4e35cf1552291ac843038d39fadcc5494171818b67d39768994ecdd9648a078d@c3nv2ev86aje4j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddduh2fehsf73o'
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