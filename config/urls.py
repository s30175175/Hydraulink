from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('press.urls')),
    path('users/', include('users.urls')),
]


def custom_404_view(request, exception):
    return render(request, 'press/404.html', status=404)


handler404 = 'config.urls.custom_404_view'
