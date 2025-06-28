import pytest
from django.urls import reverse

from press.models import ShortURL


@pytest.mark.django_db
def test_index_view_get(client):
    response = client.get(reverse('press:index'))
    assert response.status_code == 200
    assert '新增短網址' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_post_valid_form(client):
    data = {'original_url': 'https://example.com', 'note': 'test', 'is_active': True}
    response = client.post(reverse('press:index'), data)
    assert response.status_code == 200
    assert ShortURL.objects.exists()
    assert len(ShortURL.objects.first().slug) == 6
    assert '建立成功' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_post_custom_slug(client):
    data = {'original_url': 'https://example.com', 'slug': 'testslug'}
    response = client.post(reverse('press:index'), data)
    assert response.status_code == 200
    assert ShortURL.objects.filter(slug='testslug').exists()


@pytest.mark.django_db
def test_invalid_scheme(client):
    data = {'original_url': 'http://localhost'}
    response = client.post(reverse('press:index'), data)
    assert '請以 http:// 或 https:// 開頭的網站，且不可為內部網址。' in response.content.decode(
        'utf-8'
    )
