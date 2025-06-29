from django.urls import path

from . import views

app_name = 'press'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('note/', views.MetadataFetchView.as_view(), name='note'),
    path('<slug:slug>/', views.RedirectView.as_view(), name='redirect'),
    path('<slug:slug>/toggle', views.ToggleView.as_view(), name='toggle'),
]
