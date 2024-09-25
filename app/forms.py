from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User

# Registration form
class Registration(FlaskForm):
	firstname = StringField('firstname: ', validators=[DataRequired()])
	lastname = StringField('lastname: ', validators=[DataRequired()])
	username = StringField('Username: ', validators=[DataRequired()])
	email = StringField('Email: ', validators=[DataRequired(), Email()])
	phone = StringField('Phone: ', validators=[DataRequired()])
	password = PasswordField('Password: ', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password: ', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

# Edit profile form
class EditProfileForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	phone = StringField('Phone', validators=[DataRequired()])
	submit =SubmitField('Update Profile')

	# checks if username exist before editing username
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username has already been taken.')

	# checks if email exist before editing email
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already exist')

# login form
class LoginForm(FlaskForm):
	username = StringField('Username: ', validators=[DataRequired()])
	password = PasswordField('Password: ', validators=[DataRequired()])
	submit = SubmitField('Login')

# logout form
class LogoutForm(FlaskForm):
	submit  = SubmitField('Logout')

# task form
class TaskForm(FlaskForm):
	title = StringField('Title: ', validators=[DataRequired()])
	description = StringField('Description: ', validators=[DataRequired()])
	start_date = DateTimeField('Start Date: ', format='%Y-%m-%d', validators=[DataRequired()])
	due_date = DateTimeField('Due Date: ', format='%Y-%m-%d', validators=[DataRequired()])
	completed = BooleanField('Task completed: ')
	reminder_time = IntegerField('Reminder Time (days before due date)',  default=1, validators=[DataRequired()])
	submit = SubmitField('Add Task')