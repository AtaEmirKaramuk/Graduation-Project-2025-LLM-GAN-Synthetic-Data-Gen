import json
from LLM.prompt_builder import build_prompt
from LLM.LLM_api import query_zephyr
from PythonScripts.settings import (
    ZEPHYR_API_KEY, MAX_ZEPHYR_CASES
)

def run_zephyr():
    print(f" Generating {MAX_ZEPHYR_CASES} test cases from Zephyr...")
    prompt = build_prompt(MAX_ZEPHYR_CASES)
    try:
        output = query_zephyr(prompt, api_key=ZEPHYR_API_KEY)
        try:
            json_text = output[output.index("["): output.rindex("]") + 1]
            parsed = json.loads(json_text)
        except (ValueError, json.JSONDecodeError) as e:
            print(f" Failed to extract valid JSON from Zephyr output:\n{output}")
            raise e
        with open("zephyr_cases.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)
        print("Zephyr test cases saved to zephyr_cases.json")
    except Exception as e:
        print(f" Error generating from Zephyr: {e}")

if __name__ == "__main__":
    run_zephyr()
