from playwright.sync_api import sync_playwright
import time

PAGES = [
    ('index.html', 'Homepage'),
    ('donate.html', 'Donate'),
    ('archive.html', 'Archive'),
    ('world-environment-day.html', 'WED'),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for url, name in PAGES:
        page.goto(f'http://localhost:8080/{url}', wait_until='load', timeout=60000)
        load_time = page.evaluate('performance.timing.loadEventEnd - performance.timing.navigationStart') / 1000
        transfer_size = page.evaluate('''() => {
            let total = 0;
            const entries = performance.getEntriesByType('resource');
            for (const entry of entries) {
                if (entry.transferSize) total += entry.transferSize;
            }
            return total;
        }''')
        print(f"{name}: load={load_time:.1f}s, transfer={transfer_size/1024/1024:.2f}MB")
    
    browser.close()
