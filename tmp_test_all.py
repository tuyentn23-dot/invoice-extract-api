import sys, io, json, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
NL = chr(10)
base = 'https://invoice-extract-api-4eq9.onrender.com'

receipt = 'RECEIPT #R-2026-091' + NL + 'Date: 2026-10-10' + NL + 'Store: Corner Market' + NL + 'Item: Milk Qty: 2 Price: $3.50 Total: $7.00' + NL + 'Item: Bread Qty: 1 Price: $2.50 Total: $2.50' + NL + 'Subtotal: $9.50' + NL + 'Tax: $0.95' + NL + 'Total: $10.45'
po = 'PURCHASE ORDER #PO-2026-045' + NL + 'Date: 2026-10-10' + NL + 'Vendor: Supplier Co' + NL + 'Total: $500.00'
resume = 'John Smith' + NL + 'Email: john@smith.com' + NL + 'Phone: 555-1234' + NL + 'Skills: Python, JS, SQL'

samples = [('invoice', 'INVOICE #INV-2026-042' + NL + 'Date: 2026-10-09' + NL + 'Bill To: Acme Corp' + NL + 'Item: Widget A Qty: 5 Unit: $20.00 Total: $100.00' + NL + 'Subtotal: $100.00' + NL + 'Tax: $10.00' + NL + 'Total Due: $110.00'), ('receipt', receipt), ('purchase-order', po), ('resume', resume)]

for name, content in samples:
    url = base + '/v1/' + name + '/extract'
    try:
        r = requests.post(url, json={'content': content}, timeout=60)
        print('===', name, 'status', r.status_code)
        d = r.json()
        print(json.dumps(d, indent=2)[:700])
    except Exception as e:
        print('===', name, 'ERR', str(e)[:200])
