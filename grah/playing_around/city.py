import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import multiprocessing as mp

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
        """ retrieves a DiGraph with only the walking-connected points (and its edges) """
        padre = nx.DiGraph(((source, target, attr) for source, target, attr
                            in self.city_graph.edges(data=True) if attr['net'] == "father"))
        return padre

    def random_closed_path(self,terminal_node):
        """ retrieves a random closed path from node to itself"""
        path=[]
        path_complete = False

        current_node = terminal_node
        c=0
        while not path_complete:
            next_node = random.choice(list(self.mother.neighbors(current_node)))
            #i comment this as the program should realize a bad path is a way and return and all those things...
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

    def create_two_paths(self):
        """" returns two random paths to be cross-overedt """
        path1 = self.random_closed_path((0,0))
        path2 = self.random_closed_path((0,0))
        return [tuple(path1),tuple(path2)]

    def compute_fitness(self, linePath,i=None, dict=None):
        #https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.shortest_paths.generic.average_shortest_path_length.html
        father_with_linePath = self.father.copy()
        father_with_linePath.add_edges_from(linePath)
        if i==None:
            return nx.average_shortest_path_length(father_with_linePath)
        else:
            dict[str(i)] = nx.average_shortest_path_length(father_with_linePath)
            return dict

    def compute_fitness_family(self, paths):
        if isinstance(paths,dict) != True:
            raise TypeError("paths should be a dict")
        jobs=[]
        manager = mp.Manager()
        return_dict = manager.dict()
        multi=[mp.Process(target=self.compute_fitness, args=([paths[str(k)]],k,return_dict)) for k in paths.keys()]
        for i in multi:
            jobs.append(i)
            i.start()
        for proc in jobs:
            proc.join()
        return return_dict
