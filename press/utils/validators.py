def valid_url(url):
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        return False
    if not url.endswith('/'):
        url += '/'
    return url
