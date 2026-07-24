from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.on('request', lambda req: print(f"REQ: {req.resource_type}: {req.url.split('/')[-1][:60]}"))
    page.on('response', lambda res: print(f"RES: {res.request.resource_type}: {res.url.split('/')[-1][:60]} - {res.headers.get('content-length', '?')} bytes"))
    
    print("Measuring with CDP logging...")
    start = time.time()
    page.goto('http://localhost:8080/index.html', wait_until='load', timeout=120000)
    load_time = time.time() - start
    print(f"\nLoad event at: {load_time:.1f}s")
    
    time.sleep(5)
    
    # Get resource sizes via performance API
    resources = page.evaluate('''() => {
        const entries = performance.getEntriesByType('resource');
        return entries.map(e => ({
            name: e.name.split('/').pop(),
            type: e.initiatorType,
            duration: e.duration,
            transferSize: e.transferSize,
            encodedBodySize: e.encodedBodySize
        }));
    }''')
    
    print("\nResource timing entries:")
    for r in resources:
        print(f"  {r['type']}: {r['name'][:50]} - duration: {r['duration']:.0f}ms, transfer: {r['transferSize'] or 0}, encoded: {r['encodedBodySize'] or 0}")
    
    total_transfer = sum(r['transferSize'] or 0 for r in resources)
    total_encoded = sum(r['encodedBodySize'] or 0 for r in resources)
    print(f"\nTotal transfer: {total_transfer / 1024 / 1024:.2f} MB")
    print(f"Total encoded body: {total_encoded / 1024 / 1024:.2f} MB")
    
    browser.close()
