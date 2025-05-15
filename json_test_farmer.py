from playwright.sync_api import sync_playwright, Page
import time
import sys
from pathlib import Path

def f1(page):
    page.goto("https://www.farmers.com/")
    import time
    time.sleep(1)

def f2(page: Page):
    # Look for the 'GET A QUOTE' button in the header area and click it
    get_a_quote_btn = None
    header_buttons = page.query_selector_all("a")
    for btn in header_buttons:
        text = btn.inner_text().strip() if btn else ""
        if text == "GET A QUOTE":
            get_a_quote_btn = btn
            break
    if get_a_quote_btn:
        get_a_quote_btn.click()
        time.sleep(1)
    # Now look for the 'Auto' option in the quote options and click it
    auto_option = None
    auto_links = page.query_selector_all("a")
    for link in auto_links:
        text = link.inner_text().strip() if link else ""
        if text == "Auto":
            auto_option = link
            break
    if auto_option:
        auto_option.click()
        time.sleep(1)

def f3(page: Page):
    # Try to find a ZIP code input field by common attributes or placeholder
    zip_input = None
    # Try input[type="text"] with placeholder or aria-label containing 'zip'
    input_elements = page.query_selector_all('input[type="text"]')
    for inp in input_elements:
        placeholder = inp.get_attribute('placeholder') or ''
        aria_label = inp.get_attribute('aria-label') or ''
        name = inp.get_attribute('name') or ''
        if 'zip' in placeholder.lower() or 'zip' in aria_label.lower() or 'zip' in name.lower():
            zip_input = inp
            break
    # If not found, try input[type="tel"] or input[type="number"]
    if not zip_input:
        input_elements = page.query_selector_all('input[type="tel"], input[type="number"]')
        for inp in input_elements:
            placeholder = inp.get_attribute('placeholder') or ''
            aria_label = inp.get_attribute('aria-label') or ''
            name = inp.get_attribute('name') or ''
            if 'zip' in placeholder.lower() or 'zip' in aria_label.lower() or 'zip' in name.lower():
                zip_input = inp
                break
    # If still not found, try any input with 'zip' in id or class
    if not zip_input:
        input_elements = page.query_selector_all('input')
        for inp in input_elements:
            id_attr = inp.get_attribute('id') or ''
            class_attr = inp.get_attribute('class') or ''
            if 'zip' in id_attr.lower() or 'zip' in class_attr.lower():
                zip_input = inp
                break
    # If still not found, fail the test
    if not zip_input:
        raise Exception("ZIP code input field not found on the page.")
    zip_input.click()
    time.sleep(1)
    zip_input.fill('90210')
    time.sleep(1)

def run_all_tests(upto=999):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.farmers.com/")

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
