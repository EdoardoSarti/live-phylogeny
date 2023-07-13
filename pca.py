# PCS Tests to study the data

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from usage import *
plt.style.use('ggplot')


df = pd.DataFrame(dist_mat, columns =  names)
print(df)
# names is inherited
X = df.values
print(X.shape)
scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

pca_30 = PCA(n_components=8, random_state=2020)
pca_30.fit(X_scaled)
X_pca_30 = pca_30.transform(X_scaled)

plt.plot(np.cumsum(pca_30.explained_variance_ratio_))
plt.xlabel('Number of components')
plt.ylabel('Explained variance')
plt.savefig('n_vs_var.png', dpi=100)

pca_2 = PCA(n_components=2, random_state=2020)
pca_2.fit(X_scaled)
X_pca_2 = pca_2.transform(X_scaled)







plt.figure(figsize=(10, 7))
sns.scatterplot(x=X_pca_2[:, 0], y=X_pca_2[:, 1], s=70)
plt.title("2D Scatterplot: 63.24 of the variability captured", pad=15)
plt.xlabel("First principal component")
plt.ylabel ("Second principal component")
plt.savefig("2d_scatterplot.png")