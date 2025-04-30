from playwright.sync_api import sync_playwright, Page
import time
import sys
from pathlib import Path

def f1(page: Page):
    page.goto("https://www.google.com")
    time.sleep(1)

def f2(page: Page):
    search_area = page.query_selector('textarea[aria-label="Search"]')
    if search_area:
        search_area.fill('Alonzo AI')
        time.sleep(1)

def f3(page: Page):
    textarea = page.query_selector("textarea[role='combobox']")
    if textarea:
        textarea.press("Enter")
        time.sleep(1)

def run_all_tests(upto=999):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        test_functions = {
            1: f1,
            2: f2,
            3: f3,
        }

        import re
        for i in range(1, upto + 1):
            if i in test_functions:
                test_functions[i](page)

                # Extract HTML content from the page object
                html = page.content()

                # Clean the HTML by removing <style> and <script> blocks
                html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
                html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
                # Save the cleaned HTML to a file
                with open("current_html.html", "w", encoding="utf-8") as f:
                    f.write(html)

        print("Success")
        browser.close()

if __name__ == '__main__':
    import sys
    from playwright.sync_api import sync_playwright, Page
    upto = int(sys.argv[1]) if len(sys.argv) > 1 else 999
    run_all_tests(upto)
