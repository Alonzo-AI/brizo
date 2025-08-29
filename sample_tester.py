from playwright.sync_api import sync_playwright, Page
import time
import sys
from pathlib import Path
import my_custom

def f1(page: Page):
    page.goto("https://lmidemo.netlify.app")
    time.sleep(1)

def f2(page: Page):
    auto_tile = page.query_selector('div.tile[data-id="auto"]')
    if auto_tile:
        auto_tile.click()
        time.sleep(1)

def f4(page: Page):
    zip_input = page.query_selector("#zip-code")
    zip_input.fill("12345")
    time.sleep(1)

def run_all_tests(upto=999):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://lmidemo.netlify.app")

        test_functions = {
            1: f1,
            2: f2,
            3: my_custom.my_custom_test1,
            4: f4,
        }

        import re
        for i in range(1, upto + 1):
            if i in test_functions:
                print("running test_functions", i)
                test_functions[i](page)

                html = page.content()
                html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
                html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
                with open("current_html.html", "w", encoding="utf-8") as f:
                    f.write(html)

        print("Success")
        browser.close()

if __name__ == '__main__':
    import sys
    from playwright.sync_api import sync_playwright, Page
    import my_custom
    upto = int(sys.argv[1]) if len(sys.argv) > 1 else 999
    run_all_tests(upto)
