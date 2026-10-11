import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import main


class ProtectedExtractionTests(unittest.TestCase):
    def setUp(self):
        self.credentials = patch.multiple(main, PROXY_SECRET='', GATEWAY_TOKEN='synthetic-proxy', ADMIN_TOKEN='synthetic-admin')
        self.credentials.start()
        self.client = TestClient(main.app)

    def tearDown(self):
        self.credentials.stop()

    def test_public_health_and_missing_proxy(self):
        self.assertEqual(self.client.get('/health').status_code, 200)
        self.assertEqual(self.client.post('/v1/invoice/extract', json={'content': 'synthetic'}).status_code, 401)

    def test_metrics_does_not_accept_proxy(self):
        self.assertEqual(self.client.get('/metrics', headers={'X-TNT-Proxy-Secret': 'synthetic-proxy'}).status_code, 401)
        self.assertEqual(self.client.get('/metrics', headers={'Authorization': 'Bearer synthetic-admin'}).status_code, 200)

    def test_synthetic_invoice_total_after_authentication(self):
        body = {'content': 'Invoice No: SYNTHETIC-001\nDate: 2026-10-11\nVendor: Synthetic Demo Ltd\nSubtotal: 100 USD\nTax: 10 USD\nTotal: 110 USD', 'content_type': 'text', 'language': 'en'}
        with patch('app.llm._get_provider', return_value=None):
            response = self.client.post('/v1/invoice/extract', json=body, headers={'X-TNT-Proxy-Secret': 'synthetic-proxy'})
        self.assertEqual(response.status_code, 200)
        invoice = response.json()['invoice']
        self.assertEqual(invoice['invoice_number'], 'SYNTHETIC-001')
        self.assertEqual(invoice['subtotal'], 100)
        self.assertEqual(invoice['tax_amount'], 10)
        self.assertEqual(invoice['total'], 110)


if __name__ == '__main__':
    unittest.main()
