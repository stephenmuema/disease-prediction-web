import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django_apscheduler.jobstores import logger
# Create scheduler to run in a thread inside the application process
from django_apscheduler.models import DjangoJobExecution

from api.models import Test

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def my_scheduled_job():
    pass