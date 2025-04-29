from playwright.sync_api import sync_playwright, Page
import time
import sys
from pathlib import Path

def f1(page: Page):
    page.goto("https://lmidemo.netlify.app")
    time.sleep(1)

def f2(page):
    header = page.query_selector("h1")
    assert header and "Choose Your Insurance Coverage" in header.inner_text()

def f3(page: Page):
    auto_tile = page.query_selector('div.tile[data-id="auto"]')
    if auto_tile:
        auto_tile.click()
        time.sleep(1)

def f4(page):
    selected_policy = page.query_selector("#selected-policy")
    text = selected_policy.inner_text() if selected_policy else ""
    assert "Selected: Auto Insurance" in text

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
    if start_quote_button:
        start_quote_button.click()
        time.sleep(1)

def f10(page):
    header = page.query_selector("h1")
    assert header and "Account information" in header.inner_text()

def f11(page: Page):
    dba_input = page.query_selector("#dba-name")
    dba_input.fill("qwerty")
    time.sleep(1)

def f12(page: Page):
    street_address_input = page.query_selector("#street-address")
    street_address_input.fill("123 Main St")
    time.sleep(1)

def f13(page: Page):
    unit_input = page.query_selector("#unit-number")
    unit_input.fill("Suite 100")
    time.sleep(1)

def f14(page: Page):
    city_input = page.query_selector("#city")
    city_input.fill("Hyderabad")
    time.sleep(1)

def f15(page: Page):
    state_select = page.query_selector("#state")
    state_select.select_option("CA")
    time.sleep(1)

def f16(page: Page):
    fire_district_select = page.query_selector("#fire-district")
    fire_district_select.select_option("PHOENIX FPSA")
    time.sleep(1)

def f17(page: Page):
    phone_input = page.query_selector("#phone-number")
    phone_input.fill("123-456-7890")
    time.sleep(1)

def f18(page: Page):
    select_element = page.query_selector("#legal-entity")
    select_element.select_option("LLC")
    time.sleep(1)

def f19(page: Page):
    agency_input = page.query_selector("#agency-search")
    agency_input.fill("5901106")
    time.sleep(1)

def f20(page: Page):
    next_button = page.query_selector("button.btn:not(.btn-secondary)")
    if next_button:
        next_button.click()
        time.sleep(1)

def f21(page: Page):
    effective_date_input = page.query_selector("#effectiveDate")
    if effective_date_input:
        effective_date_input.evaluate("el => el.removeAttribute('readonly')")
        effective_date_input.fill("04/29/2025")
        time.sleep(1)

def f22(page: Page):
    expiration_input = page.query_selector("#expirationDate")
    if expiration_input:
        expiration_input.evaluate("el => el.removeAttribute('readonly')")
        expiration_input.fill("12/31/2025")
        time.sleep(1)

def f23(page: Page):
    checkbox = page.query_selector("#overrideRate")
    if checkbox:
        checkbox.click()
        time.sleep(1)

def f24(page: Page):
    rate_as_of_date_input = page.query_selector("#rateAsOfDate")
    if rate_as_of_date_input:
        page.evaluate("element => element.removeAttribute('readonly')", rate_as_of_date_input)
        rate_as_of_date_input.fill("04/29/2025")
        time.sleep(1)

def f25(page: Page):
    version_description_input = page.query_selector("#versionDescription")
    if version_description_input:
        version_description_input.fill("0/90 characters")
        time.sleep(1)

def f26(page: Page):
    textarea = page.query_selector("#operationsDescription")
    if textarea:
        textarea.fill("description of business activities")
        time.sleep(1)

def f27(page: Page):
    button = page.query_selector('button.save-button')
    if button:
        button.click()
        time.sleep(1)

def f28(page: Page):
    select = page.query_selector("#business-desc")
    select.select_option(label="Candle Or Candleholders Mfrers (SIC No. 3999)")
    time.sleep(1)

def f29(page: Page):
    radio_labels = page.query_selector_all('label.radio-option')
    for label in radio_labels:
        text = label.inner_text().strip()
        if "2 or more moving violations" in label.evaluate("el => el.previousElementSibling ? el.previousElementSibling.textContent : ''") or \
           "Yes" == text:
            input_elem = label.query_selector('input[type="radio"]')
            if input_elem and label.inner_text().strip() == "Yes":
                input_elem.click()
                time.sleep(1)
                break

