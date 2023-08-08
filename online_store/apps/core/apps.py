from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_store.apps.core'

    def ready(self):
        import online_store.apps.core.signals
