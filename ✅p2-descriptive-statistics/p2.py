import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset into a pandas DataFrame
df = sns.load_dataset("tips")

# --- Numerical Descriptive Statistics ---
# Select only numerical columns
numeric_df = df.select_dtypes(include=[np.number])

# Now run the descriptive statistics
print("Mean:\n", numeric_df.mean())            # Central average of each feature
print("\nMedian:\n", numeric_df.median())      # Middle value, robust to outliers
print("\nStandard Deviation:\n", numeric_df.std())  # Spread around mean
print("\nVariance:\n", numeric_df.var())       # Square of std dev, shows dispersion
print("\nMinimum:\n", numeric_df.min())        # Smallest value in each numeric column
print("\nMaximum:\n", numeric_df.max())        # Largest value in each numeric column
print("\nSkewness:\n", numeric_df.skew())      # Asymmetry of distribution
print("\nKurtosis:\n", numeric_df.kurtosis())  # Peakedness / tailedness
print("\nCorrelation Matrix:\n", numeric_df.corr())  # Linear relationships between numerical features
print("\nNon-null Count:\n", numeric_df.count())     # Checks data completeness (total non-null entries)

# --- Visual Descriptive Statistics ---

# 1. Histogram - shows frequency distribution for each numeric feature
df.hist(bins=15, figsize=(12, 10))
plt.suptitle('Histograms of Features')
plt.tight_layout()
plt.show()

# 2. Boxplot - highlights median, IQR, and outliers for numerical features only
plt.figure(figsize=(12, 6))
sns.boxplot(data=df.select_dtypes(include=[np.number]))  # Select numeric columns only
plt.title('Boxplot of Numeric Features')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Heatmap - visualizes correlation between numeric features
plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()

# 4. Pairplot - scatter plots between feature pairs, shows relationships between numerical features
sns.pairplot(df.select_dtypes(include=[np.number]))  # Select numeric columns only
plt.suptitle('Pairplot of Numeric Features', y=1.02)
plt.show()
