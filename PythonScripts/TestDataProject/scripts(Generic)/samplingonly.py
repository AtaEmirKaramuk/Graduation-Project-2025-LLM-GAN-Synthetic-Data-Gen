import os
import pickle
import pandas as pd

def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("Model loaded:", model_path)
    return model

def generate_samples(model, sample_count=1000):
    print(f"Generating synthetic data: {sample_count} rows")
    samples = model.sample(sample_count)
    return samples

def filter_samples(df):
    # Example filtering: valid emails and phone numbers with at least 8 characters
    def is_valid_email(email):
        return isinstance(email, str) and "@" in email and "." in email and len(email) <= 100

    def is_clean(text):
        return isinstance(text, str) and not any(ord(c) < 32 or ord(c) > 126 for c in text)

    df = df[df["Email"].apply(is_valid_email)]
    df = df[df["Phone"].astype(str).str.len() >= 8]
    df = df[df["Password"].apply(is_clean)]
    return df

def save_samples(df, output_dir, base_name="generated_data"):
    os.makedirs(output_dir, exist_ok=True)
    i = 1
    while True:
        path = os.path.join(output_dir, f"{base_name}_{i}.csv")
        if not os.path.exists(path):
            break
        i += 1
    df.to_csv(path, index=False)
    print("Synthetic data saved:", path)
    return path

if __name__ == "__main__":
    model_path = os.path.join("..", "models", "ctgan_model.pkl")
    output_dir = os.path.join("..", "outputs")

    model = load_model(model_path)
    samples = generate_samples(model, sample_count=1000)
    filtered_samples = filter_samples(samples)
    saved_path = save_samples(filtered_samples, output_dir)
