import pytest


@pytest.mark.django_db
def test_404_status_code(client):
    response = client.get('/thispagedoesnotexist/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_404_custom_template(client):
    response = client.get('/no-such-url/')
    assert 'Not Found' in response.content.decode('utf-8')
