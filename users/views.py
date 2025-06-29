from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from press.models import ShortURL


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('press:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, '註冊並登入成功')
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('press:index')

    def form_valid(self, form):
        messages.success(self.request, '登入成功')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('press:index')


class ShortURLListView(LoginRequiredMixin, ListView):
    model = ShortURL
    template_name = 'users/shorturl-list.html'
    context_object_name = 'short_urls'

    def get_queryset(self):
        return ShortURL.objects.filter(create_by=self.request.user)
