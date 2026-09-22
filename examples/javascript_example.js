/**
 * JavaScript / Node.js example - Invoice to JSON Extractor API.
 *
 * Requires Node 18+ (built-in fetch).
 * Get your key: https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1
 */

const API_KEY = 'YOUR_RAPIDAPI_KEY';
const HOST = 'invoice-to-json-extractor1.p.rapidapi.com';
const BASE = `https://${HOST}`;
const HEADERS = {
  'content-type': 'application/json',
  'X-RapidAPI-Key': API_KEY,
  'X-RapidAPI-Host': HOST,
};

async function extract(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

(async () => {
  // 1. Invoice
  const invoice = await extract('/v1/invoice/extract', {
    content:
      'INVOICE\n' +
      'Invoice #: INV-2024-001\n' +
      'Date: 15/03/2024\n' +
      'Vendor: Acme Supplies Ltd.\n' +
      'Total: 132.00 GBP',
    language: 'en',
  });
  console.log('Invoice:', invoice);

  // 2. Receipt
  const receipt = await extract('/v1/receipt/extract', {
    content:
      'ACME COFFEE SHOP\n' +
      'Date: 2024-05-10\n' +
      'Latte 1 4.50 4.50\n' +
      'Total: 4.50 USD\n' +
      'Paid VISA',
  });
  console.log('Receipt:', receipt);

  // 3. Resume
  const resume = await extract('/v1/resume/extract', {
    content:
      'John Smith\n' +
      'john.smith@email.com\n\n' +
      'Skills\n' +
      'Python, Go, PostgreSQL',
  });
  console.log('Resume:', resume);

  // 4. Bank statement
  const bank = await extract('/v1/bank-statement/extract', {
    content:
      'ACME BANK\n' +
      'Account Number: 1234567890\n' +
      '2024-01-05  Salary    +2500.00  7500.00\n' +
      'Closing Balance: 7,500.00 USD',
  });
  console.log('Bank:', bank);
})();
