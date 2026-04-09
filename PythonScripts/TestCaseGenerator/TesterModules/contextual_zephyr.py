import json
from Utils.field_extractor import extract_form_fields
from LLM.prompt_builder_CX import build_contextual_prompt
from LLM.LLM_api import query_zephyr
from PythonScripts.settings import ZEPHYR_API_KEY


def generate_contextual_test_cases(url: str, num_cases: int = 10, output_path: str = "contextual_cases.json"):
    print(f" Extracting fields from: {url}")
    fields = extract_form_fields(url)

    if not fields:
        print(" No fields found. Generating generic test cases.")
    else:
        print(f" Found {len(fields)} fields. Building contextual prompt...")

    prompt = build_contextual_prompt(fields, num_cases=num_cases)

    try:
        print(" Querying Zephyr API...")
        output = query_zephyr(prompt, api_key=ZEPHYR_API_KEY)

        try:
            json_text = output[output.index("["): output.rindex("]") + 1]
            parsed = json.loads(json_text)
        except (ValueError, json.JSONDecodeError) as e:
            print(f" Failed to extract valid JSON from Zephyr output:\n{output}")
            raise e

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)
        print(f" Contextual test cases saved to {output_path}")

    except Exception as e:
        print(f" Zephyr generation failed: {e}")


# Optional CLI entry
if __name__ == "__main__":
    test_url = "https://demoqa.com/login"  # Replace with your target
    generate_contextual_test_cases(test_url)
