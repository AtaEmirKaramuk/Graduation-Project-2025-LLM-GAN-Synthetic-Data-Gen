from typing import List, Dict


def build_contextual_prompt_automatic(fields: List[Dict], num_cases: int) -> str:
    if not fields:
        return "Generate generic web application test cases for a form."

    field_list = ", ".join([field.get("label") or field.get("name") or "unnamed" for field in fields])
    field_list = field_list.strip()

    return f"""
    
Generate {num_cases} diverse software test cases for a web app form that has readable steps for Selenium.

The form includes the following fields: {field_list}

Each test case should include at least one (but not all) of these fields.

Return output as a JSON list in this format:
[
  {{
  "id": "TCxxxx (xxxx being a extremely random number that is larger than 1200 up to 100000)",
  "type": "(functional, security etc)",
  "steps": [(each value in brackets until the hard bracket is a step, you need to give at least one step and as many as 5) 
    {{
      "action": "(enter, click, refresh, submit, etc.)",
      "by": "(id, name, class_name, link_text, xpath, css_selector)",
      "value": "(must be a field name exactly as given in form fields)",
      "use_data_key": "(must be a field name exactly as given in form fields)"
    }}
  ],
  "expected_result": "(what will happen when this case is complete)"
  }}
]

For example:
[
  {{
  "id": "GEN_56145",
  "type": "functional",
  "description": "",
  "steps": [
    {{
      "action": "enter",
      "by": "id",
      "value": "email",
      "use_data_key": "email"
    }},
    {{
      "action": "enter",
      "by": "id",
      "value": "password",
      "use_data_key": "password"
    }},
    {{
      "action": "click",
      "by": "id",
      "value": "loginBtn"
    }}
  ],
  "expected_result": "user dashboard visible"
  }}
]

Return only the JSON list. Do not add any comments or explanation.
Make sure the final output is a valid JSON list without any trailing commas or incomplete entries.
End your answer with a test case. Don't add any comments. If you can't finish all {num_cases} of the cases, correctly close all of the parentheses.
""".strip()



def describe_form_fields(fields: List[Dict]) -> str:
    """
    Converts a list of field metadata into a structured English list for the prompt.
    """
    desc = []
    for field in fields:
        label = field.get("label") or field.get("name") or "unnamed"
        label = label.strip().capitalize()
        f_type = field.get("type", "unknown")
        requirement = "required" if field.get("required", False) else "optional"
        placeholder = field.get("placeholder", "")
        part = f"- {label} ({f_type}, {requirement})"
        if placeholder:
            part += f" – placeholder: \"{placeholder}\""
        desc.append(part)

    return "\n".join(desc)
