import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.neighbors import NearestNeighbors, LocalOutlierFactor

# Load Iris dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)[['sepal length (cm)', 'sepal width (cm)']]

# Distance-Based Outlier Detection (kNN)
knn = NearestNeighbors(n_neighbors=5)
knn.fit(X)
distances, _ = knn.kneighbors(X)
outlier_scores_dist = distances[:, -1]
threshold_dist = np.percentile(outlier_scores_dist, 95)
outliers_dist = outlier_scores_dist > threshold_dist

# Density-Based Outlier Detection (LOF)
lof = LocalOutlierFactor(n_neighbors=20)
outliers_lof = lof.fit_predict(X)
lof_scores = -lof.negative_outlier_factor_
threshold_lof = np.percentile(lof_scores, 95)

# Plotting section
plt.figure(figsize=(12, 10))

# 1. Distance-Based Scatter Plot
plt.subplot(2, 2, 1)
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=~outliers_dist, cmap='coolwarm', edgecolor='k')
plt.title("Distance-Based Outliers")
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')

# 2. Density-Based Scatter Plot
plt.subplot(2, 2, 2)
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=lof_scores > threshold_lof, cmap='coolwarm', edgecolor='k')
plt.title("Density-Based (LOF) Outliers")
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')

# 3. Histogram of kNN distances
plt.subplot(2, 2, 3)
plt.hist(outlier_scores_dist, bins=30, color='steelblue', edgecolor='black')
plt.axvline(threshold_dist, color='red', linestyle='--', label='95th percentile')
plt.title("Histogram: kNN Distances")
plt.xlabel("5th Nearest Neighbor Distance")
plt.ylabel("Frequency")
plt.legend()

# 4. Histogram of LOF scores
plt.subplot(2, 2, 4)
plt.hist(lof_scores, bins=30, color='salmon', edgecolor='black')
plt.axvline(threshold_lof, color='black', linestyle='--', label='95th percentile')
plt.title("Histogram: LOF Scores")
plt.xlabel("LOF Score")
plt.ylabel("Frequency")
plt.legend()

plt.tight_layout()
plt.show()

# Optional: Seaborn JointPlot (Scatter + Marginal Histograms)
sns.jointplot(data=X, x='sepal length (cm)', y='sepal width (cm)',
              hue=lof_scores > threshold_lof, palette='coolwarm', kind='scatter')
plt.suptitle("LOF Outlier View (Joint Plot)", y=1.02)
plt.show()
