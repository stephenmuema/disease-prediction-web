import csv
import glob
import os
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django_apscheduler.jobstores import logger
# Create scheduler to run in a thread inside the application process
from django_apscheduler.models import DjangoJobExecution

from api.models import Files

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def my_scheduled_job():
    path=os.path.join(settings.MEDIA_ROOT,'csv')
    os.chdir(path=path)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # export to csv
    combined_csv.to_csv("'{}/data/combined_csv.csv".format(settings.BASE_DIR), index=False, encoding='utf-8-sig')
    # move to data directory
    os.chdir(path="'{}/data/".format(settings.BASE_DIR))
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # export to csv
    combined_csv.to_csv("Diseases.csv", index=False, encoding='utf-8-sig')
    files=Files.objects.all().delete()
