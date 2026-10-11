import unittest
from app.heuristic import extract_invoice_heuristic


class InvoiceTotalLabelTests(unittest.TestCase):
    def test_plain_total_and_subtotal_are_distinct(self):
        invoice = extract_invoice_heuristic('Subtotal: 100 USD\nTax: 10 USD\nTotal: 110 USD')
        self.assertEqual(invoice['subtotal'], 100)
        self.assertEqual(invoice['total'], 110)

    def test_vietnamese_summary_label(self):
        self.assertEqual(extract_invoice_heuristic('Tạm tính: 100\nTổng cộng: 110')['total'], 110)

    def test_stronger_summary_still_wins(self):
        self.assertEqual(extract_invoice_heuristic('Total: 80\nGrand Total: 110')['total'], 110)

    def test_item_and_tax_total_are_not_summary(self):
        self.assertIsNone(extract_invoice_heuristic('Item: Total 20 Qty 2 Unit: 10\nSubtotal: 20\nTotal tax: 2')['total'])


if __name__ == '__main__':
    unittest.main()
