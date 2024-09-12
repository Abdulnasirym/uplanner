from flask_mail import Message
from flask import render_template
from app import mail

def send_task_reminder(user, task, reminder_date):
    subject = f"Reminder fortask: {task.title}"
    recipients = [user.email]
    
    html_body = render_template(
        'reminder_email.html',
        task=task,
        reminder_date=reminder_date,
        user=user
    )

    message = Message(subject=subject, recipients=recipients, html=html_body)
    mail.send(message)
