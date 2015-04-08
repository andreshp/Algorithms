#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, March, 2015
# Single-Linkage Clustering Algorithm
#######################################################################

# This program read the distance between the vertices from a file.
# Afterwards, given a positive integer k, it executes the Single-Linkage
# Clustering Algorithm to find the k clusters that maximize:
#                   min d(x, y)
#                   x, y are in a different cluster

import sys
import time

# Vertex Class. 
# It keeps an index and the cluster to wich the vertex
# 
class Vertex(object):
    # Contructor
    def __init__(self, value):
        self.key = value
        self.cluster = Cluster(self)
    # Hash function
    def __hash__(self):
        return self.key.__hash__()

# Union - Find Data Structure
# Each vertex has an asociated cluster. We can:
#  - Get the asociated cluster of a vertex in O(1)
#  - Join two clusters of size r and s in O(min{r,s})
class Cluster(object):
    # Number of active clusters (class attribute)
    n_clusters = 0
    # Initializes a cluster
    def __init__(self, vertex):
        self.index = Cluster.n_clusters
        Cluster.n_clusters += 1
        self.members = [vertex]
    # Adds a vertex to the cluster
    def add(self, vertex):
        self.members.append(vertex)
        vertex.cluster = self
    # Size of the cluster
    def size(self):
        return len(self.members)
    # Get the cluster of a given vertex. It is a class method
    def getSet(vertex):
        return vertex.cluster
    # Returns True if both nodes are in the same cluster.
    # Returns False otherwise.
    def sameSet(node1, node2):
        return node1.cluster is node2.cluster
    # Class method to join nodes' cluster in just one
    def join(node1, node2):
        node1.cluster._join(node2.cluster)
    # Both clusters are joined in one of them
    def _join(self, other):
        if self.size() < other.size():
            self.__join(other)
        else:
            other.__join(self)
    # Private method to accomplish the join
    def __join(self, other):
        for vertex in self.members:
            other.add(vertex)
        self.members = []
        Cluster.n_clusters -= 1
    # Hash function
    def __hash__(self):
        return self.index.__hash__()


# Single-Linkage Clustering Algorithm
# Parameters:
#  - edges : 
#  - k : Number of clusters
def SLClustering(edges, k):
    # Sort the list with the edges ( n^2 log n time) where n is the number of vertices
    edges.sort(key=lambda edge: edge[2])

    # For each edge in edges, if it does not create a cycle
    # add it to the future spanning tree.
    for i in range(0,len(edges)):
        if not Cluster.sameSet(edges[i][0], edges[i][1]):
            Cluster.join(edges[i][0], edges[i][1])
            if Cluster.n_clusters == k:
                i += 1
                while(Cluster.sameSet(edges[i][0], edges[i][1])):
                    i += 1
                return edges[i][2]

# Read the distances between the vertices from a file.
# It initializes the vertices, the clusters (one per vertex)
# and return the vertices and a list with the edges.
def readDistances(distances_file):
    data = open(distances_file, "r")

    # Build the vertices
    num_vertices = int(data.readline())
    vertices = [None] * (num_vertices+1)
    for i in range(1, num_vertices+1):
        vertices[i] = Vertex(i)

    # Get the edges with the distances between the vertex
    edges = []
    for line in data:
        edge = [int(x) for x in line.split()]
        edges.append( (vertices[edge[0]], vertices[edge[1]], edge[2]) )

    return vertices, edges

######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Sintax: SLClustering.py <options> distances.txt k \n The option -n don't print the clusters.")
    sys.exit()

print_clusters = True

if len(sys.argv) > 3:
    if sys.argv[1] == "-n":
        print_clusters = False

# Read the distances between the vertices and the value of k
try:
    distances_file = sys.argv[1 if len(sys.argv) ==  3 else 2]
    vertices, edges = readDistances(distances_file)
    k = int(sys.argv[2 if len(sys.argv) == 3 else 3])
except IOError:
   print("Error: The file",  distances_file,  "can\'t be read.")
   sys.exit()

# Execute clustering algorithm and compute the time wasted
start_time = time.time()
try:
    maximum_spacing_distance = SLClustering(edges, k)
except RuntimeError as element:
   print("Error:", element.args[0] , "is not a vertex.")
   sys.exit()
print("--- %f seconds ---" % (time.time() - start_time))

# Print the result
print("Maximum Spacing of a", k, "-Clustering:", maximum_spacing_distance)

# If chosen, print the clusters
if print_clusters:
    print("Clusters:")
    clusters = set()
    for j in range(1,len(vertices)):
        clusters.add(vertices[j].cluster)

    i = 1
    for cluster in clusters:
        print("Cluster", i, ":")
        for vertex in cluster.members:
            print(vertex.key, end=" ")
        print()
        i += 1
