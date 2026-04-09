import json
import os
import sys
import re
import pandas as pd
import pickle
from ctgan import CTGAN

from PythonScripts.settings import CTGAN_CONFIG

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

# Groq-powered LLM functions
from dynamic_field_parser import query_groq_llama as query_falcon, extract_field_list_or_dataframe
from dynamic_ctgan_trainer import create_mock_dataframe

INPUT_DIR = os.path.join(CURRENT_DIR, "inputs")

config = dict(CTGAN_CONFIG)

def is_basedataset_format(df):
    expected = {'First Name', 'Last Name', 'Phone', 'Email', 'Country', 'Password'}
    return set(df.columns) == expected

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9]+', '_', text.lower())[:30]

def save_input_csv(df, prefix="llm_raw"):
    os.makedirs(INPUT_DIR, exist_ok=True)
    i = 1
    while True:
        path = os.path.join(INPUT_DIR, f"{prefix}_{i}.csv")
        if not os.path.exists(path):
            df.to_csv(path, index=False)
            print(f"Input CSV saved: {path}")
            return
        i += 1

def extract_header_from_prompt(prompt: str) -> list:
    match = re.search(r'^([a-zA-Z0-9_ ]+(?:,[a-zA-Z0-9_ ]+)+)', prompt, re.MULTILINE)
    if match:
        header_line = match.group(1)
        fields = [f.strip() for f in header_line.split(",")]
        if all(len(f) > 0 for f in fields):
            return fields
    return []

def train_ctgan_with_memory(df, config, prompt_label=""):
    if df.empty:
        print("Error: Data is empty, CTGAN training cancelled.")
        return

    pac = 2
    df = df.iloc[:df.shape[0] - (df.shape[0] % pac)]

    model_path = os.path.join(CURRENT_DIR, config["model_output_path"])
    if os.path.exists(model_path):
        print("Loading existing CTGAN model...")
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    else:
        print("Creating new CTGAN model...")
        model = CTGAN(
            batch_size=64,
            pac=pac,
            verbose=(config.get("log_level") == "debug")
        )

    print("Starting CTGAN training...")
    model.fit(
        df,
        discrete_columns=df.select_dtypes(include="object").columns.tolist(),
        epochs=int(config.get("max_epochs", 5))
    )
    print("Training completed.")

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print("Model saved:", model_path)

    output_dir = os.path.join(CURRENT_DIR, config["output_dir"])
    os.makedirs(output_dir, exist_ok=True)
    i = 1
    while True:
        out_path = os.path.join(output_dir, f"generated_data_{prompt_label}_{i}.csv")
        if not os.path.exists(out_path):
            model.sample(config["sample_count"]).to_csv(out_path, index=False)
            print("Synthetic data saved:", out_path)
            return
        i += 1

def main():
    prompt_path = os.path.join(CURRENT_DIR, "field_prompt.json")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = json.load(f).get("prompt", "")
    except Exception as e:
        print("Error: Prompt file could not be read:", e)
        return

    print(f"\nPrompt:\n{prompt}\n")
    prompt_label = sanitize_filename(prompt)

    llm_output = query_falcon(prompt)
    print(f"\nLLM Response:\n{llm_output}\n")

    result = extract_field_list_or_dataframe(llm_output)
    guessed_header = extract_header_from_prompt(prompt)

    base_path = os.path.join(CURRENT_DIR, config.get("base_dataset_path"))
    base_df = pd.read_csv(base_path) if os.path.exists(base_path) else pd.DataFrame()

    if isinstance(result, pd.DataFrame):
        if all(isinstance(c, int) or str(c).startswith("Unnamed") for c in result.columns):
            if guessed_header:
                print(f"Warning: Missing header detected, header extracted from prompt: {guessed_header}")
                result.columns = guessed_header
            else:
                print("Warning: Headers missing, default column names assigned: Col1, Col2...")
                result.columns = [f"Col{i+1}" for i in range(result.shape[1])]

        save_input_csv(result, prefix=f"llm_raw_{prompt_label}")
        merged_df = pd.concat([base_df, result], ignore_index=True) if is_basedataset_format(result) else result
        train_ctgan_with_memory(merged_df, config, prompt_label)

    elif isinstance(result, list):
        mock_df = create_mock_dataframe(result, config["training_rows"])
        save_input_csv(mock_df, prefix=f"mock_generated_{prompt_label}")
        merged_df = pd.concat([base_df, mock_df], ignore_index=True) if is_basedataset_format(mock_df) else mock_df
        train_ctgan_with_memory(merged_df, config, prompt_label)

    else:
        print("Error: Invalid LLM output, training cancelled.")

if __name__ == "__main__":
    main()
