import json
import re
from typing import List


def merge_json_files(file_paths: List[str], output_path: str):
    merged = []
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            merged.extend(json.load(f))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
    print(f" Combined {len(file_paths)} files into {output_path} ({len(merged)} test cases)")

def extract_all_valid_test_cases(raw_text: str):
    """
    Extracts all complete test cases from raw LLM/LLaMA output,
    even if the JSON array is malformed or cut off.
    """
    pattern = re.compile(
        r'''
        \{
        \s*"id"\s*:\s*"TC\d{4}".*?
        "expected_result"\s*:\s*".*?"
        \s*\}
        ''',
        re.DOTALL | re.VERBOSE
    )

    matches = pattern.findall(raw_text)
    valid_cases = []

    for match in matches:
        try:
            parsed = json.loads(match)
            valid_cases.append(parsed)
        except json.JSONDecodeError:
            try:
                fixed = re.sub(r'(?<!\\)\\(?![nrt"])', r"\\\\", match)
                parsed = json.loads(fixed)
                valid_cases.append(parsed)
            except Exception:
                continue

    return valid_cases

def extract_all_valid_test_cases_automated(raw_text: str):
    """
    Extracts all valid JSON test cases from raw LLM output containing a JSON list.
    Falls back to individual object extraction if overall list parse fails.
    """
    valid_cases = []

    # Try to locate the JSON list
    try:
        start = raw_text.index('[')
        end = raw_text.rindex(']')
        json_block = raw_text[start:end+1]

        # Try parsing as full list first
        parsed_list = json.loads(json_block)
        if isinstance(parsed_list, list):
            valid_cases.extend(parsed_list)
            return valid_cases
    except (ValueError, json.JSONDecodeError):
        pass

    # Fallback: extract individual objects
    pattern = re.compile(
        r'''
        \{
        \s*"id"\s*:\s*"(?:GEN|TC)_?\d+".*?
        "expected_result"\s*:\s*".*?"
        \s*\}
        ''',
        re.DOTALL | re.VERBOSE
    )
    matches = pattern.findall(raw_text)

    for match in matches:
        try:
            parsed = json.loads(match)
            valid_cases.append(parsed)
        except json.JSONDecodeError:
            try:
                fixed = re.sub(r'(?<!\\)\\(?![nrt"])', r"\\\\", match)
                parsed = json.loads(fixed)
                valid_cases.append(parsed)
            except Exception:
                continue

    return valid_cases