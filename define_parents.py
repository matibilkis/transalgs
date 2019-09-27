import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


plt.figure(figsize=(10,10))
N=M=10
padre=nx.DiGraph()
madre=nx.DiGraph()

def add_path_bi(g,a,b):
    g.add_path([a,b])
    g.add_path([b,a])
    return

d=2
for i1 in range(M+1):
    for i2 in range(N+1):
        if (i1%d ==0)& (i2%d==0):
            madre.add_nodes_from([(i1,i2)])
            if i2 !=M:
                add_path_bi(madre,(i1,i2),(i1,i2+d))
            if i1 !=0:
                add_path_bi(madre,(i1,i2),(i1-d,i2))
                add_path_bi(madre,(i1,i2),(i1-d,i2))

        padre.add_nodes_from([(i1,i2)])

nx.draw_spectral(madre)
plt.show()
