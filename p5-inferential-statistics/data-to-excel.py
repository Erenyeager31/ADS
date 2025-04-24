from sklearn.datasets import load_iris
import pandas as pd

data = load_iris()
df = pd.DataFrame(data.data,columns=data.feature_names)
df['Species'] = data.target

df.to_csv("iris.csv",index=False)