import seaborn as sns
import numpy as np

df = sns.load_dataset("titanic")

df = df.mask(np.random.rand(*df.shape) < 0.05)

df.to_excel("titanic.xlsx",index=False)