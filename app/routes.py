from flask import request, Blueprint, render_template, url_for, flash, redirect
from app import db
from app.forms import EditProfileForm, Registration, LoginForm, LogoutForm, TaskForm
from app.models import User, Task, Reminder
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from app.utils import send_task_reminder
from flask_mail import Message
from datetime import timedelta

# Define the blueprint
auth_bp = Blueprint('auth', __name__)

# landing page
@auth_bp.route('/')
@auth_bp.route('/home', methods=['GET'])
def home():
	return render_template('landing_page.html')

# Explore app button
@auth_bp.route('/explore')
def explore_app():
	if current_user.is_authenticated:
		return redirect(url_for('auth.dashboard'))
	else:
		return redirect(url_for('auth.login'))


# user registration
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
	form = Registration()
	# ensures content in both password fields match
	if form.password.data != form.confirm_password.data:
			flash('Passwords do not match', 'danger')
			print("Passwords do not match")
			return redirect(url_for('auth.register'))

	if form.validate_on_submit():
		# Check if username or email already exist
		existing_user = User.query.filter_by(username=form.username.data).first()
		existing_email = User.query.filter_by(email=form.email.data).first()
		existing_phone = User.query.filter_by(phone=form.phone.data).first()

		# checks if a user exist with the same username
		if existing_user:
			flash('Username already exist, Please choose a different username', 'danger')
			return redirect(url_for('auth.register'))

		# checks if a user exist with the same email
		if existing_email:
			flash('Email already exist. Please use a different email', 'danger')
			return redirect(url_for('auth.register'))

		# checks if a user exist with the same phone numeber
		if existing_phone:
			flash('Phone number already registered. Please use a different phone number', 'danger')
			return redirect(url_for('auth.register'))

		# hashed password entered by the users
		hashed_password = generate_password_hash(form.password.data)
		user = User(
			firstname=form.firstname.data,
			lastname=form.lastname.data,
			username=form.username.data,
			email=form.email.data,
			phone=form.phone.data,
			password_hash=hashed_password
		)
		# add user
		db.session.add(user)
		# push user to database
		db.session.commit()
		flash('Your account has been created', 'success')
		return redirect(url_for('auth.login'))

	return render_template('register.html', form=form)

# user profile route
@auth_bp.route('/profile')
def profile():
	form = Registration()
	return render_template('profile.html', user=current_user)

# edit profile
@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	user = current_user
	form = EditProfileForm(obj=user)

	# validates form
	if form.validate_on_submit():
		# Checks if username, email or phone number already exist
		existing_user = User.query.filter(User.username == form.username.data, User.id != user.id).first()
		existing_email = User.query.filter(User.email == form.email.data, User.id != user.id).first()
		existing_phone = User.query.filter(User.phone == form.phone.data, User.id != user.id).first()

		# Checks if phone number is already in use by another user
		if existing_phone:
			flash('Phone number already registered. Please use a different phone number', 'danger')
			return redirect(url_for('auth.edit_profile'))

		# Checks if username is already taken by another user
		if existing_user:
			flash('Username already exist, Please choose a different username', 'danger')
			return redirect(url_for('auth.edit_profile'))

		# Checks if email is already taken by another user
		if existing_email:
			flash('Email already exist. Please use a different email', 'danger')
			return redirect(url_for('auth.edit_profile'))

		# Update the user's details
		user.firstname = form.firstname.data
		user.lastname = form.lastname.data
		user.username = form.username.data
		user.email = form.email.data
		user.phone = form.phone.data

		# Commit changes to the database
		db.session.commit()
		flash('Profile updated successfully!', 'success')
		return redirect(url_for('auth.profile'))

	if form.errors:
		print("Form Errors:", form.errors)

	print(form.data)
	return render_template('edit_profile.html', form=form)

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
	# checks if the current user has the authority to edit task
	if task.user_id != current_user.id:
		flash('You are not authorized to edit this task,', 'danger')
		return redirect(url_for('auth.dashboard'))

	form = TaskForm(obj=task)

	# validate form
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
	# checks if the current user has the authority to delete task
	if task.user_id != current_user.id:
		flash('you are not authorized to delete this task', 'danger')
		return redirect(url_for('auth.dahboard'))

	db.session.delete(task)
	db.session.commit()
	flash('Task has been deleted', 'success')
	return redirect(url_for('auth.dashboard'))

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

# Dashboard route
@auth_bp.route('/dashboard')
@login_required
def dashboard():
	form = LogoutForm()
	tasks = Task.query.filter_by(user_id=current_user.id).all()
	return render_template('dashboard.html', tasks=tasks, form=form, user=current_user)

# User login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# validate form
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		# check is username and password entered match
		if user and check_password_hash(user.password_hash, form.password.data):
			login_user(user)
			# flash('Logged in successfully!', 'success')
			return redirect(url_for('auth.home'))
		else:
			flash('Invalid username or password', 'danger')
	return render_template('login.html', form=form)

# Logout route
@auth_bp.route('/logout',methods=['POST','GET'])
@login_required
def logout():
	logout_user()
	# flash('You have been logged out', 'warning')
	return redirect(url_for('auth.home'))