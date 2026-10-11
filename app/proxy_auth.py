"""Proxy authentication helpers; empty or UI-redacted values never authorize."""
import hmac


def configured(value):
    value = (value or '').strip()
    if value.lower() in ('<redacted>', '[redacted]', 'redacted', '********', 'changeme'):
        return ''
    return value


def authorized(headers, path, proxy_secret, admin_token='', gateway_token=''):
    if path in ('/health', '/docs', '/openapi.json', '/redoc', '/', '/robots.txt', '/sitemap.xml'):
        return True
    admin = configured(admin_token)
    if path == '/metrics':
        return bool(admin and hmac.compare_digest(headers.get('authorization', '').encode('utf-8'), ('Bearer ' + admin).encode('utf-8')))
    for header, value in (('x-rapidapi-proxy-secret', proxy_secret), ('x-tnt-proxy-secret', gateway_token)):
        secret = configured(value)
        if secret and hmac.compare_digest(headers.get(header, '').encode('utf-8'), secret.encode('utf-8')):
            return True
    return False
