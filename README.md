# Automated QA using NLP

## Installation

```bash
python -m venv brizo
source brizo/bin/activate
pip install -r requirements.txt
```

## Step 1: Test Suites

Create or Reuse test suites in `test_suites` directory.

Format
```json
{
  "name": "Test Google",
  "nodes": [
    {
      "type": "action",
      "command": "Open https://www.google.com"
    },
    {
      "type": "action",
      "command": "Type in 'Alonzo AI' in the search bar"
    },
    {
      "type": "action",
      "command": "Press Enter"
    }
  ]
}
```

### Note : LMI Demo 
LMI Mock Website is hosted at https://lmidemo.netlify.app

`test_suites/lmi_demo.json` contains test cases pertaining to that


## Step 2: Config

Create a `config.json` file.

```json

{
  "openai_api_key": "<INSERT OPENAI KEY HERE>"
}

```

## Step 3: Creating the Playwright Script

```bash
python lmi_testgen.py test_suites/lmi_demo.json lmi_script.py
```

## Step 4: Running the Playwright Script
```bash
python lmi_script.py
```