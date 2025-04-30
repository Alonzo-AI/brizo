import json
import sys
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright, Page
import openai

config = json.loads(open("config.json").read())
#load_dotenv()
openai.api_key = config["openai_api_key"]

PROMPT_TEMPLATE = '''You are an expert QA automation engineer.
Given the HTML of a webpage and a natural language test case description, generate a single Playwright Python test function using the sync API that performs the described task.

✅ Required Constraints:
For commands like "Open https://...", the function must use page.goto("<url>") and nothing else
Use the sync API from playwright.sync_api.
The function name must be f{idx} (e.g., f1, f2, ...).
The function must take a single argument: page: Page.
Only generate one function per request.
Only use page.goto() when the command explicitly asks to open a URL.
Do not include:
  - Browser or context setup (e.g., with sync_playwright(), browser =, page.goto()).
  - if __name__ == "__main__": blocks.
  - No extra functions should be included.
  - Do NOT include run_all_tests function.
Please generate the Python function definitions without including -> None in the function signature.
Use "time.sleep(1)" after each major action (e.g., click, fill).
Do not use expect() or any async methods.
Use query_selector() or query_selector_all() where appropriate.
Use visible label-based selection only if no IDs/classes are found in the HTML.
Do NOT include any prerequisite steps. Only implement the specific task described in the command.
For text verification, use "in" comparisons instead of exact matches (e.g., "expected_text in actual_text") unless the test explicitly requires exact matching.
Ensure no syntax errors, no unclosed strings, proper indentation, and no mixing of sync/async APIs.
Avoid reusing variable names unnecessarily.
Avoid duplicate or redundant actions.
Keep the code clean and modular."
---

📥 Input:
HTML: {html}
Test case: {command}

---

Now, generate the function named f{idx} accordingly. ONLY OUTPUT THE FUNCTION CODE, nothing else.'''

import openai
import time


def call_openai_for_test_function(html, command, idx, node_type):
    prompt = PROMPT_TEMPLATE
    if node_type == "test":
        prompt += "\n\nOnly perform content verification (e.g., using inner_text assertions). Do NOT click, fill, or interact with the page in any way."
    prompt = prompt.format(html=html, command=command, idx=idx)

    # Get the response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1800
    )

    # Extract the content we need to return
    content = response.choices[0].message['content']

    # Prepare the response in the desired format for printing
    result = {
        "id": response.id,
        "object": response.object,
        "created": int(time.time()),  # This will be the current timestamp
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage['prompt_tokens'],
            "completion_tokens": response.usage['completion_tokens'],
            "total_tokens": response.usage['total_tokens']
        },
        "choices": [
            {
                "message": {
                    "role": response.choices[0].message['role'],
                    "content": content
                }
            }
        ]
    }

    # Print the response in JSON-like format
    print(result)
    print(content)
    # Return just the content for function processing
    return content

def clean_generated_code(code: str,idx:int) -> str:
    # Remove code blocks
    code = re.sub(r"python\s*", "", code)
    code = re.sub(r"", "", code)
    code = re.sub(r"```", "", code)
    # Extract only the function definition
    #function_match = re.search(r"def f\d+\(page: Page\):.*?(?=def|\Z)", code, re.DOTALL)
    function_match = re.search(r"def f\d+\(page(?:: Page)?\):.*?(?=^def|\Z)", code, re.DOTALL | re.MULTILINE)

    if function_match:
        code = function_match.group(0).strip()
    else:
        # If the regex didn't match, try a more basic approach
        lines = code.splitlines()
        function_lines = []
        inside_function = False
        
        for line in lines:
            if (line.strip().startswith("def f") and "page: Page" in line) or (line.strip().startswith("def f") and "page" in line):
                inside_function = True
                function_lines.append(line)
            elif inside_function:
                if line.strip().startswith("def ") or line.strip().startswith("with sync_playwright"):
                    inside_function = False
                else:
                    function_lines.append(line)
        
        code = "\n".join(function_lines).strip()
    return code

