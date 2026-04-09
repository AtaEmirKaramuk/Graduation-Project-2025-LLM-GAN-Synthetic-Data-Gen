from playwright.sync_api import sync_playwright
from typing import List, Dict


def extract_form_fields(url: str, wait_time: int = 3) -> List[Dict]:

    fields = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(wait_time * 1000)  # milliseconds

        elements = page.query_selector_all("input, select, textarea")
        for el in elements:
            tag = el.evaluate("node => node.tagName.toLowerCase()")
            field = {
                "tag": tag,
                "name": el.get_attribute("name") or "",
                "type": el.get_attribute("type") or "text" if tag == "input" else tag,
                "placeholder": el.get_attribute("placeholder") or "",
                "required": el.get_attribute("required") is not None,
                "label": get_associated_label(page, el)
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

    # Use JS to get closest label and handle null
    parent_label_handle = el.evaluate_handle("el => el.closest('label')")
    is_null = parent_label_handle.evaluate("el => el === null")
    if not is_null:
        return parent_label_handle.evaluate("el => el.innerText").strip()

    return ""


