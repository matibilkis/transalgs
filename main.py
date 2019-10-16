import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

class CityGraph():
    def __init__(self, ratio=3,length=100, width=100):
        self.city_graph = self.create_lattice(ratio, N=length, M=width)
        self.mother = self.give_mother()
        self.father = self.give_father()

    def add_path_bi(self,g,a,b,subnet="father"):
        """ Take a graph g and creates a bidirectional edge from node a to node b """
        g.add_path([a,b],net=subnet)
        g.add_path([b,a],net=subnet)
        return


    def create_lattice(self,ratio,N,M):
        """ This function returns a city graph
        that has two edge classes: father or mother. Father
        refers to walking points, where mother to points connected with
        transport line."""

        city_graph = nx.DiGraph()
        for i1 in range(M+1):
            for i2 in range(N+1):
                city_graph.add_nodes_from([(i1,i2)])
                if (i1%ratio ==0)& (i2%ratio==0):
                    if i2 !=N:
                        self.add_path_bi(city_graph,(i1,i2),(i1,min(N,i2+ratio)),subnet="mother")
                    if i1 !=0:
                        self.add_path_bi(city_graph,(i1,i2),(max(i1-ratio,0),i2), subnet="mother")
                if i2!=N:
                    self.add_path_bi(city_graph, (i1,i2),(i1,i2+1),subnet="father")
                if i1!=0:
                    self.add_path_bi(city_graph,(i1,i2),(i1-1,i2), subnet="father")
        return city_graph

    def give_mother(self):
        """ retrieves a DiGraph with all possible paths in the transport system """
        madre = nx.DiGraph(((source, target, attr) for source, target, attr
                            in self.city_graph.edges(data=True) if attr['net'] == "mother"))
        return madre

    def give_father(self):
        """ retrieves a DiGraph with all possible paths in the transport system """
        padre = nx.DiGraph(((source, target, attr) for source, target, attr
                            in self.city_graph.edges(data=True) if attr['net'] == "father"))
        return padre

    def create_two_paths(self):
        path1 = self.random_closed_path((0,0))
        path2 = self.random_closed_path((0,0))
        return [path1,path2]

    def random_closed_path(self,terminal_node):
        """ retrieves a random closed path from node to itself"""
        path=[]
        path_complete = False

        current_node = terminal_node
        c=0
        while not path_complete:
            next_node = random.choice(list(self.mother.neighbors(current_node)))
            #i comment this as the program shoul realize a bad path is a way and return and all those things...
            #If later i've problems with convergence, i'll take a look
#            if c==1:
 #               while next_node == terminal_node: #avoid one-length path
  #                  next_node = random.choice(list(self.mother.neighbors(current_node)))
            path.append((current_node,next_node))
            current_node = next_node
            c+=1
            if current_node == terminal_node:
               path_complete = True
        return path

#     def compute_fitness(self, path=None):
#         """ Example: take path = self.random_closed_path((0,0))"""
#         average_path=0
#         c=0
#         f = self.city_graph.copy()
#         if path == None:
#             path = self.random_closed_path((0,0))
#         f.add_edges_from(path)
#         for node1 in list(f.nodes):
#             nodes2=list(f.nodes)
#             nodes2.remove(node1)
#             for node2 in nodes2:
#                 average_path += nx.shortest_path_length(f,node1,node2)
#                 #average_path += nx.shortest_path_length(f,node2,node1) #Notice this is useless if ida y vuelta

#                 c+=1
#         return average_path/c

    def compute_fitness(self, linePath):
        #https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.shortest_paths.generic.average_shortest_path_length.html
        father_with_linePath = self.father.copy()
        father_with_linePath.add_edges_from(linePath)
        return nx.average_shortest_path_length(father_with_linePath)

    def check_paths(self,paths, changePoints):
        if isinstance(changePoints,list) != True:
            changePoints = [changePoints]
        cop = paths.copy()
        for ind,i in enumerate(paths):
            if len(i)<(max(changePoints)+1):
#                 print("Path {} discarded".format(str(ind)))
                cop.remove(i)
        if len(cop)<(len(changePoints)+1): #notice it's +1 as the path may be length changePoints
            #to be serious we should put changePoint strictly higher than shortest path distance... but from which to which ?
            return False, []
        else:
            return True, cop

    def crop_and_paste(self, paths, changePoints=5):
        if self.check_paths(paths,changePoints)[0]==True:
            motherAndPaths = self.mother.copy()
            for p in paths:
                motherAndPaths.add_edges_from(p)
            if isinstance(changePoints,list) != True:
                changePoints = [changePoints]
            path = tuple(paths[0][:changePoints[0]])

            extremePath1= paths[0][changePoints[0]][1]
            extremePath2 = paths[1][changePoints[0]+1][0]

            shortest_connection = tuple(nx.shortest_path(motherAndPaths, extremePath1, extremePath2))
            path_edg = (tuple([path[-1][-1], shortest_connection[0]]),)
            for i in range(len(shortest_connection)-1):
                path_edg += tuple([(tuple([(shortest_connection[i]),(shortest_connection[i+1])]))])

#             print("shortest-connection, ", shortest_connection)
#             print("connection: ", path_edg)
            path += path_edg
            path += tuple(paths[1][(changePoints[0]+1):])
            return True, path
        else:
#             print("Paths do not satisfy sex onditions (maybe they are not hot enough)")
            return False, ()
        #I'll make it for only one changePoint, but it should not be difficult to extend this
