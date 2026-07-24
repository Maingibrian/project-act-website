from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    
    timings = {}
    
    def handle_request(request):
        if request.resource_type in ('script', 'stylesheet', 'image', 'media', 'font'):
            timings[request.url] = {
                'start': time.time(),
                'type': request.resource_type
            }
    
    def handle_response(response):
        if response.url in timings:
            timings[response.url]['end'] = time.time()
    
    page.on('request', handle_request)
    page.on('response', handle_response)
    
    print("Navigating to index.html...")
    start = time.time()
    page.goto('http://localhost:8080/index.html', wait_until='load', timeout=60000)
    end = time.time()
    
    total_time = end - start
    print(f"Total load time (load event): {total_time:.3f}s")
    
    # Wait for any remaining resources
    time.sleep(2)
    
    metrics = page.evaluate('''() => {
        const nav = performance.getEntriesByType('navigation')[0];
        if (nav) {
            return {
                dns: nav.domainLookupEnd - nav.domainLookupStart,
                tcp: nav.connectEnd - nav.connectStart,
                ttfb: nav.responseStart - nav.requestStart,
                download: nav.responseEnd - nav.responseStart,
                domInteractive: nav.domInteractive - nav.startTime,
                domComplete: nav.domComplete - nav.startTime,
            };
        }
        return {};
    }''')
    
    print("\nPerformance Timing:")
    for k, v in metrics.items():
        if v > 0:
            print(f"  {k}: {v:.0f}ms")
    
    resources = {}
    for url, data in timings.items():
        rtype = data['type']
        resources[rtype] = resources.get(rtype, 0) + 1
    
    print(f"\nResource counts: {resources}")
    
    transfer_size = page.evaluate('''() => {
        let total = 0;
        const entries = performance.getEntriesByType('resource');
        for (const entry of entries) {
            if (entry.transferSize) total += entry.transferSize;
        }
        return total;
    }''')
    print(f"Total transfer size: {transfer_size / 1024 / 1024:.2f} MB")
    
    page.screenshot(path='.kilo/plans/index_load.png', full_page=True)
    print("Screenshot saved to .kilo/plans/index_load.png")
    
    browser.close()
