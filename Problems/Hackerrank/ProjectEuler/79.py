#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-17
# Last Modified by:   andreshp
# Last Modified time: 2015-06-17
# File Name: 79.py
###################################################################

import math

#---------------------------- GRAPH IMPLEMENTATION ----------------------------#

# A Graph class. A graph is represented by its adjacency list.
class Graph(object):

    # The class is conformed by these members:
    #  - adj_list : Adjacency list to represent the graph. It is implemented as a dictionary of dictionaries.
    #               The first dictionary's keys are the nodes of the graph. Its values are dictionaries with
    #               the key's neighbours and the number of edges between them.
    #  
    #  The graph admits multiples edges from one node to another thanks to the dictionary of dictionaries implementation.

    # Initializes a graph object
    def __init__(self, adj_list = {}):
        self.adj_list = adj_list

    # Read a graph from stdin
    def readGraph(self):
        T = int(input())

        for i in range(0,T):
            line = input()
            if len(line) > 3:
                raise NameError

            for c in line:
                if ord(c) not in self.adj_list:
                    self.adj_list[ord(c)] = set()

            if line[0] != line[1]:
                self.adj_list[ord(line[0])].add(ord(line[1]))
            if line[1] != line[2]:
                self.adj_list[ord(line[1])].add(ord(line[2]))
 
        for key in self.adj_list.keys():
            self.adj_list[key] = sorted(list(self.adj_list[key]))[::-1]

        for node in self.adj_list.keys():
            reachable_nodes = []
            self.depthFirstSearch(node,{node},reachable_nodes,{node})
            self.adj_list[node] = set()
            for x in reachable_nodes:
                if x != node: 
                    self.adj_list[node].add(x)
            self.adj_list[node] = sorted(list(self.adj_list[node]))[::-1]

    # Find a topological sort of the graph in case it is acyclic.
    # Otherwise it raise an exception.
    # Efficiency:  O(|V| + |E|)
    def topologicalSort(self):
        sorted_nodes = []; visited = set()
        nodes = sorted(list(self.adj_list.keys()))[::-1]

        for node in nodes:
            if node not in visited:
                # DPS is performed starting in the node:
                visited.add(node); path = {node}
                self.depthFirstSearch(node, visited, sorted_nodes, path)

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
            elif neighbour in path: 
                # A path from an element to itself (a cycle) has been found.
                # Consecuently, the graph is not acyclic so it doesn't have
                # a topological ordering.
                raise RuntimeError(path)
        sorted_nodes.append(a)

#------------------------------ MAIN -------------------------------#

try:
    g = Graph()
    g.readGraph()
    print("".join([chr(x) for x in g.topologicalSort()]))
except RuntimeError:
    print("SMTH WRONG")