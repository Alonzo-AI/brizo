# Automated QA using NLP with custom test support

This project automates UI testing for the website using Playwright and OpenAI GPT-based code generation. It supports both standard and custom test commands defined in a JSON test plan.

#  Project Structure

├── sample_tests.json          # JSON test plan with sequential test steps

├── sample_tester.py           # Playwright test script generated dynamically

├── my_custom.py               # Custom test functions written manually

├── lmi_testgen.py             # Main generator script using OpenAI and Playwright

├── class_id_extracter.py      # Utility to extract selectors using OpenAI

## Installation

```bash
python -m venv brizo
source brizo/bin/activate
pip install -r requirements.txt
```

## Step 1: Test Suites

Edit sample_tests.json:
Format
```json
{
  "name": "Test LMI",
  "custom_tests_file": "my_custom.py",
  "nodes": [
    { "type": "action", "command": "Open https://lmidemo.netlify.app" },
    { "type": "action", "command": "Select Auto Insurance" },
    { "type": "custom", "command": "Click continue" },
    { "type": "action", "command": "Fill the 5-digit ZIP code \"12345\"" }
  ]
}
```
Supported node types:

    "action": uses GPT to generate Playwright sync code

    "custom": uses pre-written code from my_custom.py

    "test": for assertions/validation only

# Step 2 : Insert openai key in lmi_testgen.py

# Step 3 : Create or reuse my_custom.py
You can write custom Playwright functions in my_custom.py, such as:
```python
def my_custom_test1(page: Page):
    class_name = class_id_extracter.get_class(page, ".continue-button", "Button with the text 'continue'")
    my_button = page.query_selector(class_name)
    if my_button:
        my_button.click()
        time.sleep(1)
```

# Step 4 : Creating & running the Playwright Script
```bash
python lmi_testgen.py sample_tests.json
```


