from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.UserLogoutView.as_view(next_page='press:index'), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('shorturl-list/', views.ShortURLListView.as_view(), name='shorturl_list'),
]
