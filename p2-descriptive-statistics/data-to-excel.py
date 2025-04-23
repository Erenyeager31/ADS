from sklearn.datasets import load_diabetes
import pandas as pd
import seaborn as sns

# Load and convert to DataFrame
df = sns.load_dataset("tips")

# Save to Excel
df.to_excel("diabetes_data.xlsx", index=False)
