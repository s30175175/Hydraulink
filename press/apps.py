from django.apps import AppConfig
from django.conf import settings


class PressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'press'


class PressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'press'

    def ready(self):
        from django.contrib.auth import get_user_model

        if settings.SUPERUSER_USERNAME and settings.SUPERUSER_PASSWORD:
            User = get_user_model()
            if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
                print('Creating superuser...')
                User.objects.create_superuser(
                    username=settings.SUPERUSER_USERNAME,
                    password=settings.SUPERUSER_PASSWORD,
                )
            else:
                print('Superuser already exists.')
