from time import sleep

from django.db import transaction

from celery_app.models import Car


@transaction.atomic
def create_car(name: str, company: str):
    car = Car.objects.create(name=name, company=company)
    sleep(2)
    return car
