import os
import time

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quera.settings')

app = Celery('proj')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# app.conf.broker_url = 'amqp://user:password@localhost:5672/'
app.conf.broker_url = 'redis://localhost:6379/1'


# simple celery task
@app.task(bind=True, ignore_result=True)
def sample_task(self):
    print(f'Request: {self.request!r}')


# celery task with result
app.conf.result_backend = 'redis://localhost:6379/0'


@app.task(bind=True, ignore_result=False)
def compute_square(self, number: int):
    return number ** 2


# retry config

@app.task(bind=False, ignore_result=True, max_retries=3, default_retry_delay=10, autoretry_for=(BaseException,))
def bad_task():
    print(f'going to process, execution time: {time.time()}')
    raise Exception


# django tip


@app.task(bind=True, ignore_result=True)
def print_car(self, car_name: str):
    from .models import Car
    car = Car.objects.get(name=car_name)
    print(f'car: {car.name} from {car.company} processed')


# celery beat for cron jobs

app.conf.beat_schedule = {
    'my-cronjob': {
        'task': 'celery_config.print_hello',
        'schedule': crontab(minute='*/1'),  # Executes every minute
    },
}


@app.task()
def sample_cronjob():
    print('hello')
