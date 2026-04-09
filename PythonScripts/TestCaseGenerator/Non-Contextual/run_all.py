import os
import sys
import json

from Utils.data_utils import extract_all_valid_test_cases

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils.tokenizer import build_vocab_from_json, load_vocab
from SeqGAN.train_seqgan import SeqGANTrainer
from LLM.prompt_builder import build_prompt
from LLM.LLM_api import query_LLM
from PythonScripts.settings import (
    SEQGAN_CONFIG, USE_LLM, LLM_API_KEY, MAX_LLM_CASES,
    VOCAB_PATH, TRAIN_JSON_PATHS, OUTPUT_PATH, LLM_JSON_PATH, USE_GPU
)

def maybe_generate_with_LLM(LLM_output_path: str = LLM_JSON_PATH):
    if not USE_LLM:
        return
    print(f"\n[1] Requesting {MAX_LLM_CASES} test cases from LLM...")
    prompt = build_prompt(MAX_LLM_CASES)

    print("[2] Querying LLM API...")
    output = query_LLM(prompt, api_key=LLM_API_KEY)

    # For debugging purposes, you can uncomment the following lines to see the full LLM response
    '''
    print("\nFull LLM response:")
    print("=" * 60)
    print(output.strip())
    print("=" * 60 + "\n")
    '''

    valid_cases = extract_all_valid_test_cases(output)

    if valid_cases:
        print(f"Extracted {len(valid_cases)} valid test case(s).")
        with open(LLM_output_path, "w") as f:
            json.dump(valid_cases, f, indent=2)
    else:
        print("No usable test cases found.")
        with open(LLM_output_path, "w") as f:
            json.dump([], f)

    print(f"Saved LLM cases to {LLM_output_path}")
def main():
    json_paths = list(TRAIN_JSON_PATHS)
    if USE_LLM:
        maybe_generate_with_LLM(LLM_output_path=LLM_JSON_PATH)
        json_paths.append(LLM_JSON_PATH)

    print("\n[3] Building vocabulary...")
    build_vocab_from_json(json_paths, vocab_path=VOCAB_PATH)

    print("[4] Loading vocabulary...")
    vocab, _, _ = load_vocab(VOCAB_PATH)

    print("\n[5] Training GAN...")
    config = SEQGAN_CONFIG
    config["output_path"] = OUTPUT_PATH or "non-contextual_generated_cases.txt"

    trainer = SeqGANTrainer(config=config, vocab=vocab, gpu=USE_GPU)
    combined_data = []
    for path in json_paths:
        with open(path, 'r') as f:
            combined_data.extend(json.load(f))
    with open("combined_train.json", "w") as f:
        json.dump(combined_data, f)
    trainer.run_pipeline("combined_train.json")
    print(f"\nDone! Generated cases saved to: {config['output_path']}")



if __name__ == "__main__":
    main()
