#!/usr/bin/python

#######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, February, 2015
# Depth-First Search for finding a Topological Sort of a Directed Graph
########################################################################

# This program read a directed graph as an adjacency list from a file. 
# Afterwards it executes the DFS algorithm on it to find a topological sort
# of the graph if it is possible (the graph must be acyclic, what is 
# checked in the code). It then prints the result.
# 
# More info about topological sort: http://en.wikipedia.org/wiki/Topological_sorting

import sys   # For arguments (syc.argv) and exit (syc.exit())
import time  # To time the program

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

    # Find a topological sort of the graph in case it is acyclic.
    # Otherwise it raise an exception.
    # Efficiency:  O(|V| + |E|)
    def topologicalSort(self):
        sorted_nodes = []; visited = set()

        for node in self.adj_list:
            if node not in visited:
                # DPS is performed starting in the node:
                visited.add(node); path = {node}
                self.depthFirstSearch(node, visited, sorted_nodes, path)
            elif len(visited) == len(self.adj_list):
                break

        return sorted_nodes[::-1] # They are in the reverse order

    # Find a subarray of the topological order.
    # Efficiency: O(|Va| + |Ea|)
    # Parameters:
    #   - a : Current node.
    #   - visited : Set with the visited nodes.
    #   - sorted_nodes : Nodes visited in reverse topological ordering.
    #   - path : Current path. A path is a sucesion of nodes connected by an edge.
    #            It is only used to check that the graph is acyclic.
    def depthFirstSearch(self, a, visited, sorted_nodes, path):
        # Each non-visited neighbour is visited:
        for neighbour in self.adj_list[a]:
            if neighbour not in visited:
                visited.add(neighbour); path.add(neighbour)
                self.depthFirstSearch(neighbour, visited, sorted_nodes, path)
                path.remove(neighbour) # Set the path as it was before the call.
            else:
                if neighbour in path: 
                    # A path from an element to itself (a cycle) has been found.
                    # Consecuently, the graph is not acyclic so it doesn't have
                    # a topological ordering.
                    raise RuntimeError(path)

        # The node is added to the topological ordering. Every neighbour is before him.
        # (If any neighbour was already visited before this call it has already added to the list).
        sorted_nodes.append(a)



######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Sintax: TopologicalSort.py <options> graph.txt \n The option -n don't print the topological ordering.")
    sys.exit()

print_order = True

if len(sys.argv) > 2:
    if sys.argv[1] == "-n":
        print_order = False

# Create Graph

try:
    graph_file = sys.argv[1 if len(sys.argv) ==  2 else 2]
    graph = Graph()
    graph.readGraph(graph_file)
except IOError:
   print("Error: The file",  graph_file,  "can\'t be read.")
   sys.exit()

# Execute the topological sort algorithm
start_time = time.time()
try:
    topological_order = graph.topologicalSort()
except RuntimeError as path:
   print("Error: The directed graph is not acyclic: ", path.args[0])
   sys.exit()
print("--- %f seconds ---" % (time.time() - start_time))

# Print the result
if print_order:
    print("Topological Order: ", topological_order)
else:
    print("The graph is acyclic.")