def f30(page: Page):
    radio_labels = page.query_selector_all('label.radio-option')
    for label in radio_labels:
        text = label.inner_text().strip()
        if "supporting policy" in label.evaluate("el => el.previousElementSibling ? el.previousElementSibling.textContent : ''").lower():
            # This is not reliable, so we check text of label for Yes/No
            pass
    # Instead, find the question text and then find the next radio group for that question
    questions = page.query_selector_all('div.eligibility-question')
    for question in questions:
        if "supporting policy such as bop" in question.inner_text().lower():
            # The radio group is the next sibling div with class radio-group
            radio_group = question.evaluate_handle("el => el.nextElementSibling")
            radios = radio_group.as_element().query_selector_all('label.radio-option')
            for label in radios:
                if label.inner_text().strip().lower() == "no":
                    input_el = label.query_selector('input[type="radio"]')
                    input_el.click()
                    time.sleep(1)
                    return

def f31(page: Page):
    year_input = page.query_selector("#year-founded")
    if year_input:
        year_input.fill("2010")
        time.sleep(1)

def f32(page: Page):
    fulltime_input = page.query_selector("#fulltime-employees")
    if fulltime_input:
        fulltime_input.fill("5")
        time.sleep(1)

def f33(page: Page):
    part_time_input = page.query_selector("#part-time-employees")
    part_time_input.fill("2")
    time.sleep(1)

def f34(page: Page):
    seasonal_employees_input = page.query_selector("#seasonal-employees")
    seasonal_employees_input.fill("1")
    time.sleep(1)

def f35(page: Page):
    first_name_input = page.query_selector("#first-name")
    if first_name_input:
        first_name_input.fill("John")
        time.sleep(1)

def f36(page: Page):
    last_name_input = page.query_selector("#last-name")
    if last_name_input:
        last_name_input.fill("Doe")
        time.sleep(1)

def f37(page: Page):
    dob_input = page.query_selector("#date-of-birth")
    dob_input.click()
    time.sleep(1)
    month_selector = page.query_selector("#month-selector")
    month_selector.select_option("0")
    time.sleep(1)
    year_selector = page.query_selector("#year-selector")
    year_selector.select_option("1980")
    time.sleep(1)
    calendar_days = page.query_selector_all("#calendar-days .day")
    for day in calendar_days:
        day_text = day.inner_text().strip()
        if day_text == "1" and "other-month" not in day.get_attribute("class"):
            day.click()
            time.sleep(1)
            break

def f38(page: Page):
    home_address_input = page.query_selector("#home-address")
    home_address_input.fill("123 Main St")
    time.sleep(1)

def f39(page: Page):
    city_input = page.query_selector("#city")
    city_input.fill("Phoenix")
    time.sleep(1)

def f40(page: Page):
    state_select = page.query_selector("#state")
    if state_select:
        state_select.select_option("AZ")
        time.sleep(1)

def f41(page: Page):
    zip_input = page.query_selector("#zip")
    if zip_input:
        zip_input.fill("85001")
        time.sleep(1)

def f42(page: Page):
    radio_options = page.query_selector_all('input[name="owner-as-driver"]')
    for option in radio_options:
        parent_label = option.evaluate_handle("node => node.parentElement")
        label_text = parent_label.evaluate("node => node.textContent").strip()
        if "Yes" in label_text:
            option.click()
            time.sleep(1)
            break

def f43(page: Page):
    button = page.query_selector('button.nav-btn.continue-btn')
    if button:
        button.click()
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
            3: f3,
            4: f4,
            5: f5,
            6: f6,
            7: f7,
            8: f8,
            9: f9,
            10: f10,
            11: f11,
            12: f12,
            13: f13,
            14: f14,
            15: f15,
            16: f16,
            17: f17,
            18: f18,
            19: f19,
            20: f20,
            21: f21,
            22: f22,
            23: f23,
            24: f24,
            25: f25,
            26: f26,
            27: f27,
            28: f28,
            29: f29,
            30: f30,
            31: f31,
            32: f32,
            33: f33,
            34: f34,
            35: f35,
            36: f36,
            37: f37,
            38: f38,
            39: f39,
            40: f40,
            41: f41,
            42: f42,
            43: f43,
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
