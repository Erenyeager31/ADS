import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from scipy.stats import zscore, ttest_ind, f_oneway, chi2_contingency, norm

sns.set(style="whitegrid")
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# ----------------- Z-Test -----------------
print("\n--- Z-Test on Sepal Length vs Population Mean = 5.8 ---")
sample = df['sepal length (cm)']
pop_mean = 5.8
z_val = (sample.mean() - pop_mean) / (sample.std(ddof=0) / np.sqrt(len(sample)))
p_val = 2 * (1 - norm.cdf(abs(z_val)))
print(f"Z = {z_val:.2f}, p = {p_val:.4f}")

if p_val < 0.05:
    print("🔬 Conclusion (Technical): Reject H0 – Sample mean is significantly different from population mean.")
    print("🧠 Interpretation (Layman): The average sepal length in this dataset is different from the expected value of 5.8 cm.")
else:
    print("🔬 Conclusion (Technical): Fail to reject H0 – No significant difference.")
    print("🧠 Interpretation (Layman): The sepal length in the dataset is close enough to 5.8 cm; it's likely just natural variation.")

# Plot
plt.figure(figsize=(6, 4))
sns.histplot(sample, kde=True, color='skyblue')
plt.axvline(pop_mean, color='red', linestyle='--', label='Population Mean = 5.8')
plt.axvline(sample.mean(), color='green', linestyle='--', label=f'Sample Mean = {sample.mean():.2f}')
plt.title("Z-Test: Sepal Length vs Population Mean")
plt.legend()
plt.show()

# ----------------- T-Test -----------------
print("\n--- T-Test: Petal Length of Class 0 vs Class 1 ---")
group1 = df[df['target'] == 0]['petal length (cm)']
group2 = df[df['target'] == 1]['petal length (cm)']
t_stat, p_val = ttest_ind(group1, group2)
print(f"T = {t_stat:.2f}, p = {p_val:.4f}")

if p_val < 0.05:
    print("🔬 Conclusion (Technical): Reject H0 – Significant difference in means.")
    print("🧠 Interpretation (Layman): Class 0 and Class 1 have clearly different petal lengths.")
else:
    print("🔬 Conclusion (Technical): Fail to reject H0 – No significant difference.")
    print("🧠 Interpretation (Layman): Both classes have similar petal lengths.")

# Plot
plt.figure(figsize=(6, 4))
sns.boxplot(data=[group1, group2], palette='Set2')
plt.xticks([0, 1], ['Class 0', 'Class 1'])
plt.title("T-Test: Petal Length (Class 0 vs 1)")
plt.ylabel("Petal Length (cm)")
plt.show()

# ----------------- F-Test (ANOVA) -----------------
print("\n--- ANOVA (F-Test): Petal Width Across 3 Classes ---")
groups = [df[df['target'] == i]['petal width (cm)'] for i in range(3)]
f_stat, p_val = f_oneway(*groups)
print(f"F = {f_stat:.2f}, p = {p_val:.4f}")

if p_val < 0.05:
    print("🔬 Conclusion (Technical): Reject H0 – At least one group differs significantly.")
    print("🧠 Interpretation (Layman): Not all classes have the same petal width – there are clear differences among them.")
else:
    print("🔬 Conclusion (Technical): Fail to reject H0 – No significant difference.")
    print("🧠 Interpretation (Layman): Petal widths across the classes are fairly similar.")

# Plot
plt.figure(figsize=(6, 4))
sns.boxplot(x='target', y='petal width (cm)', data=df, palette='Set3')
plt.title("ANOVA: Petal Width Across 3 Classes")
plt.xlabel("Class")
plt.ylabel("Petal Width (cm)")
plt.show()

# ----------------- Chi-Square Test -----------------
print("\n--- Chi-Square Test: Petal Length Category vs Target Class ---")
df['petal_len_cat'] = pd.cut(df['petal length (cm)'], bins=3, labels=["Short", "Medium", "Long"])
contingency = pd.crosstab(df['petal_len_cat'], df['target'])
chi2, p, dof, expected = chi2_contingency(contingency)
print(f"Chi2 = {chi2:.2f}, p = {p:.4f}, dof = {dof}")

if p < 0.05:
    print("🔬 Conclusion (Technical): Reject H0 – Variables are dependent.")
    print("🧠 Interpretation (Layman): Petal length category and flower class are related – some petal lengths are more common in specific classes.")
else:
    print("🔬 Conclusion (Technical): Fail to reject H0 – Variables are independent.")
    print("🧠 Interpretation (Layman): Petal length category doesn't vary much across classes.")

# Plot
contingency.plot(kind='bar', stacked=True, colormap='viridis')
plt.title("Chi-Square Test: Petal Length Category vs Class")
plt.xlabel("Petal Length Category")
plt.ylabel("Count")
plt.legend(title="Class")
plt.tight_layout()
plt.show()
