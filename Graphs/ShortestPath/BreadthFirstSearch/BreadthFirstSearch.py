#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Breadth-First Search for Shortest Path Problem in Graph Theory
#######################################################################

# This program read a graph as an adjacency list from a file and two graph's 
# nodes. Afterwards it executes de BFS algorithm on it and returns the 
# length of the shortest path. The user can choose between printing the path or not. 

import sys   # For arguments (syc.argv) and exit (syc.exit())
import time  # To time the program
import math  # log
import copy  # To copy the graph
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

    # 
    def breadthFirstSearch(self, a, b):
        # See if parameters are correct:
        if a not in self.adj_list:
            raise RuntimeError(a)
        if b not in self.adj_list:
            raise RuntimeError(b)
        
        if a == b: return 0, [a] # If a==b then that's the asked path

        # Algorithm
        visited = {a : (0,a)} # Dictionary with the visited nodes and their distance to a
        q = queue.Queue() # queue with the nodes to read
        q.put(a)
        found = False
        # Visit nodes 
        while(not q.empty() and not found):
            node = q.get()
            for neighbour in self.adj_list[node]:
                if not neighbour in visited:
                    visited[neighbour] = (visited[node][0]+1, node)
                    q.put(neighbour)
                    if (neighbour == b):
                        found = True; break

        if found:
            sol = [b]; x = visited[b][1]
            while(x != a):
                sol.append(x); x = visited[x][1]
            sol.append(a)
            return visited[b][0], sol[::-1]
        else:
            return -1, []

    # Returns the edges of the graph 
    def edges(self):
        edges = set()
        for node in range(1, len(self.adj_list)):
            for neighbour in self.adj_list[node]:
                if (neighbour, node) not in edges:
                    for i in range(self.adj_list[node][neighbour]):
                        edges.add((node, neighbour))
        return edges


######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 4 or len(sys.argv) > 5:
    print("Sintax: BreadthFirstSearch.py <options> graph.txt NodeA NodeB \n The option -n don't print the path between A and B.")
    sys.exit()

print_path = True

if len(sys.argv) > 4:
    if sys.argv[1] == "-n":
        print_path = False

# Create Graph

try:
    graph_file = sys.argv[1 if len(sys.argv) ==  4 else 2]
    graph = Graph()
    graph.readGraph(graph_file)
except IOError:
   print("Error: The file",  graph_file,  "can\'t be read.")
   sys.exit()

a = int(sys.argv[2 if len(sys.argv) ==  4 else 3])
b = int(sys.argv[3 if len(sys.argv) ==  4 else 4])


# Execute Breadth-First Search and count the time wasted
start_time = time.time()

try:
    length, path = graph.breadthFirstSearch(a,b)
except RuntimeError as element:
   print("Error:", element.args[0] , "is not a node.")
   sys.exit()

print("--- %f seconds ---" % (time.time() - start_time))

if length < 0:
    print("The given nodes are not connected.")
else:
    print("Path length: ", length)
    if print_path:
        print("Path between the nodes ", a, " and ", b, ": ", path)
        