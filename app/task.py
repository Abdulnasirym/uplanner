from celery import Celery
from datetime import datetime, timedelta
from app import db, Task, mail
from flask_mail import Message
from flask import render_template
from app import current_app

app = create_app()

@celery.task
def send_reminders():
	now =  datetime.utcnow()
	upcoming_tasks = Task.query.filter(Task.due_date > now).all()

	for task in upcoming_tasks:
		reminder_time = task.due_date - timedelta(hours=2)

		if now >= reminder_time and not task.reminder_sent:
			msg = Message(
				subject=f'Reminder: {task.title} is due soon!',
				sender=app.config['MAIL_DEFAULT_SENDER'],
				recipients=[task.user.email]
			)

			msg.html = render_template('reminder_email.html', task=task, user=task.user)

			mail.send(msg)

			task.completed = True
			db.session.commit()