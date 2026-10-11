import unittest
from app.proxy_auth import authorized


class ProxyAuthTests(unittest.TestCase):
    def test_missing_configuration_is_closed(self):
        self.assertFalse(authorized({}, '/v1/invoice/extract', ''))
        self.assertFalse(authorized({'x-rapidapi-proxy-secret': '<redacted>'}, '/v1/invoice/extract', '<redacted>'))

    def test_existing_and_custom_proxy(self):
        self.assertTrue(authorized({'x-rapidapi-proxy-secret': 'synthetic-existing'}, '/v1/invoice/extract', 'synthetic-existing'))
        self.assertTrue(authorized({'x-tnt-proxy-secret': 'synthetic-custom'}, '/v1/invoice/extract', '', gateway_token='synthetic-custom'))
        self.assertFalse(authorized({'x-tnt-proxy-secret': 'wrong'}, '/v1/invoice/extract', '', gateway_token='synthetic-custom'))
        self.assertFalse(authorized({'x-tnt-proxy-secret': 'clé'}, '/v1/invoice/extract', '', gateway_token='synthetic-custom'))

    def test_metrics_is_separate_and_health_public(self):
        self.assertFalse(authorized({'x-rapidapi-proxy-secret': 'synthetic-proxy'}, '/metrics', 'synthetic-proxy', 'synthetic-admin'))
        self.assertTrue(authorized({'authorization': 'Bearer synthetic-admin'}, '/metrics', '', 'synthetic-admin'))
        self.assertFalse(authorized({}, '/metrics', ''))
        self.assertTrue(authorized({}, '/health', ''))


if __name__ == '__main__':
    unittest.main()
