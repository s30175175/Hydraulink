from urllib.parse import parse_qs, urlparse

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.edit import FormView

from .forms import ShortURLForm
from .models import ShortURL
from .utils.metadata import fetch_description
from .utils.rate_limit import check_rate_limit
from .utils.shortener import create_slug
from .utils.validators import safe_url, valid_url


class IndexView(FormView):
    template_name = 'press/index.html'
    form_class = ShortURLForm
    success_url = '.'

    def form_valid(self, form):
        short_url = form.save(commit=False)
        ip = self.request.META.get('REMOTE_ADDR')
        original_url = valid_url(short_url.original_url)

        if short_url.slug and (not 6 <= len(short_url.slug) <= 8 or not short_url.slug.isalnum()):
            self._error_message = '短碼請介於6-8位，且只支援英數字。'
            return self.form_invalid(form)

        if short_url.password and (
            not 6 <= len(short_url.password) <= 8 or not short_url.password.isalnum()
        ):
            self._error_message = '密碼請介於6-8位，且只支援英數字。'
            return self.form_invalid(form)
        if short_url.password:
            short_url.password = make_password(short_url.password)

        while not short_url.slug:
            slug = create_slug()
            if not ShortURL.objects.filter(slug=slug).exists():
                short_url.slug = slug

        if not original_url:
            self._error_message = '請以 http:// 或 https:// 開頭的網站，且不可為內部網址。'
            return self.form_invalid(form)

        if not safe_url(original_url):
            self._error_message = '網址有安全疑慮，來源：Google Safe Browsing'
            return self.form_invalid(form)

        if not check_rate_limit(ip):
            self._error_message = '請求過於頻繁，請稍後再試。'
            return self.form_invalid(form)

        short_url.original_url = original_url

        parsed = urlparse(original_url)
        query_dict = parse_qs(parsed.query)
        utm_fields = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']
        for utm in utm_fields:
            setattr(short_url, utm, query_dict.get(utm, [None])[0])

        if self.request.user.is_anonymous:
            short_url.is_active = True
        else:
            short_url.create_by = self.request.user

        short_url.save()
        messages.success(self.request, '建立成功')

        form = ShortURLForm()

        return render(self.request, self.template_name, {'form': form, 'slug': short_url.slug})

    def form_invalid(self, form):
        if hasattr(self, '_error_message'):
            messages.error(self.request, self._error_message)
        else:
            messages.error(self.request, '此短網址已存在。')
        return super().form_invalid(form)


class RedirectView(View):
    def get(self, request, slug):
        short_url = get_object_or_404(ShortURL, slug=slug, is_active=True)

        if short_url.password:
            return render(request, 'press/password.html', {'slug': slug, 'note': short_url.note})

        short_url.click_count += 1
        short_url.save()

        return redirect(short_url.original_url)

    def post(self, request, slug):
        short_url = get_object_or_404(ShortURL, slug=slug, is_active=True)
        input_password = request.POST.get('password')

        if short_url.password and check_password(input_password, short_url.password):
            return redirect(short_url.original_url)

        else:
            messages.error(self.request, '密碼錯誤，請再試一次。')
            return render(request, 'press/password.html', {'slug': slug})


class MetadataFetchView(View):
    def get(self, request):
        url = request.GET.get('url')
        if not url:
            return redirect('press:index')

        try:
            note = fetch_description(url)
            return JsonResponse({'success': True, 'result': note})
        except Exception:
            return JsonResponse({'success': False})


class ToggleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        short_url = get_object_or_404(ShortURL, slug=slug, create_by=request.user)

        short_url.is_active = not short_url.is_active
        short_url.save()

        return redirect('users:shorturl_list')
