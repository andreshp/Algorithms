#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Kager's Contraction Algorithm for the Minimum Cut Problem in Graphs  
#######################################################################

# This program read a graph as an adjacency list from a file a execute the 
# Contraction Algorithm for the Minimum Cut Problem. Afterwards, the number
# of crossing edges in the min cut is printed. The user can choose between
# printing or not the sets of vertices A and B of the minimum cut (A,B). 

import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program
import math # log
import copy # To copy the graph
from random import randrange # Random integer generator


# A Graph class. A graph is represented by its adjacency list.
# The graph is assumed to be undirected.
class Graph(object):

    # The class is conformed by these members:
    #  - adj_list : Adjacency list to represent the graph. It is implemented as a dictionary of dictionaries.
    #               The first dictionary's keys are the vertices of the graph. Its values are dictionaries with
    #               the key's neighbours and the number of edges between them.
    #  - vertices_degree : Dictionary which maps for each vertex its degree.
    #  - num_edges : Number of edges in the graph.
    #  - type_vertices : Type of the graph vertices. It is int by default.
    #  
    #  The graph admits multiples edges from one vertex to another thanks to the dictionary of dictionaries implementation.

    # Initializes a graph object
    def __init__(self, adj_list = {}, vertices_degree = {}, num_edges = 0, type_vertices = int):
        self.adj_list = adj_list
        self.vertices_degree = vertices_degree
        self.num_edges = num_edges
        self.type_vertices = type_vertices

    # Read a graph from a file in adjacency list form
    def readGraph(self, file):
        data = open(file, "r")

        for line in data:
            # Get the nodes and initialize the current node adj_list
            nodes = [self.type_vertices(element) for element in line.split()]
            self.adj_list[nodes[0]] = {}
            
            # Add the neighbours to node[0] adj_list
            for i in range(1, len(nodes)):
                self.adj_list[nodes[0]][nodes[i]] = self.adj_list[nodes[0]][nodes[i]]+1 if nodes[i] in self.adj_list[nodes[0]] else 1
            
            # Increment num_edges and add degree(nodes[0]) to vertices_degree:
            self.num_edges += len(nodes)-1; self.vertices_degree[nodes[0]] = len(nodes)-1
        
        # Each edge is counted twice (one for both directions)
        self.num_edges /= 2
        data.close()

    # Contraction Algorithm iteration for the Minimum Cut problem.
    # It find the minimum cut wit probability greater than 2 / ( |V| * (|V|-1) ).
    def contractionAlgorithm(self):
        # Copy the graph (it is going to change)
        graph_copy = copy.deepcopy(self.adj_list); num_edges = self.num_edges; vertices_degree = copy.copy(self.vertices_degree)
        # Current cuts. At the end there will be 2 cuts (unless there are more than 2 connected components)
        cuts = { vertex: {vertex} for vertex in vertices_degree.keys() }

        # Do a contraction |V|-2 times (or until there are no more edges)
        for i in range(0, len(self.adj_list)-2):

            if num_edges >= 1:

                # Select a random edge in O(|E|)
                random_edge = randrange(1, 2*num_edges+1); count = 0
    
                for element in vertices_degree:
                    count += vertices_degree[element]
                    if random_edge <= count:
                        vertex = element; count -= vertices_degree[element]; break
    
                for element in graph_copy[vertex]:
                    count += graph_copy[vertex][element]
                    if count >= random_edge:
                        edge = (vertex, element); break
    
                # Update num_edges and degrees taking into account that edges 
                # from edge[0] to edge[1] are going to be deleted
                num_edges -= graph_copy[edge[0]][edge[1]]
                vertices_degree[edge[0]] = vertices_degree[edge[0]] + vertices_degree[edge[1]] - 2*graph_copy[edge[0]][edge[1]]
    
                # Add edge[1] neighbours to edge[0] neighbours.
                # Delete edge[1] from every neighbout's adjacency list and add edge[0] instead.
                # Efficiency: O(|V|)
                for element, value in graph_copy[edge[1]].items():
                    graph_copy[edge[0]][element] = graph_copy[edge[0]][element] + value if element in graph_copy[edge[0]] else value
                    graph_copy[element][edge[0]] = graph_copy[edge[0]][element]
                    del graph_copy[element][edge[1]]
    
                # Delete edges from edge[0] to edge[0]. Delete edge[1] from the graph
                del graph_copy[edge[0]][edge[0]]; del vertices_degree[edge[1]]; del graph_copy[edge[1]]
                # Union the cuts formed by edge[0] and edge[1]
                cuts[edge[0]] = cuts[edge[0]].union(cuts[edge[1]]); del cuts[edge[1]]

            else: # There are no more edges, the solution is 0.
                return 0, [tuple(cut_set) for cut_set in cuts.values()]

        return min(vertices_degree.values()), [tuple(cut_set) for cut_set in cuts.values()]

    # Repeats the constaction algorithm a given number of times.
    # Consecuently, the probability of finding the minimum cut is greater than 1 - (1- 2 / ( |V| * (|V|-1) ) ) ^ times.
    # By default the number of repetitions is |V|^2 log |V| what gives a probability greater than 1 - 1 / |V|.
    def contractionAlgorithmRepetitions(self, num_repetitions = -1):
        
        # if num_repetitions == -1 then num_repetitions = |V|^2 log |V|
        if num_repetitions <= 0:
            num_repetitions = int(math.log(len(self.vertices_degree)))*(len(self.vertices_degree))**2 
        
        # First call to the contraction algorithm
        (min_num_crossing_edges, minimum_cut) = self.contractionAlgorithm()
        
        # Rest of repetitions
        for i in range(1, num_repetitions):
            (num_crossing_edges, cut) = self.contractionAlgorithm()
            if num_crossing_edges < min_num_crossing_edges:
                min_num_crossing_edges = num_crossing_edges; minimum_cut = cut
        
        return min_num_crossing_edges, minimum_cut

    # Returns the edges of the graph 
    def edges(self):
        edges = set()
        for vertex in range(1, len(self.adj_list)):
            for neighbour in self.adj_list[vertex]:
                if (neighbour, vertex) not in edges:
                    for i in range(self.adj_list[vertex][neighbour]):
                        edges.add((vertex, neighbour))
        return edges


######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) == 1 or len(sys.argv) > 5:
    print("Sintax: ContractionAlgorithm.py <options> graph.txt \n The option -n don't print the sets conforming the cut. \n The option -r <number> choose the number of repetitions")
    sys.exit()

print_cut = True
num_repetitions = -1

if len(sys.argv) > 2:
    if sys.argv[1] == "-n" or sys.argv[2] == "-n":
        print_cut = False
    
    if sys.argv[1] == "-r":
        num_repetitions = int(sys.argv[2]) if print_cut == True else int(sys.argv[3]) 
    elif sys.argv[2] == "-r":
        num_repetitions = int(sys.argv[3])

# Create Graph
graph_file = sys.argv[len(sys.argv)-1]
graph = Graph()
graph.readGraph(graph_file)

# Execute Contraction Algorithm for Minimum Cut and count the time wasted
start_time = time.time()
num, cut = graph.contractionAlgorithmRepetitions(num_repetitions)
print("--- %f seconds ---" % (time.time() - start_time))

print("Number of crossing edges in the minimum cut: ", num)
if print_cut:
    print("Minimum cut:")
    print("Set A: ", cut[0])
    print("Set B: ", cut[1])
