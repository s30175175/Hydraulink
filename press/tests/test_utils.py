import time

from django.core.cache import cache

from press.utils.metadata import fetch_description
from press.utils.rate_limit import check_rate_limit
from press.utils.shortener import create_slug
from press.utils.validators import safe_url, valid_url


def test_create_slug_length():
    assert len(create_slug(length=8)) == 8


def test_create_slug_unique():
    slugs = [create_slug() for _ in range(100)]
    assert len(set(slugs)) == 100


def test_valid_url_scheme():
    assert valid_url('example.com') is False
    assert valid_url('abc://example.com') is False
    assert valid_url('http://example.com/') == 'http://example.com/'
    assert valid_url('https://example.com/') == 'https://example.com/'


def test_valid_url_slash():
    assert valid_url('https://example.com/') == 'https://example.com/'
    assert valid_url('https://example.com') == 'https://example.com/'


def test_valid_url_localhost():
    assert valid_url('https://localhost:8000/') is False
    assert valid_url('https://127.0.0.1/') is False


def test_safe_url():
    assert safe_url('https://www.google.com/') is True
    assert safe_url('http://malware.testing.google.test/testing/malware/') is False


def test_fetch_description():
    desc = fetch_description('https://www.google.com')
    assert isinstance(desc, str)


def test_check_rate_limit_allow():
    ip = '127.0.0.1'
    cache.delete(ip)

    for _ in range(5):
        assert check_rate_limit(ip, timeout=2) is True


def test_check_rate_limit_block():
    ip = '127.0.0.2'
    cache.delete(ip)

    for _ in range(5):
        assert check_rate_limit(ip, timeout=2) is True

    assert check_rate_limit(ip, timeout=2) is False


def test_check_rate_limit_allow_after_limit():
    ip = '127.0.0.3'
    cache.delete(ip)

    for _ in range(5):
        assert check_rate_limit(ip, timeout=2) is True

    assert check_rate_limit(ip, timeout=2) is False
    time.sleep(3)
    assert check_rate_limit(ip, timeout=2) is True
