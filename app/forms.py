from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class Registration(FlaskForm):
	username = StringField('Username: ', validators=[DataRequired()])
	email = StringField('Email: ', validators=[DataRequired(), Email()])
	password = PasswordField('Password: ', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password: ', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('sign Up')

	# def validate_password(self, field):
	# 	if len(field.data) < 8:
	# 		raise ValidationError('Password must be at least 8 characters long.')

class LoginForm(FlaskForm):
	username = StringField('Username: ', validators=[DataRequired()])
	password = PasswordField('Password: ', validators=[DataRequired()])
	submit = SubmitField('Login')

class LogoutForm(FlaskForm):
	submit  = SubmitField('Logout')

class TaskForm(FlaskForm):
	title = StringField('Title: ', validators=[DataRequired()])
	description = StringField('Description: ', validators=[DataRequired()])
	start_date = DateTimeField('Start Date: ', format='%Y-%m-%d', validators=[DataRequired()])
	due_date = DateTimeField('Due Date: ', format='%Y-%m-%d', validators=[DataRequired()])
	completed = BooleanField('Task completed: ')
	reminder_time = IntegerField('Reminder Time (days before due date)',  default=1, validators=[DataRequired()])
	submit = SubmitField('Add Task')