def extract_html_from_url(page, url: str):
    if not url:
        print("⚠️ No URL available to fetch HTML.")
        return ""
    page.goto(url)
    time.sleep(3)
    return page.content()

def get_existing_function_count():
    if not Path(sys.argv[2]).exists():
        return 0
    with open(sys.argv[2]) as f:
        return len(re.findall(r"^def f\d+\(", f.read(), re.M))

def ensure_script_header():
    file_path = sys.argv[2]
    if not Path(file_path).exists():
        with open(file_path, "w") as f:
            f.write("from playwright.sync_api import sync_playwright, Page\nimport time\nimport sys\nfrom pathlib import Path\n\n")

def append_function_to_test_script(new_func: str):
    # Check if the file exists and read its content
    file_path = sys.argv[2]
    if Path(file_path).exists():
        with open(file_path, "r") as f:
            content = f.read()
        
        # Remove any existing run_all_tests function and __main__ block
        content = re.sub(r"def run_all_tests.*?if __name__ == ['\"]__main__['\"]:.*?run_all_tests\(.*?\)\n?", "", content, flags=re.DOTALL)

        
        # Write the content back without run_all_tests and __main__ block
        if content.strip():
            with open(file_path, "w") as f:
                f.write(content.strip() + "\n\n")
    
    # Append the new function
    with open(file_path, "a") as f:
        f.write(new_func + "\n\n")

import re

def regenerate_run_all_tests(upto: int):
    # Read the existing test file
    with open(sys.argv[2], "r") as f:
        content = f.read()

    # Extract all defined test functions (e.g., f1, f2, ...)
    function_matches = re.findall(r"def (f\d+)\(page(?:: Page)?\):", content)
    function_matches = sorted(function_matches, key=lambda x: int(x[1:]))


    # Start constructing the new run_all_tests block
    run_all_tests = "def run_all_tests(upto=999):\n"
    run_all_tests += "    with sync_playwright() as p:\n"
    run_all_tests += "        browser = p.chromium.launch(headless=False, slow_mo=500)\n"
    run_all_tests += "        context = browser.new_context()\n"
    run_all_tests += "        page = context.new_page()\n"

    # Build the test_functions dictionary
    run_all_tests += "        test_functions = {\n"
    for func in function_matches:
        num = int(func[1:])
        run_all_tests += f"            {num}: {func},\n"
    run_all_tests += "        }\n\n"

    # Loop through range and execute valid functions
    """run_all_tests += "        for i in range(1, upto + 1):\n"
    run_all_tests += "            if i in test_functions:\n"
    run_all_tests += "                test_functions[i](page: Page)\n\n"
    run_all_tests += "                # Save current HTML after each function call\n"
    run_all_tests += "                with open(\"current_html.html\", \"w\", encoding=\"utf-8\") as f:\n"
    run_all_tests += "                    f.write(page.content())\n\n"
    run_all_tests += "        print(\"Success\")\n" """
    run_all_tests += "        import re\n"
    run_all_tests += "        for i in range(1, upto + 1):\n"
    run_all_tests += "            if i in test_functions:\n"
    run_all_tests += "                test_functions[i](page)\n\n"
    run_all_tests += "                # Extract HTML content from the page object\n"
    run_all_tests += "                html = page.content()\n\n"
    run_all_tests += "                # Clean the HTML by removing <style> and <script> blocks\n"
    run_all_tests += "                html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)\n"
    run_all_tests += "                html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)\n"
    run_all_tests += "                # Save the cleaned HTML to a file\n"
    run_all_tests += "                with open(\"current_html.html\", \"w\", encoding=\"utf-8\") as f:\n"
    run_all_tests += "                    f.write(html)\n\n"
    run_all_tests += "        print(\"Success\")\n"

    run_all_tests += "        browser.close()\n\n"

    # Append __main__ block
    run_all_tests += "if __name__ == '__main__':\n"
    run_all_tests += "    import sys\n"
    run_all_tests += "    from playwright.sync_api import sync_playwright, Page\n"
    run_all_tests += "    upto = int(sys.argv[1]) if len(sys.argv) > 1 else 999\n"
    run_all_tests += "    run_all_tests(upto)\n"

    # Remove any old run_all_tests or __main__ block before appending
    content = re.sub(r"if __name__ == ['\"]__main__['\"]:.*?run_all_tests\(upto\)","", content, flags=re.DOTALL)
    try:
        content = re.sub(r"def run_all_tests\(.*?\n(?:    .*\n)*?browser\.close\(\)\n\n", "", content, flags=re.DOTALL)
    except Exception as e:
        print("Regex substitution failed:", e)

    content = content.strip() + "\n\n" + run_all_tests
    # Rewrite the file with new logic
    with open(sys.argv[2], "w") as f:
        f.write(content)

