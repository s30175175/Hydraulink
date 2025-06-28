from urllib.parse import parse_qs, urlparse

from django.contrib import messages
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import ShortURLForm
from .models import ShortURL
from .utils.rate_limit import check_rate_limit
from .utils.shortener import create_slug
from .utils.validators import safe_url, valid_url


class IndexView(FormView):
    template_name = 'index.html'
    form_class = ShortURLForm
    success_url = '.'

    def form_valid(self, form):
        short_url = form.save(commit=False)
        ip = self.request.META.get('REMOTE_ADDR')
        original_url = valid_url(short_url.original_url)

        if ShortURL.objects.filter(slug=short_url.slug).exists():
            messages.error(self.request, '此短網址已存在。')
            return self.form_invalid(form)

        while not short_url.slug:
            slug = create_slug()
            if not ShortURL.objects.filter(slug=slug).exists():
                short_url.slug = slug

        if not original_url:
            messages.error(self.request, '請以 http:// 或 https:// 開頭的網站，且不可為內部網址。')
            return self.form_invalid(form)

        if not safe_url(original_url):
            messages.error(self.request, '網址有安全疑慮，來源：Google Safe Browsing')
            return self.form_invalid(form)

        if not check_rate_limit(ip):
            messages.error(self.request, '請求過於頻繁，請稍後再試。')
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

        return render(
            self.request, self.template_name, {'form': self.get_form(), 'slug': short_url.slug}
        )
