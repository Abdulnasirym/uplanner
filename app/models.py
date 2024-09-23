from datetime import datetime
from app import db
from flask_login import UserMixin

# Stores registered user infromation
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(64), nullable=False)
	lastname = db.Column(db.String(64), nullable=False)
	username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(120), nullable=False)
	phone = db.Column(db.String(20), unique=True, nullable=False)
	tasks = db.relationship('Task', backref='owner', lazy=True)

	def __repr__(self):
		return f'<user {self.username}>'

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

# Stores tasks created by users
class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(500), nullable=False)
	start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	due_date = db.Column(db.DateTime)
	completed = db.Column(db.Boolean, default=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	reminders = db.relationship('Reminder', backref='task', cascade='all, delete-orphan', passive_deletes=True)

	def __repr__(self):
		return f'<Task {self.title}>'

# Handles reminders for tasks
class Reminder(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	send_at = db.Column(db.DateTime, nullable=False)
	sent = db.Column(db.Boolean, default=False)
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

	def __repr__(self):
		return f'<Reminder for Task {self.task_id} at {self.reminder_time}>'
