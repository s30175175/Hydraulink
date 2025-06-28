import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from press.models import ShortURL


class TestIndexView:
    def test_index_view_get(self, client):
        response = client.get(reverse('press:index'))
        assert response.status_code == 200
        assert '新增短網址' in response.content.decode('utf-8')

    @pytest.mark.django_db
    def test_post_valid_form(self, client):
        response = client.post(
            reverse('press:index'),
            {'original_url': 'https://example.com', 'note': 'test', 'is_active': True},
        )
        assert response.status_code == 200
        assert ShortURL.objects.exists()
        assert len(ShortURL.objects.first().slug) == 6
        assert '建立成功' in response.content.decode('utf-8')

    @pytest.mark.django_db
    def test_post_custom_slug(self, client):
        response = client.post(
            reverse('press:index'),
            {'original_url': 'https://example.com', 'slug': 'testslug'},
        )
        assert response.status_code == 200
        assert ShortURL.objects.filter(slug='testslug').exists()

    @pytest.mark.django_db
    def test_invalid_scheme(self, client):
        response = client.post(reverse('press:index'), {'original_url': 'http://localhost'})
        assert '請以 http:// 或 https:// 開頭的網站，且不可為內部網址。' in response.content.decode(
            'utf-8'
        )


class TestRedirectView:
    @pytest.mark.django_db
    def test_valid_slug_redirect(self, client):
        url = ShortURL.objects.create(slug='test', original_url='https://example.com/')
        response = client.get(reverse('press:redirect', kwargs={'slug': 'test'}))
        assert response.status_code == 302
        assert response.url == 'https://example.com/'

    @pytest.mark.django_db
    def test_non_existent_slug_returns_404(self, client):
        response = client.get(reverse('press:redirect', kwargs={'slug': 'notfound'}))
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_inactive_slug_returns_404(self, client):
        ShortURL.objects.create(
            slug='inactive', original_url='https://example.com/', is_active=False
        )
        response = client.get(reverse('press:redirect', kwargs={'slug': 'inactive'}))
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_redirect_password_page(self, client):
        ShortURL.objects.create(
            slug='secret', original_url='https://example.com/', password=make_password('123456')
        )
        response = client.get(reverse('press:redirect', kwargs={'slug': 'secret'}))
        assert response.status_code == 200
        assert '請輸入密碼' in response.content.decode('utf-8')

    @pytest.mark.django_db
    def test_correct_password_redirect_orignial_url(self, client):
        ShortURL.objects.create(
            slug='secret', original_url='https://example.com/', password=make_password('123456')
        )
        response = client.post(
            reverse('press:redirect', kwargs={'slug': 'secret'}), {'password': '123456'}
        )
        assert response.status_code == 302
        assert response.url == 'https://example.com/'

    @pytest.mark.django_db
    def test_wrong_password_error_message(self, client):
        ShortURL.objects.create(
            slug='secret', original_url='https://example.com/', password=make_password('123456')
        )
        response = client.post(
            reverse('press:redirect', kwargs={'slug': 'secret'}), {'password': 'wrong'}
        )
        assert response.status_code == 200
        assert '密碼錯誤' in response.content.decode('utf-8')
