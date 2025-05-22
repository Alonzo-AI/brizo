
import class_id_extracter
import time
import sys
from pathlib import Path
from playwright.sync_api import Page
def my_custom_test1(page: Page):
    """
    A custom test function performing user-defined actions on the page.

    This function can include any specific logic such as interacting with elements,
    clicking buttons, filling forms, or other browser automation steps as needed.
    """
    # Custom Logic
    class_name = class_id_extracter.get_class(page,".continue-button","Button with the text 'continue'")
    my_button=page.query_selector(class_name)
    if my_button:
        my_button.click()
        time.sleep(1)


    
    