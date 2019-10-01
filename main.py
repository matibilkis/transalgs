import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

class CityGraph():
    def __init__(self, ratio=3,length=100, width=100):
        self.city_graph = self.create_lattice(ratio, N=length, M=width)
        self.mother = self.give_mother()

    def add_path_bi(self,g,a,b,subnet="father"):
        """ Take a graph g and creates a bidirectional edge from node a to node b """
        g.add_path([a,b],net=subnet)
        g.add_path([b,a],net=subnet)
        return


    def create_lattice(self,ratio,N=4,M=4):
        """ This function returns a city graph
        that has two edge classes: father or mother. Father
        refers to walking points, where mother to points connected with
        transport line."""

        city_graph = nx.DiGraph()
        for i1 in range(M+1):
            for i2 in range(N+1):
                city_graph.add_nodes_from([(i1,i2)])
                if (i1%ratio ==0)& (i2%ratio==0):
                    if i2 !=M:
                        self.add_path_bi(city_graph,(i1,i2),(i1,min(M,i2+ratio)),subnet="mother")
                    if i1 !=0:
                        self.add_path_bi(city_graph,(i1,i2),(max(i1-ratio,0),i2), subnet="mother")
                if i2!=M:
                    self.add_path_bi(city_graph, (i1,i2),(i1,i2+1),subnet="father")
                if i1!=0:
                    self.add_path_bi(city_graph,(i1,i2),(i1-1,i2), subnet="father")
        return city_graph

    def give_mother(self):
        """ retrieves a DiGraph with all possible paths in the transport system """
        madre = nx.DiGraph(((source, target, attr) for source, target, attr
                            in self.city_graph.edges(data=True) if attr['net'] == "mother"))
        return madre

    def random_closed_path(self,terminal_node):
        """ retrieves a random closed path from node to itself"""
        path=[]
        path_complete = False

        current_node = terminal_node
        c=0
        while not path_complete:
            next_node = random.choice(list(self.mother.neighbors(current_node)))
            if c==1:
                while next_node == terminal_node: #avoid one-length path
                    next_node = random.choice(list(self.mother.neighbors(current_node)))
            path.append((current_node,next_node))
            current_node = next_node
            c+=1
            if current_node == terminal_node:
               path_complete = True
        return path

    def compute_fitness(self, path=None):
        """ Example: take path = self.random_closed_path((0,0))"""
        average_path=0
        c=0
        f = self.city_graph.copy()
        if path == None:
            path = self.random_closed_path((0,0))
        f.add_edges_from(path)
        for node1 in list(f.nodes):
            nodes2=list(f.nodes)
            nodes2.remove(node1)
            for node2 in nodes2:
                average_path += nx.shortest_path_length(f,node1,node2)
                #average_path += nx.shortest_path_length(f,node2,node1) #Notice this is useless if ida y vuelta

                c+=1
        return average_path/c

    
