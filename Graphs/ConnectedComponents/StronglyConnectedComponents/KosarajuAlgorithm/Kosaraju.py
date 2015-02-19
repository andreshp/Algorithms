#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Kosaraju's Algorithm to find the Strongly Connected Components of a Directed Graph
######################################################################################

# This program read a directed graph as an adjacency list from a file. 
# Afterwards it executes Kosaraju's algorithm on it to find a the strongly
# connected components of the graph. It then prints the size of the 5 biggest ones.
# 
# More info about topological sort: http://en.wikipedia.org/wiki/Topological_sorting

import sys   # For arguments (syc.argv) and exit (syc.exit())
import time  # To time the program

# A Graph class. A graph is represented by its adjacency list.
class Graph(object):

    # The class is conformed by these members:
    #  - adj_list : Adjacency list to represent the graph. It is implemented as a dictionary of set.
    #               The first dictionary's keys are the nodes of the graph. Its values are sets with
    #               the key's neighbours.
    #  - num_edges : Number of edges in the graph.
    #  - type_node : Type of the graph nodes. It is int by default.
    #  
    #  The graph admits multiples edges from one node to another thanks to the dictionary of dictionaries implementation.

    # Initializes a graph object
    def __init__(self, adj_list = {}, num_edges = 0, type_node = int):
        self.adj_list = adj_list
        self.num_edges = num_edges
        self.type_node = type_node

    # Read a graph from a file in adjacency list form
    def readGraph(self, file):
        data = open(file, "r")

        for line in data:
            # Get the nodes and initialize the current node adj_list
            nodes = [self.type_node(element) for element in line.split()]
            if nodes[0] not in self.adj_list:
                self.adj_list[nodes[0]] = set()
            
            # Add the neighbours to node[0] adj_list
            for i in range(1, len(nodes)):
                self.adj_list[nodes[0]].add(nodes[i])
                if nodes[i] not in self.adj_list:
                    self.adj_list[nodes[i]] = set()
            
            # Increment num_edges
            self.num_edges += len(nodes)-1

        data.close()

    # Find the Strongly Connected Components of the graph.
    def kosarajuAlgorithm(self):

        # First pass with DFS on the reverse graph.
        # The list with that determines the topological order of the meta-graph is
        # obtained. This will allows us to discover every SCC in the second pass.
        node_list = self.DFS_Loop1()
        scc_set = []; visited = set()

        # Second pass with DFS. Now it is performed in the real graph.
        # Each pass is always done in a SCC which is a sink in the meta-graph.
        # Consecuently, only that SCC is discovered. Afterwards, the SCC is 
        # "deleted" from the graph.
        for node in node_list:
            if node not in visited:
                current_scc = self.DFS(node, visited)
                if len(scc_set) < 5:
                    scc_set.append(current_scc)
                else: 
                    min_i = 0
                    for i in range(1,5):
                        if scc_set[i] < scc_set[min_i]:
                            min_i = i
                    if (scc_set[min_i] < current_scc):
                        scc_set[min_i] = current_scc 
                current_scc = []

        return scc_set

    # Return the reverse graph:
    def reverse(self):
        reverse_g = Graph({})
        for node in self.adj_list:
            reverse_g.adj_list[node] = set()
        
        for node in self.adj_list:
            for destination in self.adj_list[node]:
                reverse_g.adj_list[destination].add(node)
        return reverse_g

    def DFS_Loop1(self):        
        reverse = self.reverse()
        node_list = []; visited = set()
        for node in reverse.adj_list:
            if node not in visited:
                reverse.DFS_Reverse(node, visited, node_list)

        return node_list[::-1]

    def DFS_Reverse(self, node, visited, node_list):
        visited.add(node)

        # Each non-visited neighbour is visited:
        for neighbour in self.adj_list[node]:
            if neighbour not in visited:
                self.DFS_Reverse(neighbour, visited, node_list)

        node_list.append(node)

    # Find a Strongly Connected Component for Kosaraju Algorithm.
    # Efficiency: O(|Va| + |Ea|)
    # Parameters:
    #   - node : Current node.
    #   - visited : Set with the visited nodes.
    def DFS(self, node, visited, current_scc):
        visited.add(node); current_scc += 1

        # Each non-visited neighbour is visited:
        for neighbour in self.adj_list[node]:
            if neighbour not in visited:
                self.DFS(neighbour, visited, current_scc)



######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Sintax: Kosaraju.py <options> graph.txt \n The option -n don't print the Strongly Connected Components.")
    sys.exit()

print_scc = True

if len(sys.argv) > 2:
    if sys.argv[1] == "-n":
        print_scc = False

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
scc_set = graph.kosarajuAlgorithm()
print("--- %f seconds ---" % (time.time() - start_time))

# Print the result
if print_scc:
    print("Strongly Connected Components: ")
    for i in range(0,len(scc_set)):
        print("SCC", i+1, "(size", len(scc_set[i]), "):", scc_set[i])
else:
    print("Strongly Connected Components Size: ")
    for i in range(0,len(scc_set)):
        print("SCC", i+1, ":", len(scc_set[i]))
