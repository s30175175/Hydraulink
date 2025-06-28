import requests
from bs4 import BeautifulSoup


def fetch_description(url):
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.text, 'lxml')

    description = soup.find('meta', attrs={'name': 'description'}) or soup.find(
        'meta', attrs={'name': 'og:description'}
    )

    if description and description.get('content'):
        return description['content']

    title = soup.find('title')

    if title and title.string:
        return title.string

    return '此頁面無簡介'
