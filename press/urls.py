from django.urls import path

from . import views

app_name = 'press'

urlpatterns = [path('', views.IndexView.as_view(), name='index')]
