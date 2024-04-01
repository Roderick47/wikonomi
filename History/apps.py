from django.apps import AppConfig
from django.db.models.signals import post_save

class HistoryConfig(AppConfig):
    name = 'History'

    def ready(self):
        from . import signals
