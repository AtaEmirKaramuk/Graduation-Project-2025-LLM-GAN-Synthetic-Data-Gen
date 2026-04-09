import pandas as pd
import os
import pickle
import json
from datetime import datetime
from ctgan import CTGAN
from PythonScripts.TestDataProject.generated_mode.dynamic_ctgan_trainer import create_mock_dataframe
from PythonScripts.TestDataProject.generated_mode.dynamic_field_parser import (
    query_groq_llama,
    extract_field_list_or_dataframe,
    build_groq_prompt_from_fields
)

pd.set_option("display.max_columns", None)

# 1. Directory and path settings
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_path = os.path.join(base_dir, "data", "base_dataset_2000.csv")
model_path = os.path.join(base_dir, "models", "ctgan_model.pkl")
config_path = os.path.join(base_dir, "generated_mode", "generated_config.json")
output_dir = os.path.join(base_dir, "outputs")
inputs_dir = os.path.join(base_dir, "inputs")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(inputs_dir, exist_ok=True)

# Save LLM output as CSV
def save_llm_input_csv(df, prefix="llm_generic"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.csv"
    path = os.path.join(inputs_dir, filename)
    df.to_csv(path, index=False)
    print(f"LLM output saved as input CSV: {path}")

# 2. Load config
default_config = {"use_llm_in_generic": False, "training_rows": 500, "sample_count": 1000}
try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = {**default_config, **json.load(f)}
except Exception as e:
    print("Warning: Config file could not be loaded, default will be used:", e)
    config = default_config

use_llm = config.get("use_llm_in_generic", False)
expected_fields = {"First Name", "Last Name", "Phone", "Email", "Country", "Password"}
expected_order = ["First Name", "Last Name", "Phone", "Email", "Country", "Password"]

# 3. Data generation: via LLM or mock or CSV
if use_llm:
    print("LLM-based synthetic data generation started...")
    sample_fields = list(expected_fields)
    prompt = build_groq_prompt_from_fields(
        [{"label": f} for f in sample_fields],
        num_rows=config["training_rows"]
    )
    raw_output = query_groq_llama(prompt)

    print("Full LLM output:\n" + raw_output[:1500] + "...\n")

    df = extract_field_list_or_dataframe(raw_output)

    if isinstance(df, pd.DataFrame):
        actual = set(df.columns)
        if actual != expected_fields:
            print(f"Error: LLM output does not match expected format!\nExpected: {expected_fields}\nReceived: {actual}")
            exit()
        df = df[expected_order]
        save_llm_input_csv(df)

    elif isinstance(df, list):
        actual = set(df)
        if actual != expected_fields:
            print(f"Error: LLM field list does not match expected format!\nExpected: {expected_fields}\nReceived: {actual}")
            exit()
        df = create_mock_dataframe(df, config["training_rows"])
        df = df[expected_order]
        save_llm_input_csv(df)

    else:
        print("Error: LLM output not recognized. Process aborted.")
        exit()

else:
    print("Loading standard dataset file...")
    df = pd.read_csv(data_path)

df.dropna(inplace=True)

# 4. Email filtering
def is_valid_email(email):
    return isinstance(email, str) and "@" in email and "." in email and len(email) <= 100

df = df[df["Email"].apply(is_valid_email)]
print(f"Total usable rows: {len(df)}")

# 5. Categorical columns
discrete_columns = df.select_dtypes(include=['object']).columns.tolist()
for col in expected_order:
    if col in df.columns and col not in discrete_columns:
        discrete_columns.append(col)

print("Categorical columns:", discrete_columns)

# 6. CTGAN training or model loading
if os.path.exists(model_path):
    print("Loading existing model...")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
else:
    print("Training CTGAN model...")
    model = CTGAN(
        epochs=500,
        batch_size=128,
        pac=2,
        embedding_dim=128,
        verbose=True
    )
    model.fit(df, discrete_columns=discrete_columns)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print("Model saved:", model_path)

# 7. Generate synthetic data
print("Generating synthetic data...")
generated = model.sample(config["sample_count"])

# 8. Filtering
generated = generated[generated["Email"].apply(is_valid_email)]
generated = generated[generated["Phone"].astype(str).str.len() >= 8]

def is_clean(text):
    return isinstance(text, str) and not any(ord(c) < 32 or ord(c) > 126 for c in text)

generated = generated[generated["Password"].apply(is_clean)]
sample = generated.head(config["sample_count"])

# 9. Save output
base_name = "generated_data"
i = 1
while True:
    output_path = os.path.join(output_dir, f"{base_name}_{i}.csv")
    if not os.path.exists(output_path):
        break
    i += 1

sample.to_csv(output_path, index=False)
print("Data saved to file:", output_path)

# 10. Preview
print("Sample preview:")
print(sample.head())
