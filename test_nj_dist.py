# To check d_{NJ}(i,j) >= d_{actual}(i,j)
from usage import *

dist_matrix, dates, networkx_graph
ans = 0
denom = 0
for i in range (len(dates)) : 
    for j in range (len(dates)) : 
        if (i!=j) :
            d_real = dist_matrix[i][j]
            d_nj = nx.shortest_path_length(networkx_graph, dates[i], dates[j], weight='distance')
            print(d_real, d_nj)
            if d_real <= d_nj : ans +=1
            denom += 1

print(ans)
print(denom)
