import json

from PythonScripts.TestCaseGenerator.Utils.data_utils import extract_all_valid_test_cases
from PythonScripts.TestCaseGenerator.Utils.field_extractor import extract_form_fields
from PythonScripts.TestCaseGenerator.LLM.prompt_builder_CX import build_contextual_prompt
from PythonScripts.TestCaseGenerator.LLM.LLM_api import query_LLM
from PythonScripts.TestCaseGenerator.Utils.tokenizer import build_vocab_from_json, load_vocab, build_vocab_from_sjson
from PythonScripts.TestCaseGenerator.SeqGAN.train_seqgan import SeqGANTrainer
from PythonScripts.settings import (
    SEQGAN_CONFIG,
    VOCAB_PATHCX,
    LLM_API_KEY,
    MAX_LLM_CASES_CX,
    USE_LLM,
    OUTPUT_PATHCX,
    TRAIN_JSON_PATHS,
    URL,
    LLM_JSON_PATHCX,
    USE_GPU,
    NUM_LLM_RUNS, ALL_CASES
)

import time

def maybe_generate_with_LLM(url: str, LLM_output_path: str = LLM_JSON_PATHCX):
    if not USE_LLM:
        return

    all_cases = []

    for run_idx in range(NUM_LLM_RUNS):
        print(f"\n[Run {run_idx + 1}/{NUM_LLM_RUNS}] Extracting form fields from {url}")
        fields = extract_form_fields(url)

        if not fields:
            print("No fields found. Using generic prompt.")
        else:
            print(f"Found {len(fields)} fields")

        print("[2] Building contextual prompt")
        prompt = build_contextual_prompt(fields, num_cases=MAX_LLM_CASES_CX)

        print("[3] Querying LLM API...")
        output = query_LLM(prompt, api_key=LLM_API_KEY)

        valid_cases = extract_all_valid_test_cases(output)

        if valid_cases:
            print(f"Extracted {len(valid_cases)} valid test case(s).")
            all_cases.extend(valid_cases)
        else:
            print("No usable test cases found for this run.")

        # Delay between runs to avoid overwhelming the API
        if run_idx < NUM_LLM_RUNS - 1:
            time.sleep(1.0)

    # Save all cases together after loop
    if all_cases:
        print(f"\nTotal accumulated cases: {len(all_cases)}")
    else:
        print("\nNo test cases extracted in any run.")

    with open(LLM_output_path, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2)

    print(f"Saved all LLM cases to {LLM_output_path}")




def main():
    json_paths = list(TRAIN_JSON_PATHS)

    if USE_LLM:
        maybe_generate_with_LLM(URL, LLM_output_path=LLM_JSON_PATHCX)
        json_paths.append(LLM_JSON_PATHCX)

    if ALL_CASES:
        print("\n[4] Building vocabulary...")
        build_vocab_from_json(json_paths, vocab_path=VOCAB_PATHCX)
    else:
        print("\n[4] Building vocabulary...")
        build_vocab_from_sjson(LLM_JSON_PATHCX, vocab_path=VOCAB_PATHCX)

    print("[5] Loading vocabulary...")
    vocab, _, _ = load_vocab(VOCAB_PATHCX)

    print("[6] Training GAN...")
    config = dict(SEQGAN_CONFIG)
    config["output_path"] = OUTPUT_PATHCX or "contextual_generated_cases.txt"

    trainer = SeqGANTrainer(config=config, vocab=vocab, gpu=USE_GPU)
    combined_data_cx = []
    for path in json_paths:
        with open(path, 'r') as f:
            combined_data_cx.extend(json.load(f))
    with open("combined_train_cx.json", "w") as f:
        json.dump(combined_data_cx, f)
    trainer.run_pipeline("combined_train_cx.json")
    print(f"Contextual GAN test cases saved to {config['output_path']}")


if __name__ == "__main__":
    main()
