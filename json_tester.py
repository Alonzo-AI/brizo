from playwright.sync_api import sync_playwright, Page
import time
import sys
from pathlib import Path

def f1(page: Page):
    page.goto("https://lmidemo.netlify.app")
    time.sleep(1)

def f3(page: Page):
    tile = page.query_selector('div.tile[data-id="auto"]')
    if tile:
        tile.click()
        time.sleep(1)

def f4(page: Page):
    selected_policy = page.query_selector("#selected-policy")
    time.sleep(1)
    assert selected_policy is not None
    content = selected_policy.inner_text()
    time.sleep(1)
    assert "Selected: Auto Insurance" in content

def f5(page: Page):
    continue_button = page.query_selector("#continue-btn")
    if continue_button:
        continue_button.click()
        time.sleep(1)

def f6(page: Page):
    zip_input = page.query_selector("#zip-code")
    zip_input.fill("12345")
    time.sleep(1)

def f7(page: Page):
    business_name_input = page.query_selector("#business-name")
    business_name_input.fill("qwerty")
    time.sleep(1)

def f8(page: Page):
    textarea = page.query_selector("#business-description")
    textarea.fill("wertju")
    time.sleep(1)

def f9(page: Page):
    start_quote_button = page.query_selector("#submit-btn")
    start_quote_button.click()
    time.sleep(1)

def run_all_tests(upto=999):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://lmidemo.netlify.app")

        test_functions = {
            1: f1,
            3: f3,
            4: f4,
            5: f5,
            6: f6,
            7: f7,
            8: f8,
            9: f9,
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
