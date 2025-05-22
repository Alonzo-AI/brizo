import json
import time
import re
from playwright.sync_api import Page
import openai

openai.api_key="Insert api key here"
PROMPT_TEMPLATE = '''Extract the class name or id name for the given test case from the HTML. Strictly output only class name or id name. with it's respective "." or "#"
📥 Input:
HTML: {html}
Test case: {command}
'''

def remove_style_script(html: str) -> str:
    """
    Removes all <style> and <script> blocks from the given HTML string.

    Args:
        html (str): The HTML content as a string.

    Returns:
        str: The cleaned HTML without any <style> or <script> tags and their content.
    """
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    return html

def extract_html_from_url(page: Page, url: str) -> str:
    """
    Extracts the HTML content from the given URL using the provided Playwright page.

    Args:
        page (Page): The Playwright page instance.
        url (str): The URL to navigate to and extract HTML from.

    Returns:
        str: The HTML content of the page after navigation.
             Returns an empty string if no URL is provided.
    """
    if not url:
        print("⚠️ No URL provided.")
        return ""
    return page.content()

def call_openai_for_test_function(html: str, command: str) -> str:
    """
    Sends a prompt to OpenAI to generate a Playwright test function based on the given HTML and command.

    Args:
        html (str): The HTML content of the web page to analyze.
        command (str): A natural language command describing the test action to generate.

    Returns:
        str: The code returned by OpenAI, expected to be a Python test function as a string.
    """
    prompt = PROMPT_TEMPLATE.format(html=html, command=command)

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000
    )

    return response.choices[0].message['content'].strip()

def get_class(page: Page,default, command: str) -> str:
    """
    Attempts to locate a UI element on the page using a default selector.
    If not found, it sends the page HTML and a natural language description
    to OpenAI to extract the selector.

    Args:
        page (Page): The current Playwright page object.
        default (str): A default CSS selector to try first.
        command (str): A natural language description of the element to find.

    Returns:
        str: A selector string for the desired element, either the default or AI-extracted.
    """
    url = page.url
    html = extract_html_from_url(page, url)
    html = remove_style_script(html)
    button=page.query_selector(default)
    if button is None:
        print("Default button not found...extracting button")
        class_or_id = call_openai_for_test_function(html, command)
        print(f"🔍 Extracted selector: {class_or_id}")
    else:
        class_or_id=button
    return class_or_id
