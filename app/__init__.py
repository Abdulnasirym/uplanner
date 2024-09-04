from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
@app.route('/')
def rou():
	return "Welcome asir"

from app import routes, models