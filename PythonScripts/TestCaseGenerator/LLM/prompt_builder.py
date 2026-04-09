from PythonScripts.settings import MAX_ZEPHYR_CASES


def build_prompt(num_cases=MAX_ZEPHYR_CASES):
    return f"""
Generate {num_cases} diverse software test cases for a web app registration form.
Each test case should include at least one of these (but not all of these) fields: First Name, Last Name, Phone, Email, Country, Password.
End your answer with a test case. Don't add any comments. If you can't finish all 10 of the cases, correctly close all of the parentheses.

Return output as a JSON list like this:
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
"""
