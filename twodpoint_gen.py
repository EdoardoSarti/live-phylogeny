# Used for multidimentional scaling of the dist_mat 
from usage import dist_mat, datanodes, nodes
from sklearn.manifold import MDS
import matplotlib.pyplot as plt


mds = MDS(n_components=2, dissimilarity='precomputed')
coordinates = mds.fit_transform(dist_mat)


colors = ['red' if i in datanodes else 'blue' for i in range(coordinates.shape[0])]
plt.scatter(coordinates[:, 0], coordinates[:, 1], c=colors)
plt.show()
