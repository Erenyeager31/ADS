import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load dataset
tips = sns.load_dataset("tips")
sns.set_theme(style="whitegrid")

# ========== UNIVARIATE ==========

# 1. Histogram
sns.histplot(tips["total_bill"], kde=True)
plt.title("Total Bill Distribution")
plt.show()
# Interpretation: Most bills are between $10 and $20, with a right-skewed distribution.

# 2. Count Plot
sns.countplot(x="day", data=tips)
plt.title("Count of Days")
plt.show()
# Interpretation: Saturday and Sunday have the highest number of entries, indicating busier weekends.

# 3. Box Plot
sns.boxplot(y="tip", data=tips)
plt.title("Tip Amount Distribution")
plt.show()
# Interpretation: Most tips are between $2 and $4, with a few high-value outliers.

# ========== BIVARIATE ==========

# 4. Scatter Plot
sns.scatterplot(x="total_bill", y="tip", data=tips)
plt.title("Total Bill vs Tip")
plt.show()
# Interpretation: Tips generally increase with the total bill, but not in a perfectly linear fashion.

# 5. Bar Plot
sns.barplot(x="sex", y="tip", data=tips)
plt.title("Average Tip by Gender")
plt.show()
# Interpretation: Males tend to give slightly higher average tips than females.

# 6. Box Plot with Grouping
sns.boxplot(x="smoker", y="total_bill", data=tips)
plt.title("Total Bill by Smoking Status")
plt.show()
# Interpretation: Smokers and non-smokers have similar billing patterns, but with some variation in outliers.

stack_data = pd.crosstab(tips["sex"], tips["smoker"])

# Plot stacked bar chart
stack_data.plot(kind='bar', stacked=True, colormap='Set2')
plt.title("Smokers by Gender (Stacked Bar)")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.legend(title="Smoker")
plt.show()

# ========== TRIVARIATE ==========

# 7. Scatter with Hue
sns.scatterplot(x="total_bill", y="tip", hue="sex", data=tips)
plt.title("Total Bill vs Tip by Gender")
plt.show()
# Interpretation: Tip trends are similar for both genders, though male tips slightly more at higher bills.

# 8. Grouped Boxplot
sns.boxplot(x="day", y="total_bill", hue="sex", data=tips)
plt.title("Bill by Day and Gender")
plt.show()
# Interpretation: Males spend slightly more on weekends; both genders show similar patterns across days.

# 9. Pairplot
sns.pairplot(tips, hue="smoker")
plt.suptitle("Pairwise Plots by Smoking Status", y=1.02)
plt.show()
# Interpretation: Relationships between features like tip and bill are consistent regardless of smoking status.

# ========== BONUS PLOT ==========

# 10. Heatmap (Encoded Correlation)
tips_encoded = pd.get_dummies(tips, drop_first=True)
corr = tips_encoded.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap with Encoded Features")
plt.show()
# Interpretation: 'total_bill' and 'tip' are strongly correlated. Other features show mild associations.
