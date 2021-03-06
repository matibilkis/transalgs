import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def add_path_bi(g,a,b):
    """ Take a graph g and creates a bidirectional edge from node a to node b """

    g.add_path([a,b])
    g.add_path([b,a])
    return

def create_grid_parents(ratio,N=4,M=4):
    """ This function returns mother and father graphs, mother is kind of a subgraph of father """
    padre=nx.DiGraph()
    madre=nx.DiGraph()
    for i1 in range(M+1):
        for i2 in range(N+1):
            if (i1%ratio ==0)& (i2%ratio==0):
                madre.add_nodes_from([(i1,i2)])
                if i2 !=M:
                    add_path_bi(madre,(i1,i2),(i1,i2+ratio))
                if i1 !=0:
                    add_path_bi(madre,(i1,i2),(i1-ratio,i2))
            padre.add_nodes_from([(i1,i2)])
            if i2!=M:
                add_path_bi(padre, (i1,i2),(i1,i2+1))
            if i1!=0:
                add_path_bi(padre,(i1,i2),(i1-1,i2))
    return padre, madre

padre, madre = create_grid_parents(2,6,6)
print(madre.nodes)
