from django.apps import AppConfig
from django.conf import settings


# from djangoHealthAnalytics import settings


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from . import crons
        if settings.SCHEDULER_AUTOSTART:
            crons.start()
