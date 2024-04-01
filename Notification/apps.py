from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = 'Notification'

    def ready(self):
        from . import signals
