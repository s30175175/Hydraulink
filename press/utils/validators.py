import requests
from django.conf import settings


def valid_url(url):
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        return False
    if not url.endswith('/'):
        url += '/'

    domain = url.split('//', 1)[1]
    if domain.startswith(('localhost', '127.', '192.168.', '10.')):
        return False

    return url


def safe_url(url):
    api_key = settings.GOOGLE_API_KEY

    endpoint = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}'
    body = {
        'client': {'clientId': 'hydraulink', 'clientVersion': '1.0'},
        'threatInfo': {
            'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING'],
            'platformTypes': ['WINDOWS'],
            'threatEntryTypes': ['URL'],
            'threatEntries': [{'url': url}],
        },
    }

    response = requests.post(endpoint, json=body, timeout=5)

    if response.status_code != 200:
        return False

    return response.json() == {}
