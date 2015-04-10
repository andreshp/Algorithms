#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, March, 2015
# Single-Linkage Clustering Algorithm
#######################################################################

# This program read the values asociated to the vertices from a file.
# The distance between 2 vertices is calculated with those values.
# For example, if the values are a string of 0s and 1s with a fixed size,
# the hamming distance is the sum of the bits where both strings differ.
# (This is the distance considered in the code but it is easy to change).
#
#  Given a positive integer k, the program executes the Single-Linkage
# Clustering Algorithm to find the k clusters that maximize:
#                   min d(x, y)
#                   x, y are in a different cluster

import sys
import time
from gmpy2 import popcount

#------------- MINHEAP IMPLEMENTATION --------------#

# Swap two components of an array
def swap(array, i, j):
    copy = array[i]
    array[i] = array[j]
    array[j] = copy
    array[i].index = i
    array[j].index = j

# MinHeap Class.
# A heap is a representation of a complete binary tree as an array.
# The array has the Breadth-First Order of the nodes. Consecuently,
# the following equitities are true:
#    leftChild(index) = 2*index+1
#    rightChild(index) = 2*index+2
#    parent(index) = (index-1) // 2
#
# A MinHeap is a heap where there is a total order relation and verifies the following property:
#    "heap[i] >= heap[parent(i)] for all i in range(0, size())"
# analogously:
#    "Each children is greater or equal than its parent."
# 
# Consecuently,  heap[0] is the minimum of the elements of the heap.
# A MinHeap supports the following operations:
#    - Get the minimum in O(1) (return heap[0])
#    - Insert an element in O(log n)
#    - Delete an element in O(log n)
class MinHeap(object):
    
    # Init method
    def __init__(self):
        self.heap = []

    # Check if the Heap is empty
    def empty(self):
        return (not self.heap)

    # Return the min of the Heap.
    # Precondition: The Heap must be not empty.
    def min(self):
        return self.heap[0] # A MinHeap keeps the min in the first position.

    # Size of the Heap
    def size(self):
        return len(self.heap)

    # Insert Method
    def insert(self, element):
        element.index = len(self.heap)
        self.heap.append(element)
        self._repairUp(len(self.heap)-1)

    # Insert the elements of an array
    def insertArray(self, array):
        for number in array:
            self.insert(number)

    # Delete an element from the Heap
    # Precondition: The Heap must be not empty. 
    def delete(self, index):
        swap(self.heap, index, len(self.heap)-1)
        self.heap.pop()
        self._repairDown(index)

    # Delete min from the Heap.
    # Precondition: The Heap must be not empty. 
    def deleteMin(self):
        swap(self.heap, 0, len(self.heap)-1)
        self.heap.pop()
        self._repairDown(0)

    # Change the value of an element and repair the MinHeap Structure.
    def changeElement(self, index, value):
        self.heap[index] = value
        self.repairHeap(index)

    # Execute HeapSort to the elements of the heap.
    def heapSort(self):
        sorted_array = []
        while(not self.empty()):
            sorted_array.append(self.min())
            self.deleteMin()
        return sorted_array

    # Print Heap by levels
    def printHeap(self):
        elements_level = 1
        print("Heap:")
        for i in range(0, len(self.heap)):
            if i == elements_level:
                elements_level += elements_level+1; print()
            print(self.heap[i], " ", end="")
    
        print(); print()
    
    # Check that it is a MinHeap.
    # The invariant is checked.
    def _checkHeap(self):
        is_heap = True; fail = -1 
        for i in range(1, len(self.heap)):
            if self.heap[i] < self.heap[(i-1) // 2]:
                is_heap = False; fail = i; break

        return is_heap, fail

    # Repair the Min Heap invariant:
    # Each parent key is less or equal than their children keys.
    def _repairHeap(self, index):
        self._repairUp(index)
        self._repairDown(index)

    # Go up in the Heap repairing its invariant
    def _repairUp(self, index):
        parent = (index-1) // 2
        while index > 0:
            if self.heap[index] < self.heap[parent]:
                swap(self.heap, index, parent)
            else: break
            index = parent
            parent = (index-1) // 2

    # Go down in the Heap repairing its invariant
    def _repairDown(self, index):
        child = 2 * index + 1
        while child < len(self.heap):
            if child + 1 < len(self.heap) and self.heap[child] > self.heap[child+1]:
                child += 1
            if self.heap[index] > self.heap[child]:
                swap(self.heap, child, index)
            else: break
            index = child
            child = 2 * index +1

#------------- VERTEX IMPLEMENTATION --------------#

# Vertex Class. 
# It keeps the vertex value and the cluster
# asociated with the vertex.
class Vertex(object):
    # Contructor
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.cluster = Cluster(self)
        self.edge = -1               # Used in the clustering algorithm
        self.distance = float("inf") # Used in the clustering algorithm
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
    # Distance between two vertices.
    # In this case, it is the Hamming Distance.
    def hammingDistance(self, vertex):
        return popcount(self.value ^ vertex.value)

#------------- CLUSTER IMPLEMENTATION --------------#

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
    def sameCluster(node1, node2):
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

#------------- SINGLE-LINKAGE CLUSTERING --------------#

# Single-Linkage Clustering Algorithm
# Parameters:
#  - edges : 
#  - k : Number of clusters
def SLClustering(vertices, k):
    
    # For each vertex, we find the one to which there is less distance (and not used yet).
    for i in range(1, len(vertices)-1):
        for j in range(i+1, len(vertices)):
            new_distance = vertices[i].hammingDistance(vertices[j])
            if new_distance < vertices[i].distance:
                vertices[i].distance = new_distance
                vertices[i].edge = j

    for i in range(2, len(vertices)):
        for j in range(1, i):
            if vertices[j].edge != i:
                new_distance = vertices[i].hammingDistance(vertices[j])
                if new_distance < vertices[i].distance:
                    vertices[i].distance = new_distance
                    vertices[i].edge = j

    # Build a min heap with all the vertices:
    heap = MinHeap()
    for i in range(1, len(vertices)):
        heap.insert(vertices[i])

    # Add the max_edges times the edge between separated clusters
    # that has the minimum cost and join the respective clusters.
    max_edges = len(vertices) - k - 1
    added_edges = 0
    while added_edges < max_edges:
        # Next vertex of the heap
        next_vertex = heap.min(); heap.deleteMin()

        # If it has a valid edge (an edge between two different clusters)
        # join those clusters and count it.
        if not Cluster.sameCluster(next_vertex, vertices[next_vertex.edge]):
            Cluster.join(next_vertex, vertices[next_vertex.edge])
            added_edges += 1

        # Put the vertex again in the heap with the edge with minimum cost
        # from those which go to a different cluster.
        next_vertex.distance = float("inf")
        next_vertex.edge = -1
        for j in range(1, len(vertices)):
            if not Cluster.sameCluster(next_vertex, vertices[j]):
                new_distance = next_vertex.hammingDistance(vertices[j])
                if new_distance < next_vertex.distance:
                    next_vertex.distance = new_distance
                    next_vertex.edge = j
        if next_vertex.distance < float("inf"):
            heap.insert(next_vertex)
        if added_edges % 10 == 0:
            print("Completed: ", (added_edges / max_edges) * 100.0)
    # Find the maximum spacing distance between k clusters
    max_spacing = float("inf")
    while Cluster.sameCluster(heap.min(), vertices[heap.min().edge]):
        heap.deleteMin()
    max_spacing = heap.min().distance

    return max_spacing

# Read the vertices from a file.
# It initializes the vertices, the clusters (one per vertex)
# and return list with the vertices.lk
def readVertices(distances_file):
    data = open(distances_file, "r")

    # Build the vertices
    first_line = data.readline()
    num_vertices = int(first_line.split()[0])
    num_bits = int(first_line.split()[1])

    vertices = [None] * (num_vertices+1)

    # Each line corresponds to a vertex
    # It contains the value of the vertex, a string with num_bits bits of 0s and 1s,
    # such as: 1 1 1 0 0 0 0 0 1 1 0 1 0 0 1 1 1 1 0 0 1 1 1 1.
    # We represent it as an integer in base 2.
    i = 1
    for line in data:
        vertices[i] = Vertex(i, int(line.replace(" ", ""), 2))
        i += 1

    return vertices

######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Sintax: SLClusteringDistance.py <options> distances.txt k \n The option -n don't print the clusters.")
    sys.exit()

print_clusters = True

if len(sys.argv) > 3:
    if sys.argv[1] == "-n":
        print_clusters = False

# Read the distances between the vertices and the value of k
try:
    distances_file = sys.argv[1 if len(sys.argv) ==  3 else 2]
    vertices = readVertices(distances_file)
    k = int(sys.argv[2 if len(sys.argv) == 3 else 3])
except IOError:
   print("Error: The file",  distances_file,  "can\'t be read.")
   sys.exit()

# Execute clustering algorithm and compute the time wasted
start_time = time.time()
try:
    maximum_spacing_distance = SLClustering(vertices, k)
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