import re

def remove_style_script(html):
    # Remove <style>...</style> blocks (case-insensitive, dot matches newline)
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove <script>...</script> blocks (case-insensitive, dot matches newline)
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    return html

def generate_function_from_test_node(node, idx, prior_nodes):
    command = node["command"]
    url = None
    for past_node in reversed(prior_nodes):
        if past_node["type"] == "action" and past_node["command"].startswith("Open "):
            url = past_node["command"].split("Open ")[1]
            break

    html = ""
    if not command.startswith("Open "):
        # First check if we have a saved HTML file from previous function
        if Path("current_html.html").exists():
            try:
                with open("current_html.html", "r", encoding="utf-8") as f:
                    html = f.read()
                    html= remove_style_script(html)
                print("📄 Using HTML from saved file")
            except Exception as e:
                print(f"⚠️ Error reading HTML file: {e}")
                
        # Fall back to browser extraction if no file or empty file
        if not html and url:
            print("🌐 Extracting HTML from browser")
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False, slow_mo=500)
                context = browser.new_context()
                page = context.new_page()
                html = extract_html_from_url(page, url)
                html= remove_style_script(html)
                with open("current_html.html", "w", encoding="utf-8") as f:
                    f.write(html)
                browser.close()

    generated_code = call_openai_for_test_function(html, command, idx, node["type"])
    return clean_generated_code(generated_code,idx)

def main():
    # Delete existing json_tester.py to start fresh
    if Path(sys.argv[2]).exists():
        try:
            Path(sys.argv[2]).unlink()
            print(f"Removed existing {sys.argv[2]} to start fresh")
        except Exception as e:
            print(f"Warning: Could not remove existing {sys.argv[2]}: {e}")
    
    # Also remove any existing HTML file
    if Path("current_html.html").exists():
        try:
            Path("current_html.html").unlink()
            print("Removed existing current_html.html to start fresh")
        except Exception as e:
            print(f"Warning: Could not remove existing current_html.html: {e}")

    with open(sys.argv[1]) as f:
        plan = json.load(f)

    ensure_script_header()
    total_nodes = len(plan["nodes"])
    for i, node in enumerate(plan["nodes"]):
        idx = i + 1
        if idx <= get_existing_function_count():
            continue
        if node["type"] not in ("action", "test"):
            print("⏭️ Skipping non-action/test node.")
            continue

        print(f"⚙️ Generating f{idx} for: {node['command']}")
        new_func = generate_function_from_test_node(node, idx, plan["nodes"][:idx])
        append_function_to_test_script(new_func)
        regenerate_run_all_tests(idx)
        
        try:
            # Run the test with a timeout to avoid hanging
            subprocess.run(["python", sys.argv[2], str(idx)], timeout=300)
            #subprocess.run(["C:/Users/HP/Desktop/Brizo/venvv/Scripts/python.exe", "json_tester.py", str(idx)], timeout=100)
        except subprocess.TimeoutExpired:
            print(f"⚠️ Test execution timed out for f{idx}")

if __name__ == "__main__":
    main()