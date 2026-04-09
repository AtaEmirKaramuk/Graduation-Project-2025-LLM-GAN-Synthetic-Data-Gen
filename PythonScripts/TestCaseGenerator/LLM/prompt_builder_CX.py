from typing import List, Dict


def build_contextual_prompt(fields: List[Dict], num_cases: int) -> str:
    if not fields:
        return "Generate generic web application test cases for a form."

    field_list = ", ".join([field["label"] or field["name"] or "unnamed" for field in fields])
    field_list = field_list.strip()

    return f"""
Generate {num_cases} diverse software test cases for a web app form.

The form includes the following fields: {field_list}

Each test case should include at least one (but not all) of these fields.

Return output as a JSON list in this format:
[
  {{
    "id": "TCxxxx (xxxx being a larger number than 1200)",
    "type": "(functional, security etc)",
    "description": "(what does this test case do)",
    "steps": [
    ],
    "expected_result": ""
  }}
]

For example:
[
  {{
    "id": "TC018",
    "type": "negative",
    "description": "Login with both username and password fields empty",
    "steps": [
      "Open the login page",
      "Leave username and password fields empty",
      "Click the login button"
    ],
    "expected_result": "Error message is displayed: 'Username and password required'"
  }}
]

Return only the JSON list. Do not add any comments or explanation.
Make sure the final output is a valid JSON list without any trailing commas or incomplete entries.
End your answer with a test case. Don't add any comments. If you can't finish all 10 of the cases, correctly close all of the parentheses.
""".strip()



def describe_form_fields(fields: List[Dict]) -> str:
    """
    Converts a list of field metadata into a structured English list for the prompt.
    """
    desc = []
    for field in fields:
        label = field["label"] or field["name"] or "unnamed"
        label = label.strip().capitalize()
        f_type = field["type"]
        requirement = "required" if field["required"] else "optional"
        placeholder = field["placeholder"]
        part = f"- {label} ({f_type}, {requirement})"
        if placeholder:
            part += f" – placeholder: \"{placeholder}\""
        desc.append(part)

    return "\n".join(desc)
