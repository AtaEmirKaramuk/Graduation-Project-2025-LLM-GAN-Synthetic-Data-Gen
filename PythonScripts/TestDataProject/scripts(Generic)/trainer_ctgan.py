import os
import pickle
import pandas as pd
from ctgan import CTGAN

pd.set_option("display.max_columns", None)

# 1. File paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_path = os.path.join(base_dir, "data", "base_dataset_2000.csv")
model_path = os.path.join(base_dir, "models", "ctgan_model.pkl")
os.makedirs(os.path.dirname(model_path), exist_ok=True)

# 2. Load data
df = pd.read_csv(data_path)
df.dropna(inplace=True)

# 3. Filter valid emails and phone numbers
def is_valid_email(email):
    return isinstance(email, str) and "@" in email and "." in email and len(email) <= 100

def is_clean(text):
    return isinstance(text, str) and not any(ord(c) < 32 or ord(c) > 126 for c in text)

df = df[df["Email"].apply(is_valid_email)]
df = df[df["Phone"].astype(str).str.len() >= 8]
df = df[df["Password"].apply(is_clean)]

print(f"Filtered data: {df.shape[0]} rows")

# 4. Identify categorical columns
discrete_columns = df.select_dtypes(include="object").columns.tolist()
print("Categorical columns:", discrete_columns)

# 5. Train CTGAN model
print("Training CTGAN model...")
model = CTGAN(
    epochs=500,
    batch_size=128,
    pac=2,
    embedding_dim=128,
    verbose=True
)
model.fit(df, discrete_columns=discrete_columns)

# 6. Save model
with open(model_path, "wb") as f:
    pickle.dump(model, f)
print("CTGAN model saved:", model_path)
