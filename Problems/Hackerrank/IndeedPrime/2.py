#!/usr/bin/python

#######################################################################
# Author: Andrés Herrera Poyatos
# Universidad de Granada, June, 2015
# Indeed Prime Challengue
# Depth-First Search and Topological Sort to solve problem 2
########################################################################

# Use topological sort idea to find the largest path between two nodes.
# If there is a cycle then solution is never.

# A Graph class. A graph is represented by its adjacency list.
class Graph(object):

    # The class is conformed by these members:
    #  - adj_list : Adjacency list to represent the graph. It is implemented as a dictionary of dictionaries.
    #               The first dictionary's keys are the nodes of the graph. Its values are dictionaries with
    #               the key's neighbours and the number of edges between them.
    #  - num_edges : Number of edges in the graph.
    #  - type_node : Type of the graph nodes. It is int by default.
    #  
    #  The graph admits multiples edges from one node to another thanks to the dictionary of dictionaries implementation.

    # Initializes a graph object
    def __init__(self, adj_list = [], num_edges = 0):
        self.adj_list = adj_list
        self.num_edges = num_edges

    # Read a graph with the subjects
    def readGraph(self):
        N, self.num_edges = [int(x) for x in input().split()]
        self.adj_list = [[] for i in range(0,N) ]
        for i in range(0, self.num_edges):
            u, v = [int(x) for x in input().split()]
            self.adj_list[v].append(u)

    # Find a topological sort of the graph in case it is acyclic.
    # This allows us finding the largest path from a subject to another.
    # The length of this path is the number of semesters needed.
    # Otherwise it raise an exception.
    # Efficiency:  O(|V| + |E|)
    def solve(self):
        largest_path = [1]*len(self.adj_list)
        visited = set()
         
        for node in range(0,len(self.adj_list)):
            if node not in visited:
                # DPS is performed starting in the node:
                visited.add(node); path = {node}
                self.depthFirstSearch(node, visited, largest_path, path)
            elif len(visited) == len(self.adj_list):
                break

        return max(largest_path)

    # Find a subarray of the topological order.
    # Efficiency: O(|Va| + |Ea|)
    # Parameters:
    #   - a : Current node.
    #   - visited : Set with the visited nodes.
    #   - largest_path :
    #   - path : Current path. A path is a sucesion of nodes connected by an edge.
    #            It is only used to check that the graph is acyclic.
    def depthFirstSearch(self, a, visited, largest_path, path):
        
        # Each non-visited neighbour is visited:
        for neighbour in self.adj_list[a]:
            if neighbour not in visited:
                visited.add(neighbour); path.add(neighbour)
                self.depthFirstSearch(neighbour, visited, largest_path, path)
                path.remove(neighbour) # Set the path as it was before the call.
            elif neighbour in path: 
                # A path from an element to itself (a cycle) has been found.
                # Consecuently, the graph is not acyclic so it doesn't have
                # a topological ordering.
                raise RuntimeError(path)
            
            largest_path[a] = max(largest_path[a], largest_path[neighbour]+1)


######################## MAIN ##########################

T = int(input())
for i in range(0,T):
    graph = Graph(  )
    graph.readGraph()
    try:
        sol = graph.solve()
        print("Case {}:".format(i+1), sol, "semester(s)")
    except RuntimeError:
        print("Case {}:".format(i+1),"Never Ends")
