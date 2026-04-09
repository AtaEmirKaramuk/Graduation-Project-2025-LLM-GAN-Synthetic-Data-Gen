import os
import json
import pandas as pd
import pickle
from ctgan import CTGAN

from PythonScripts.TestDataProject.generated_mode.dynamic_field_parser import (
    query_groq_llama,
    extract_field_list_or_dataframe,
    extract_form_fields,
    build_groq_prompt_from_fields
)
from PythonScripts.TestDataProject.generated_mode.dynamic_ctgan_trainer import create_mock_dataframe

# Directory paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DATASET_PATH = os.path.join(BASE_DIR, "data", "base_dataset_2000.csv")
MODEL_PATH = os.path.join(BASE_DIR, "generated_mode", "models", "ctgan_model_generated.pkl")

WEB_INPUT_DIR = os.path.join(BASE_DIR, "web_input_module", "inputs")
WEB_OUTPUT_DIR = os.path.join(BASE_DIR, "web_input_module", "outputs")

def load_config():
    default = {
        "sample_count": 250,
        "training_rows": 500,
        "max_epochs": 5,
        "output_dir": "outputs",
        "model_output_path": "models/ctgan_model_generated.pkl",
        "log_level": "info"
    }
    config_path = os.path.join(BASE_DIR, "generated_mode", "generated_config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            return {**default, **user_config}
    except Exception as e:
        print("Warning: Config file could not be loaded, defaults will be used:", e)
        return default

def is_basedataset_format(df):
    expected = {'First Name', 'Last Name', 'Phone', 'Email', 'Country', 'Password'}
    return set(df.columns) == expected

def build_filename_from_columns(df, prefix, folder):
    columns = df.columns[:3] if len(df.columns) >= 3 else df.columns
    name_part = "_".join(c.strip().replace(" ", "").replace(",", "") for c in columns if c)
    name_part = name_part[:50] or "data"
    i = 1
    while True:
        filename = f"{prefix}_{name_part}_{i}.csv"
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            return path
        i += 1

def save_web_input_csv(df, prefix="llm_raw"):
    os.makedirs(WEB_INPUT_DIR, exist_ok=True)
    path = build_filename_from_columns(df, prefix, WEB_INPUT_DIR)
    df.to_csv(path, index=False)
    print(f"Input CSV saved: {path}")

def save_web_output_csv(df, prompt_label="url"):
    os.makedirs(WEB_OUTPUT_DIR, exist_ok=True)
    path = build_filename_from_columns(df, f"generated_{prompt_label}", WEB_OUTPUT_DIR)
    df.to_csv(path, index=False)
    print(f"Synthetic data saved: {path}")

def train_ctgan(df, config, prompt_label="url"):
    if df.empty:
        print("Error: Data is empty, CTGAN training canceled.")
        return

    df = df.dropna(axis=0)

    drop_cols = []
    for col in df.columns:
        nunique = df[col].nunique(dropna=True)
        if nunique <= 1:
            print(f"Warning: Column '{col}' dropped (unique value count: {nunique})")
            drop_cols.append(col)

    df = df.drop(columns=drop_cols)

    if df.empty:
        print("Warning: Data is empty after cleaning. CTGAN training canceled.")
        return

    df = df.iloc[:df.shape[0] - (df.shape[0] % 2)]

    if os.path.exists(MODEL_PATH):
        print("Loading existing CTGAN model...")
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
    else:
        print("Creating new CTGAN model...")
        model = CTGAN(batch_size=64, pac=2, verbose=(config.get("log_level") == "debug"))

    print("Starting CTGAN training...")
    model.fit(df, discrete_columns=df.select_dtypes(include="object").columns.tolist(),
              epochs=int(config.get("max_epochs", 5)))
    print("Training completed.")

    sample_df = model.sample(config["sample_count"])
    save_web_output_csv(sample_df, prompt_label=prompt_label)

def process_url_to_data(url):
    config = load_config()

    if not url:
        print("Error: URL is empty or missing.")
        return

    print(f"Form URL: {url}")
    fields = extract_form_fields(url)

    if not fields:
        print("Error: No fields found. Unable to analyze form.")
        return

    prompt = build_groq_prompt_from_fields(fields, config["training_rows"])

    print(f"Prompt:\n{prompt[:1500]}...\n")
    llm_output = query_groq_llama(prompt)
    print(f"LLM Output (truncated):\n{llm_output[:1500]}...\n")
    result = extract_field_list_or_dataframe(llm_output)

    base_df = pd.read_csv(BASE_DATASET_PATH) if os.path.exists(BASE_DATASET_PATH) else pd.DataFrame()

    if isinstance(result, pd.DataFrame):
        print("LLM output: CSV format detected")
        save_web_input_csv(result, prefix="llm_raw_url")
        merged_df = pd.concat([base_df, result], ignore_index=True) if is_basedataset_format(result) else result
        train_ctgan(merged_df, config, prompt_label="url")

    elif isinstance(result, list):
        print("LLM output: Field list detected — generating mock data")
        mock_df = create_mock_dataframe(result, config["training_rows"])
        save_web_input_csv(mock_df, prefix="mock_generated_url")
        merged_df = pd.concat([base_df, mock_df], ignore_index=True) if is_basedataset_format(mock_df) else mock_df
        train_ctgan(merged_df, config, prompt_label="url")

    else:
        print("Error: LLM output not recognized, training canceled.")
