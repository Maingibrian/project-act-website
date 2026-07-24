from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    
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
    
    print("Measuring desktop load times...")
    start = time.time()
    page.goto('http://localhost:8080/index.html', wait_until='load', timeout=120000)
    load_time = time.time() - start
    print(f"Load event at: {load_time:.1f}s")
    
    checkpoints = [0, 2, 5, 10, 15, 20, 30]
    for cp in checkpoints:
        if cp == 0:
            transfer_size = page.evaluate('''() => {
                let total = 0;
                const entries = performance.getEntriesByType('resource');
                for (const entry of entries) {
                    if (entry.transferSize) total += entry.transferSize;
                }
                return total;
            }''')
            video = page.evaluate('''() => {
                const video = document.querySelector('video');
                if (video) {
                    return { readyState: video.readyState, paused: video.paused };
                }
                return null;
            }''')
            print(f"At load: {transfer_size / 1024 / 1024:.2f} MB transferred, video: {video}")
        else:
            time.sleep(cp - (time.time() - start))
            transfer_size = page.evaluate('''() => {
                let total = 0;
                const entries = performance.getEntriesByType('resource');
                for (const entry of entries) {
                    if (entry.transferSize) total += entry.transferSize;
                }
                return total;
            }''')
            video = page.evaluate('''() => {
                const video = document.querySelector('video');
                if (video) {
                    return { readyState: video.readyState, paused: video.paused };
                }
                return null;
            }''')
            total_elapsed = time.time() - start
            print(f"After +{cp}s ({total_elapsed:.0f}s total): {transfer_size / 1024 / 1024:.2f} MB transferred, video: {video}")
    
    browser.close()
