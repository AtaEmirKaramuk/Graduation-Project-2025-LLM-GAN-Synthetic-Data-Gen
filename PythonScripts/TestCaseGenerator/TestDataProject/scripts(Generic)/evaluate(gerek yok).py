import os
import glob
import pandas as pd
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

# File paths
real_path = os.path.join("..", "data", "base_dataset_2000.csv")
output_dir = os.path.join("..", "outputs")

# Find the most recently generated synthetic data file
csv_files = glob.glob(os.path.join(output_dir, "generated_data_*.csv"))
if not csv_files:
    raise FileNotFoundError("No 'generated_data_*.csv' files found in outputs/ directory.")

synthetic_path = max(csv_files, key=os.path.getctime)
print(f"Using synthetic data file: {synthetic_path}\n")

# Load the datasets
real_data = pd.read_csv(real_path)
synthetic_data = pd.read_csv(synthetic_path)

print("Datasets loaded successfully.\n")
print(f"Real data row count: {len(real_data)}")
print(f"Synthetic data row count: {len(synthetic_data)}\n")

# Summary statistics
print("Real data summary statistics:")
print(real_data.describe(include='all'))

print("\nSynthetic data summary statistics:")
print(synthetic_data.describe(include='all'))

# Column-by-column comparison
print("\nColumn-wise detailed comparison:\n")
comparison_results = []

for column in real_data.columns:
    real_col = real_data[column].dropna()
    synthetic_col = synthetic_data[column].dropna()

    col_type = "Numeric" if pd.api.types.is_numeric_dtype(real_col) else "Categorical"

    real_unique = real_col.nunique()
    synthetic_unique = synthetic_col.nunique()

    # Calculate KL divergence only for categorical columns
    if col_type == "Categorical":
        real_counts = real_col.value_counts(normalize=True)
        synthetic_counts = synthetic_col.value_counts(normalize=True)
        all_vals = set(real_counts.index).union(set(synthetic_counts.index))
        real_probs = [real_counts.get(val, 1e-12) for val in all_vals]
        synthetic_probs = [synthetic_counts.get(val, 1e-12) for val in all_vals]
        kl_div = entropy(real_probs, synthetic_probs)
    else:
        kl_div = np.nan

    similarity_score = min(real_unique, synthetic_unique) / max(real_unique, synthetic_unique) if max(real_unique, synthetic_unique) > 0 else 0.0

    print(f"- Column: {column}")
    print(f"  Type: {col_type}")
    print(f"  Real Unique: {real_unique}, Synthetic Unique: {synthetic_unique}")
    print(f"  Similarity Score: {similarity_score:.2%}")
    if not np.isnan(kl_div):
        print(f"  Entropy (KL Divergence): {kl_div:.4f}")
    print("")

    comparison_results.append({
        "Column": column,
        "Type": col_type,
        "Real Unique": real_unique,
        "Synthetic Unique": synthetic_unique,
        "Similarity Score": round(similarity_score, 4),
        "KL Divergence": None if np.isnan(kl_div) else round(kl_div, 4)
    })

# Overall score
df_results = pd.DataFrame(comparison_results)
overall_score = df_results["Similarity Score"].mean()
print(f"Overall Similarity Score: {overall_score:.2%}")

# Save CSV output
summary_path = os.path.join(output_dir, "evaluation_summary.csv")
df_results.to_csv(summary_path, index=False)
print(f"Comparison summary saved to: {summary_path}")

# Visualization (bar chart)
try:
    df_results.set_index("Column")[["Similarity Score"]].plot.bar(
        title="Column-wise Similarity Scores", legend=False, figsize=(10, 5)
    )
    plt.ylabel("Score (0-1)")
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"Visualization failed: {e}")
