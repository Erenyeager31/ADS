# GPT convo --> [convo](https://chatgpt.com/share/6808d767-190c-800c-a6e3-06d368ddb588)

# Python code --> [python](./p3.py)
## ✅ **Overview of Data Cleaning Steps**

1. **Load Dataset**: Loads Titanic dataset from Seaborn.
2. **Drop Irrelevant Columns**: Drops `deck` and `parch` due to too many missing values or redundancy.
3. **Inject Random Missing Values**: Simulates a dirty dataset by adding 5% random NaNs.
4. **Visualize Missing Data**: Plots heatmaps before and after cleaning.
5. **Outlier Removal**: Removes outliers in numeric columns using the IQR method.
6. **Missing Value Imputation**:
   - **Numerical**: Imputes using mean or median based on skewness.
   - **Categorical**: Imputes using the most frequent value.
7. **Text Cleaning**: Standardizes text (lowercase, stripped whitespace).
8. **Encoding**: Converts categorical columns to numerical using label encoding.
9. **Normalization**: Scales numerical columns to [0, 1] using Min-Max scaling.
10. **Target Preparation**: Ensures the `survived` column (target) is integer type.
11. **Export**: Saves both the dirty and cleaned datasets to Excel and CSV respectively.

# Excel --> [Excel](./titanic.xlsx)
stopped midway - too much of hassle