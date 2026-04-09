import os
import json
import time

from LLM.prompt_builder_automatic import build_contextual_prompt_automatic
from PythonScripts import settings
from PythonScripts.TestCaseGenerator.Utils.data_utils import extract_all_valid_test_cases_automated
from PythonScripts.TestCaseGenerator.Utils.field_extractor import extract_form_fields
from PythonScripts.TestCaseGenerator.LLM.prompt_builder_CX import build_contextual_prompt
from PythonScripts.TestCaseGenerator.LLM.LLM_api import query_LLM
from PythonScripts.TestCaseGenerator.Utils.tokenizer import build_vocab_from_json, load_vocab
from PythonScripts.TestCaseGenerator.SeqGAN.train_seqgan import SeqGANTrainer
from PythonScripts.settings import (
    SEQGAN_CONFIG,
    LLM_API_KEY,
    MAX_LLM_CASES_CX,
    USE_LLM,
    URL,
    USE_GPU,
    NUM_LLM_RUNS,
    SITE_LLM_CASES_PATH,
    SITE_VOCAB_PATH,
    SITE_GAN_OUTPUT_PATH,
    AUTOMATED, ALL_CASES, TRAIN_JSON_PATHS, BASE_TRAIN_DATA_PATH, SITE_COMBINED_CASES_PATH
)

def maybe_generate_with_LLM(url: str):
    if not USE_LLM:
        return []

    all_cases = []

    for run_idx in range(NUM_LLM_RUNS):
        print(f"\n[Run {run_idx + 1}/{NUM_LLM_RUNS}] Extracting form fields from {url}")
        fields = extract_form_fields(url)

        if not fields:
            print("No fields found. Using generic prompt.")
        else:
            print(f"Found {len(fields)} fields")

        print("[2] Building contextual prompt")

        if AUTOMATED:
            prompt = build_contextual_prompt_automatic(fields, num_cases=MAX_LLM_CASES_CX)
        else:
            prompt = build_contextual_prompt(fields, num_cases=MAX_LLM_CASES_CX)

        print("[3] Querying LLM API...")
        output = query_LLM(prompt, api_key=LLM_API_KEY)

        valid_cases = extract_all_valid_test_cases_automated(output)

        if valid_cases:
            print(f"Extracted {len(valid_cases)} valid test case(s).")
            all_cases.extend(valid_cases)
        else:
            print("No usable test cases found for this run.")

        if run_idx < NUM_LLM_RUNS - 1:
            time.sleep(1.0)

    return all_cases


def main():
    if USE_LLM:
        new_cases = maybe_generate_with_LLM(URL)

        os.makedirs(os.path.dirname(settings.SITE_NEW_CASES_PATH), exist_ok=True)
        # Save new cases to separate temp file
        with open(settings.SITE_NEW_CASES_PATH, "w", encoding="utf-8") as f:
            json.dump(new_cases, f, indent=2)
        print(f"\nNew LLM cases saved to: {settings.SITE_NEW_CASES_PATH}")

        # Load existing cumulative cases if exist
        existing_cases = []
        if os.path.exists(SITE_LLM_CASES_PATH):
            with open(SITE_LLM_CASES_PATH, "r", encoding="utf-8") as f:
                existing_cases = json.load(f)

        # Merge new and existing, deduplicate by ID
        all_cases = existing_cases + new_cases
        seen_ids = set()
        unique_cases = []
        for case in all_cases:
            if case["id"] not in seen_ids:
                unique_cases.append(case)
                seen_ids.add(case["id"])

        # Save updated cumulative cases
        with open(SITE_LLM_CASES_PATH, "w", encoding="utf-8") as f:
            json.dump(unique_cases, f, indent=2)
        print(f"\nUpdated cumulative LLM cases saved to: {SITE_LLM_CASES_PATH}")

    # Build vocab from cumulative file
    if ALL_CASES:
        json_paths = [BASE_TRAIN_DATA_PATH, SITE_LLM_CASES_PATH]
        print("\n[4] Building vocabulary...")
        build_vocab_from_json(json_paths, vocab_path=SITE_VOCAB_PATH)
        print(f"Vocab saved: {SITE_VOCAB_PATH}")
    else:
        print("\n[4] Building vocabulary...")
        build_vocab_from_json([SITE_LLM_CASES_PATH], vocab_path=SITE_VOCAB_PATH)
        print(f"Vocab saved: {SITE_VOCAB_PATH}")

    print("[5] Loading vocabulary...")
    vocab, _, _ = load_vocab(SITE_VOCAB_PATH)

    # GAN
    print("[6] Training GAN...")
    config = dict(SEQGAN_CONFIG)
    config["output_path"] = SITE_GAN_OUTPUT_PATH

    trainer = SeqGANTrainer(config=config, vocab=vocab, gpu=USE_GPU)

    if ALL_CASES:
        combined_data_cx = []
        for path in json_paths:
            with open(path, 'r') as f:
                combined_data_cx.extend(json.load(f))
        os.makedirs(os.path.dirname(settings.SITE_COMBINED_CASES_PATH), exist_ok=True)
        with open(SITE_COMBINED_CASES_PATH, "w") as f:
            json.dump(combined_data_cx, f)
        trainer.run_pipeline(settings.SITE_COMBINED_CASES_PATH)
        print(f"Contextual GAN test cases that are derived from base+LLM saved to {config['output_path']}")
    else:
        trainer.run_pipeline(SITE_LLM_CASES_PATH)
        print(f"Contextual GAN test cases that are derived from LLM to {config['output_path']}")

if __name__ == "__main__":
    main()
