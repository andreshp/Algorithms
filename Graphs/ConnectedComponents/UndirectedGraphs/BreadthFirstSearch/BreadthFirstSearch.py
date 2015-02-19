#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Breadth-First Search for finding the Connected Components of Graph
#######################################################################

# This program read a graph as an adjacency list from a file. 
# Afterwards it executes de BFS algorithm on it to find the number of
# connected components of the graph. The user can choose between printing 
# them or not. 

import sys   # For arguments (syc.argv) and exit (syc.exit())
import time  # To time the program
import queue # Python queue module 
from random import randrange # Random integer generator


# A Graph class. A graph is represented by its adjacency list.
class Graph(object):

    # The class is conformed by these members:
    #  - adj_list : Adjacency list to represent the graph. It is implemented as a dictionary of dictionaries.
    #               The first dictionary's keys are the nodes of the graph. Its values are dictionaries with
    #               the key's neighbours and the number of edges between them.
    #  - outdegree : Dictionary which maps for each node its outdegree (The number of edges leaving from this node).
    #  - num_edges : Number of edges in the graph.
    #  - type_node : Type of the graph nodes. It is int by default.
    #  
    #  The graph admits multiples edges from one node to another thanks to the dictionary of dictionaries implementation.

    # Initializes a graph object
    def __init__(self, adj_list = {}, outdegree = {}, num_edges = 0, type_node = int):
        self.adj_list = adj_list
        self.outdegree = outdegree
        self.num_edges = num_edges
        self.type_node = type_node

    # Read a graph from a file in adjacency list form
    def readGraph(self, file):
        data = open(file, "r")

        for line in data:
            # Get the nodes and initialize the current node adj_list
            nodes = [self.type_node(element) for element in line.split()]
            self.adj_list[nodes[0]] = {}
            
            # Add the neighbours to node[0] adj_list
            for i in range(1, len(nodes)):
                self.adj_list[nodes[0]][nodes[i]] = self.adj_list[nodes[0]][nodes[i]]+1 if nodes[i] in self.adj_list[nodes[0]] else 1
            
            # Increment num_edges and add degree(nodes[0]) to outdegree:
            self.num_edges += len(nodes)-1; self.outdegree[nodes[0]] = len(nodes)-1
        
        data.close()

    # Find every connected component in the graph and returns them.
    # Efficiency:  O(|V| + |E|)
    def connectedComponents(self):
        connected_components = []
        if len(self.adj_list) > 0:
            visited = set()
            for node in self.adj_list:
                if node not in visited:
                    visited.add(node)
                    connected_components.append(self.breadthFirstSearch(node, visited))
                elif len(visited) == len(self.adj_list):
                    break
        return connected_components

    # Find the connected component which contains a.
    # Efficiency: O(|Va| + |Ea|)
    def breadthFirstSearch(self, a, visited):

        q = queue.Queue() # queue with the nodes to read
        q.put(a); connected_component = []

        # Visit every possible node
        while(not q.empty()):
            node = q.get(); connected_component.append(node)
            for neighbour in self.adj_list[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    q.put(neighbour)

        return connected_component


######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Sintax: BreadthFirstSearch.py <options> graph.txt \n The option -n don't print the connected components.")
    sys.exit()

print_components = True

if len(sys.argv) > 2:
    if sys.argv[1] == "-n":
        print_components = False

# Create Graph

try:
    graph_file = sys.argv[1 if len(sys.argv) ==  2 else 2]
    graph = Graph()
    graph.readGraph(graph_file)
except IOError:
   print("Error: The file",  graph_file,  "can\'t be read.")
   sys.exit()

# Execute Breadth-First Search for connected components and count the time wasted
start_time = time.time()
components = graph.connectedComponents()
print("--- %f seconds ---" % (time.time() - start_time))

print("Number of connected components: ", len(components))
if print_components:
    if len(components) == 0:
        print("There are no connected components.")
    else:
        for i in range(0,len(components)):
            print("Connected Component ", i+1, ": ", components[i])
        