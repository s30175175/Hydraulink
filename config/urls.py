from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

urlpatterns = [
    path(settings.ADMIN_PATH, admin.site.urls),
    path('', include('press.urls')),
    path('users/', include('users.urls')),
]


def custom_404_view(request, exception):
    return render(request, 'press/404.html', status=404)


handler404 = 'config.urls.custom_404_view'

if settings.SUPERUSER_USERNAME and settings.SUPERUSER_PASSWORD:
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
        print('Creating superuser...')
        User.objects.create_superuser(
            username=settings.SUPERUSER_USERNAME, password=settings.SUPERUSER_PASSWORD
        )
    else:
        print('Superuser already exists.')
