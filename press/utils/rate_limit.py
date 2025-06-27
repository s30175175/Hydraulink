from django.core.cache import cache


def check_rate_limit(ip, timeout=60):
    count = cache.get(ip)

    if count and count >= 5:
        return False
    elif count is None:
        cache.set(ip, 1, timeout=timeout)
    else:
        cache.incr(ip)
    return True
