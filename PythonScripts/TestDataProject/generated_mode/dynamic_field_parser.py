import requests
import json
import re
import io
import pandas as pd
from playwright.sync_api import sync_playwright
from PythonScripts.settings import ZEPHYR_API_KEY

# Groq LLaMA 4 API settings
API_URL = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {ZEPHYR_API_KEY}",
    "Content-Type": "application/json"
}

def query_groq_llama(prompt):
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Groq API error: {response.status_code} - {response.text}")
            return ""
    except Exception as e:
        print("LLM API request failed:", e)
        return ""

def clean_llm_csv(raw_text):
    lines = raw_text.strip().splitlines()
    csv_lines = []
    header_found = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not header_found and "," in line and not line.lower().startswith(("the", "generate", "example", "this")):
            header_found = True
            csv_lines.append(line)
        elif header_found:
            if "," in line:
                csv_lines.append(line)
            else:
                break
    return "\n".join(csv_lines)

def extract_field_list_or_dataframe(raw_text):
    try:
        if not raw_text.strip():
            return []

        raw_text = clean_llm_csv(raw_text)
        lines = raw_text.strip().splitlines()
        csv_lines = [line for line in lines if "," in line]

        if len(csv_lines) >= 2:
            df = pd.read_csv(io.StringIO("\n".join(csv_lines)))
            df = df.dropna(how="all")
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
            return df

        match = re.search(r"\[[^\[\]]+\]", raw_text)
        if match:
            return json.loads(match.group(0).replace("'", '"'))

        fields = [line.split("-")[0].strip() for line in lines if "-" in line]
        if fields:
            return fields

        return []
    except Exception as e:
        print("Field/CSV parsing error:", str(e))
        return []

def extract_form_fields(url: str, wait_time: int = 3):
    fields = []
    ignore_keywords = [
        "captcha", "recaptcha", "h-captcha", "slide", "terms", "agreement",
        "privacy", "policy", "checkbox", "consent", "i am", "i agree", "enter the characters"
    ]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(wait_time * 1000)
        elements = page.query_selector_all("input, select, textarea")
        for el in elements:
            input_type = el.get_attribute("type") or ""
            if input_type.lower() == "hidden":
                continue

            tag = el.evaluate("node => node.tagName.toLowerCase()")
            label = get_associated_label(page, el) or el.get_attribute("placeholder") or el.get_attribute("aria-label") or ""
            if not label.strip() and not el.get_attribute("name"):
                continue

            # UPDATED: filter using label, name and placeholder
            label_text = label.strip().lower()
            name_text = (el.get_attribute("name") or "").strip().lower()
            placeholder_text = (el.get_attribute("placeholder") or "").strip().lower()

            if any(bad in label_text for bad in ignore_keywords) or any(bad in name_text for bad in ignore_keywords) or any(bad in placeholder_text for bad in ignore_keywords):
                continue

            field = {
                "tag": tag,
                "name": el.get_attribute("name") or "",
                "type": input_type or "text" if tag == "input" else tag,
                "placeholder": el.get_attribute("placeholder") or "",
                "required": el.get_attribute("required") is not None,
                "label": label.strip()
            }
            fields.append(field)
        browser.close()
    return fields

def get_associated_label(page, el):
    id_attr = el.get_attribute("id")
    if id_attr:
        label = page.query_selector(f"label[for='{id_attr}']")
        if label:
            return label.evaluate("el => el.innerText").strip()
    parent_label_handle = el.evaluate_handle("el => el.closest('label')")
    is_null = parent_label_handle.evaluate("el => el === null")
    if not is_null:
        return parent_label_handle.evaluate("el => el.innerText").strip()
    return ""

def build_groq_prompt_from_fields(fields, num_rows: int = 1000) -> str:
    column_names = []
    for field in fields:
        label = field.get("label") or field.get("name") or field.get("placeholder") or ""
        label = label.strip().replace(",", "")
        if label:
            column_names.append(label)

    # Force column order if standard fields matched
    expected_order = ["First Name", "Last Name", "Phone", "Email", "Country", "Password"]
    if set(column_names) == set(expected_order):
        column_names = expected_order

    header = ",".join(column_names)
    example_row = ",".join(["example" for _ in column_names])

    prompt = f"""Generate 50 rows of realistic fake data in pure CSV format only with the following columns in **this exact order**:
{header}

Do not include explanations, comments, markdown, or code.
Do not output anything other than the CSV data.
The first line must be the header row.
Make sure all columns contain varied and complete values.
Do not include quotes (") in the values.

Example:
{header}
{example_row}
{example_row}
"""
    return prompt
