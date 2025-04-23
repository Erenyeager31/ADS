# Basic Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# Step 1: Create imbalanced dataset
X, y = make_classification(n_samples=1000, n_features=10, n_informative=3, n_redundant=2,
                           n_classes=2, weights=[0.9, 0.1], random_state=42)

# Step 2: Visualize class imbalance
print("Original class distribution:", Counter(y))
plt.bar(['Class 0', 'Class 1'], [Counter(y)[0], Counter(y)[1]], color=['skyblue', 'salmon'])
plt.title('Class Distribution Before SMOTE')
plt.ylabel('Samples')
plt.show()

# Step 3: Apply PCA to visualize feature space before SMOTE
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.scatter(X_pca[y==0, 0], X_pca[y==0, 1], alpha=0.5, label='Class 0', c='skyblue')
plt.scatter(X_pca[y==1, 0], X_pca[y==1, 1], alpha=0.5, label='Class 1', c='salmon')
plt.title('Feature Space Before SMOTE (PCA)')
plt.legend()
plt.show()

# Step 4: Apply SMOTE
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X, y)
print("After SMOTE:", Counter(y_res))

# Step 5: Visualize feature space after SMOTE
X_res_pca = pca.transform(X_res)
plt.scatter(X_res_pca[y_res==0, 0], X_res_pca[y_res==0, 1], alpha=0.5, label='Class 0', c='skyblue')
plt.scatter(X_res_pca[y_res==1, 0], X_res_pca[y_res==1, 1], alpha=0.5, label='Class 1', c='salmon')
plt.title('Feature Space After SMOTE (PCA)')
plt.legend()
plt.show()

# Step 6: Compare model performance before vs after SMOTE
def train_and_evaluate(X_data, y_data, label):
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.3, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print(f"\n--- {label} ---")
    print(classification_report(y_test, y_pred))
    ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred)).plot()
    plt.title(f'Confusion Matrix: {label}')
    plt.show()

train_and_evaluate(X, y, "Before SMOTE")
train_and_evaluate(X_res, y_res, "After SMOTE")
