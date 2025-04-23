import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.neighbors import NearestNeighbors, LocalOutlierFactor

# Load Iris dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)[['sepal length (cm)', 'sepal width (cm)']]  # Use 2D for plotting

# Distance-Based Outlier Detection (kNN)
knn = NearestNeighbors(n_neighbors=5)
knn.fit(X)
distances, _ = knn.kneighbors(X)
outlier_scores_dist = distances[:, -1]  # Distance to the 5th nearest neighbor
threshold_dist = np.percentile(outlier_scores_dist, 95)
outliers_dist = outlier_scores_dist > threshold_dist

# Plot Distance-Based Outliers
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=~outliers_dist, cmap='coolwarm', edgecolor='k')
plt.title("Distance-Based Outliers")
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')

# Density-Based Outlier Detection (LOF)
lof = LocalOutlierFactor(n_neighbors=20)
outliers_lof = lof.fit_predict(X)
lof_scores = -lof.negative_outlier_factor_
threshold_lof = np.percentile(lof_scores, 95)

# Plot Density-Based Outliers
plt.subplot(1, 2, 2)
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=lof_scores > threshold_lof, cmap='coolwarm', edgecolor='k')
plt.title("Density-Based (LOF) Outliers")
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')

plt.tight_layout()
plt.show()
