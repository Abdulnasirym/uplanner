from celery import Celery
from celery.schedules import crontab

def make_celery(app):
	celery = Celery(
		app.import_name,
		backend=app.config['CELERY_RESULT_BACKEND'],
		broker=app.config['CELERY_BROKER_URL']
	)
	celery.conf.update(app.config)

	class ContextTask(celery.Task):
		abstract = True
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return super().__call__(self, *args, **kwargs)

	celery.Task = ContextTask

	celery.conf.beat_schedule = {
	'send-reminders-every-10-minutes': {
		'task': 'app.task.send_reminders',
		'schedule': crontab(minute='*/10')
		},
	}

	return celery