import pandas as pd
import os
import json
import pickle
import random
import string
from ctgan import CTGAN

from PythonScripts.TestDataProject.generated_mode.dynamic_field_parser import query_groq_llama as query_falcon, extract_field_list_or_dataframe
from PythonScripts.settings import CTGAN_CONFIG

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GEN_INPUT_DIR = os.path.join(BASE_DIR, "generated_mode", "inputs")

config = dict(CTGAN_CONFIG)

def create_mock_dataframe(columns, num_rows):
    df = pd.DataFrame()
    for col in columns:
        if "name" in col.lower():
            df[col] = [random.choice(["Ali", "Ayşe", "John", "Emily"]) for _ in range(num_rows)]
        elif "email" in col.lower():
            df[col] = [f"user{random.randint(100,999)}@example.com" for _ in range(num_rows)]
        elif "password" in col.lower():
            df[col] = [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(num_rows)]
        elif "phone" in col.lower():
            df[col] = [f"+90{random.randint(5000000000,5999999999)}" for _ in range(num_rows)]
        elif "country" in col.lower():
            df[col] = [random.choice(["Turkey", "USA", "Germany"]) for _ in range(num_rows)]
        elif "date" in col.lower():
            df[col] = pd.date_range("2000-01-01", periods=num_rows, freq='W').astype(str)
        else:
            df[col] = [f"val{random.randint(1,100)}" for _ in range(num_rows)]
    return df

def is_basedataset_format(df):
    base_columns = {'First Name', 'Last Name', 'Phone', 'Email', 'Country', 'Password'}
    return set(df.columns) == base_columns

def save_input_csv(df, prefix="llm_raw"):
    os.makedirs(GEN_INPUT_DIR, exist_ok=True)
    i = 1
    while True:
        path = os.path.join(GEN_INPUT_DIR, f"{prefix}_{i}.csv")
        if not os.path.exists(path):
            break
        i += 1
    df.to_csv(path, index=False)
    print(f"Input CSV saved: {path}")

def train_ctgan_on_dataframe(df, config):
    if df.empty:
        print("Data is empty, GAN training cancelled.")
        return

    pac = 2
    rows = df.shape[0]
    df = df.iloc[:rows - (rows % pac)]

    model_path = os.path.join(BASE_DIR, config["model_output_path"])
    if os.path.exists(model_path):
        print("Existing CTGAN model is being loaded...")
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    else:
        print("New CTGAN model is being created...")
        model = CTGAN(
            epochs=config.get("max_epochs", 500),
            batch_size=64,
            pac=pac,
            verbose=(config.get("log_level", "info") == "debug")
        )

    print(f"Starting CTGAN training... ({config.get('max_epochs')} epochs)")
    model.fit(df, discrete_columns=df.columns.tolist())
    print("Training completed.")

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print("Model saved:", model_path)

    output_dir = os.path.join(BASE_DIR, config["output_dir"])
    os.makedirs(output_dir, exist_ok=True)

    i = 1
    while True:
        out_path = os.path.join(output_dir, f"generated_data_{i}.csv")
        if not os.path.exists(out_path):
            break
        i += 1

    model.sample(config["sample_count"]).to_csv(out_path, index=False)
    print("Synthetic data saved:", out_path)

if __name__ == "__main__":
    try:
        with open(os.path.join(BASE_DIR, "generated_mode", "field_prompt.json"), encoding="utf-8") as f:
            prompt = json.load(f).get("prompt", "")
    except Exception as e:
        print("Failed to read prompt file:", e)
        exit()

    print("Prompt:", prompt)

    llm_raw = query_falcon(prompt)
    result = extract_field_list_or_dataframe(llm_raw)

    base_path = os.path.join(BASE_DIR, "data", "base_dataset_2000.csv")
    base_df = pd.read_csv(base_path) if os.path.exists(base_path) else pd.DataFrame()

    if isinstance(result, list):
        print("LLM output: field list — generating mock data...")
        mock_df = create_mock_dataframe(result, config["training_rows"])
        save_input_csv(mock_df, prefix="mock_generated")
        merged_df = pd.concat([base_df, mock_df], ignore_index=True) if is_basedataset_format(mock_df) else mock_df
        train_ctgan_on_dataframe(merged_df, config)

    elif isinstance(result, pd.DataFrame):
        print("LLM output: CSV data received.")
        save_input_csv(result, prefix="llm_raw")
        merged_df = pd.concat([base_df, result], ignore_index=True) if is_basedataset_format(result) else result
        train_ctgan_on_dataframe(merged_df, config)

    else:
        print("LLM output could not be recognized. Training cancelled.")
