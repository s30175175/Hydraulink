from press.utils.metadata import fetch_description
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


def test_safe_url():
    assert safe_url('https://www.google.com/') is True
    assert safe_url('http://malware.testing.google.test/testing/malware/') is False


def test_fetch_description():
    desc = fetch_description('https://www.google.com')
    assert isinstance(desc, str)
