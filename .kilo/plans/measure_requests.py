from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    requests_made = []
    
    def handle_request(request):
        if request.resource_type in ('script', 'stylesheet', 'image', 'media', 'font'):
            requests_made.append({
                'url': request.url,
                'type': request.resource_type,
                'time': time.time()
            })
    
    def handle_response(response):
        if response.request.resource_type in ('script', 'stylesheet', 'image', 'media', 'font'):
            for req in requests_made:
                if req['url'] == response.url and 'size' not in req:
                    try:
                        body = response.body()
                        req['size'] = len(body) if body else 0
                    except:
                        req['size'] = 'unknown'
                    req['status'] = response.status
    
    page.on('request', handle_request)
    page.on('response', handle_response)
    
    print("Measuring requests...")
    page.goto('http://localhost:8080/index.html', wait_until='load', timeout=120000)
    time.sleep(3)
    
    total_size = sum(r.get('size', 0) for r in requests_made if isinstance(r.get('size'), int))
    print(f"Total requests: {len(requests_made)}")
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    print("\nDetails:")
    for req in requests_made:
        size_str = f"{req['size'] / 1024 / 1024:.2f} MB" if isinstance(req.get('size'), int) else str(req.get('size', '?'))
        print(f"  {req['type']}: {req['url'].split('/')[-1][:60]} - {size_str}")
    
    browser.close()
