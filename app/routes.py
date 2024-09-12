from flask import Blueprint, render_template, url_for, flash, redirect
from app import db
from app.forms import Registration, LoginForm, LogoutForm, TaskForm
from app.models import User, Task, Reminder
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from app.utils import send_task_reminder
from flask_mail import Message
from datetime import timedelta


# Define the blueprint
auth_bp = Blueprint('auth', __name__)

# # Testing email sending functionality
# @auth_bp.route('/dashboard/test-email')
# @login_required
# def task_reminder():
# 	subject = "Test Email"
# 	recipient = "bitwebtechnologies@gmail.com"

# 	try:
# 		print("Calling send_email function...")
# 		send_task_reminder(current_user, task, reminder_date)
# 		print("Email sending function called successfully.")
# 		return "Test email sent successfully"
# 	except Exception as e:
# 		print(f"An error occurred: {e}")
# 		return f"An error occurred: {str(e)}"

# User registration route
@auth_bp.route('/index')
@auth_bp.route('/')
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
	form = Registration()
	if form.password.data != form.confirm_password.data:
			flash('Passwords do not match', 'danger')
			print("Passwords do not match")
			return redirect(url_for('auth.register'))

	if form.validate_on_submit():
		# Check if username or email already exist
		existing_user = User.query.filter_by(username=form.username.data).first()
		existing_email = User.query.filter_by(email=form.email.data).first()

		if existing_user:
			flash('Username already exist, Please choose a different username', 'danger')
			return redirect(url_for('auth.register'))

		if existing_email:
			flash('Email already exist. Please use a different email', 'danger')
			return redirect(url_for('auth.register'))

		hashed_password = generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created', 'success')
		return redirect(url_for('auth.login'))

	return render_template('register.html', form=form)

# Adding task route
@auth_bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task(): 
	form = TaskForm()
	if form.validate_on_submit():
		try:
			task = Task(
				title=form.title.data,
				description=form.description.data,
				start_date=form.start_date.data,
				due_date=form.due_date.data,
				user_id=current_user.id			
			)
			db.session.add(task)
			db.session.commit()

			if task.id is None:
				print("Task ID is not generated.")
			else:
				print(f"Task ID after commit: {task.id}")
				
			flash('Task has been added', 'success')
			return redirect(url_for('auth.dashboard'))
		except Exception as e:
			print(f"Error occurred: {str(e)}")  # Catch and print any errors
			db.session.rollback()  # Rollback in case of failure
			flash('An error occurred while adding the task', 'danger')
	return render_template('add_task.html', form=form)

# Edit task route
@auth_bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
	task = Task.query.get_or_404(task_id)
	if task.user_id != current_user.id:
		flash('You are not authorized to edit this task,', 'danger')
		return redirect(url_for('auth.dashboard'))

	form = TaskForm(obj=task)

	if form.validate_on_submit():
		task.title = form.title.data
		task.description = form.description.data
		task.start_date = form.start_date.data
		task.due_date = form.due_date.data
		task.completed = form.completed.data
		db.session.commit()
		flash('Task updated successfully!', 'success')
		return redirect(url_for('auth.dashboard'))

	if form.errors:
		print("Form Errors:", form.errors)

	return render_template('edit_task.html', form=form, task=task)

# Delete task route
@auth_bp.route('/delete_task/<int:task_id>', methods=['POST', 'GET'])
@login_required
def delete_task(task_id):
	task = Task.query.get_or_404(task_id)
	if task.user_id != current_user.id:
		flash('you are not authorized to delete this task', 'danger')
		return redirect(url_for('auth.dahboard'))

	db.session.delete(task)
	db.session.commit()
	flash('Task has been deleted', 'success')
	return redirect(url_for('auth.dashboard'))

# View task details
@auth_bp.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task_details(task_id):
	task = Task.query.get_or_404(task_id)
	reminders = Reminder.query.filter_by(task_id=task_id).all()
	return render_template('tasks_details.html', task=task, reminders=reminders)

# # Deleting reminder
# @auth_bp.route('/delete-reminder/<int:reminder_id>', methods=['POST', 'GET'])
# @login_required
# def delete_reminder(reminder_id):
# 	reminder = Reminder.query.get_or_404(reminder_id)
# 	db.session.delete(reminder)
# 	db.session.commit()
# 	flash('Reminder deleted successfully!', 'success')
# 	return redirect(url_for('auth.task_details', task_id=reminder.task_id))


# Checkbox route for task completeion
@auth_bp.route('/toggle_complete/<int:task_id>', methods=['POST'])
@login_required
def toggle_complete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('You are not authorized to update this task.', 'danger')
        return redirect(url_for('auth.dashboard'))

    task.completed = not task.completed
    db.session.commit()
    flash('Task status updated', 'success')
    return redirect(url_for('auth.dashboard'))


# User login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and check_password_hash(user.password_hash, form.password.data):
			login_user(user)
			flash('Logged in successfully!', 'success')
			return redirect(url_for('auth.dashboard'))
		else:
			flash('Invalid username or password', 'danger')
	return render_template('login.html', form=form)


# Logout route
@auth_bp.route('/logout',methods=['POST','GET'])
@login_required
def logout():
	logout_user()
	flash('You have been logged out', 'warning')
	return redirect(url_for('auth.login'))

# Dashboard route
@auth_bp.route('/dashboard')
@login_required
def dashboard():
	form = LogoutForm()
	tasks = Task.query.filter_by(user_id=current_user.id).all()
	return render_template('dashboard.html', tasks=tasks, form=form, user=current_user)


