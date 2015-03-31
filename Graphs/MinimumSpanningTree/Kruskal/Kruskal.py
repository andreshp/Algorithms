#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, March, 2015
# Kruskal Algorithm for Minimum Spanning Tree Problem
#######################################################################

# This program read a weighted graph as an adjacency list from a file. 
# Afterwards it executes de Kruskal algorithm to find the minimum spanning tree.
# This implementation runs in O(|E| log |V| time) with an Union-Find Structure

import sys
import time
import functools # reduce

#----------------- GRAPH IMPLEMENTATION ------------------#

# Node Class. Allows changing the way a node is interpreted.
class Node(object):
    # Contructor
    def __init__(self, value):
        self.key = value
        self.set = Set(self)
    # Overloading comparisons operators
    def __lt__(self, other):
        return (self.distance < other.distance)
    def __le__(self, other):
        return(self.distance <= other.distance)
    def __gt__(self, other):
        return(self.distance > other.distance)
    def __ge__(self, other):
        return(self.distance >= other.distance)
    # Hash function
    def __hash__(self):
        return self.key.__hash__()

# Union - Find Data Structure for Kruskal's Algorithm
class Set(object):
    # Number of active sets (class attribute)
    n_sets = 0
    # Initializes a set
    def __init__(self, node):
        Set.n_sets += 1
        self.members = [node]
    # Adds a node to the set
    def add(self, node):
        self.members.append(node)
        node.set = self
    # Size of the set
    def size(self):
        return len(self.members)
    # Get the set of a given node. It is a class method
    def getSet(node):
        return node.set
    # Returns True if both nodes are in the same set.
    # Returns False otherwise.
    def sameSet(node1, node2):
        return node1.set is node2.set
    # Class method to join nodes' set in just one
    def join(node1, node2):
        node1.set._join(node2.set)
    # Both sets are joined in one of them
    def _join(self, other):
        if self.size() < other.size():
            self.__join(other)
        else:
            other.__join(self)
    # Private method to accomplish the join
    def __join(self, other):
        for node in self.members:
            other.add(node)
        self.members = []
        Set.n_sets -= 1

# A Weighted Graph class. A graph is represented by its adjacency list.
class WeightedGraph(object):

    # The class is conformed by these members:
    #  - nodes     : Dictionary which keys are the graph's nodes keys and its values the nodes of the graphs.
    #                Thanks to this dictionary the keys works as pointers to the graph nodes, what allows
    #                work with more information in each node for kruskal algorithm.
    #  - adj_list  : Adjacency list to represent the graph. It is implemented as a dictionary of sets.
    #                The first dictionary's keys are the nodes (Objects Node) of the graph. Its values are sets with
    #                tuples (key's neighbours, distance of the edge).
    #  - outdegree : Dictionary which maps for each node its outdegree (The number of edges leaving from this node).
    #  - num_edges : Number of edges in the graph.
    #  - type_node : Type of the graph nodes. It is int by default.
 
    # Initializes a graph object
    def __init__(self, adj_list = {}, outdegree = {}, num_edges = 0, type_node = int):
        self.nodes = {}
        self.adj_list = adj_list
        self.outdegree = outdegree
        self.num_edges = num_edges
        self.type_node = type_node

    # Read a weighted graph from a file in adjacency list form
    def readWeightedGraph(self, file):
        data = open(file, "r")
        nodes = {}

        # Get the nodes and initialize the current node adj_list
        for line in data:
            node = self.type_node(line.split(" ", 1)[0])
            nodes[node] = Node(node)
            self.adj_list[nodes[node]] = set()

        data.seek(0, 0) # Set data offset to the beginning of the file
 
        # Add the neighbours to each node in adj_list
        for line in data:
            info = [element for element in line.split()]
            node = nodes[self.type_node(info[0])]        # Get the current node
 
            for i in range(1, len(info)):
                pair = info[i].split(',')
                self.adj_list[node].add( (nodes[self.type_node(pair[0])], int(pair[1])) )

            # Increment num_edges and add degree(node) to outdegree:
            self.num_edges += len(info)-1; self.outdegree[node] = len(info)-1; self.nodes = nodes

        data.close()

    # Kruskal algorithm
    def kruskal(self):

        # Build the list with the edges
        edges = set()
        for node in self.adj_list.keys():
            for neighbour, distance in self.adj_list[node]:
                edges.add((distance, node, neighbour))
        edges = list(edges)

        # Sort the list with the edges (|E| log |V| time)
        edges.sort(key=lambda edge: edge[0])
        mst_distance = 0; mst_edges = []

        # For each edge in edges, if it does not create a cycle
        # add it to the future spanning tree.
        for edge in edges:
            if not Set.sameSet(edge[1], edge[2]):
                mst_edges.append(edge)
                mst_distance += edge[0]
                Set.join(edge[1], edge[2])
                if len(mst_edges)+1 == len(self.nodes):
                    break

        return mst_distance, mst_edges

######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Sintax: Kruskal.py <options> graph.txt \n The option -n don't print the MST.")
    sys.exit()

print_tree = True

if len(sys.argv) > 2:
    if sys.argv[1] == "-n":
        print_tree = False

# Create WeightedGraph
try:
    graph_file = sys.argv[1 if len(sys.argv) ==  2 else 2]
    graph = WeightedGraph()
    graph.readWeightedGraph(graph_file)
except IOError:
   print("Error: The file",  graph_file,  "can\'t be read.")
   sys.exit()

# Execute Kruskal and count the time wasted
start_time = time.time()
try:
    distance, edges = graph.kruskal()
except RuntimeError as element:
   print("Error:", element.args[0] , "is not a node.")
   sys.exit()
print("--- %f seconds ---" % (time.time() - start_time))

# Print the result
print("Total distance of the MST:", distance)

# If chosen, print the tree
if print_tree:
    print("Minimum Spanning Tree:")
    print("Edge = (node1, node2, distance)")
    for edge in edges:
        print((edge[1].key, edge[2].key, edge[0]))

