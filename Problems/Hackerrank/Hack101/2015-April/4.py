#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Dijkstra Algorithm for Shortest Path (non-negative weight) Problem
#######################################################################

# This program read a weighted graph as an adjacency list from a file and a graph's
# node. Afterwards it executes de Dijkstra algorithm on it and returns the 
# length of the shortest path each other node.
# The user can choose between printing the path or not.

import sys
import time

#------------- MINHEAP IMPLEMENTATION FOR DIJKSTRA--------------#

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

#----------------- GRAPH IMPLEMENTATION ------------------#

# Node Class. Allows changing the way a node is interpreted.
class Node(object):

    # Contructor
    def __init__(self, value):
        self.key = value
        self.distance = -1
        self.index = -1
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

# A Weighted Graph class. A graph is represented by its adjacency list.
class WeightedGraph(object):

    # The class is conformed by these members:
    #  - nodes     : Dictionary which keys are the graph's nodes keys and its values the nodes of the graphs.
    #                Thanks to this dictionary the keys works as pointers to the graph nodes, what allows
    #                work with more information in each node for dijkstra algorithm.
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
    def readWeightedGraph(self, N):
        nodes = {}

        # Get the nodes and initialize the current node adj_list
        for i in range(0):
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

    # Dijkstra algorithm
    # Parameters:
    #    - node : Key of the node to which apply the algorithm.
    # Result: Each Node distance attribute has the shortest distance to the given node.
    def dijkstra(self, node):
        # Find the node with key node.
        a = self.nodes[node]
        visited = {a}; heap = MinHeap()

        # Initialize the visited set and the heap with the non-visited vertices.
        for neighbour, distance in self.adj_list[a]:
            neighbour.distance = distance
            heap.insert(neighbour)

        # Apply the Dijkstra iteration until every node is visited
        while len(visited) < len(self.adj_list):
            # Extract the node for which we can claim we have the shortest path:
            next_node = heap.min(); heap.deleteMin()
            visited.add(next_node)

            # Insert neighbours to the heap (if they aren't) or change their distance
            # if we have found a shorter path from node using next_node shortest path.
            for neighbour, distance in self.adj_list[next_node]:
                if neighbour not in visited:
                    if neighbour.distance == -1:
                        neighbour.distance = next_node.distance+distance
                        heap.insert(neighbour)
                    else:
                        neighbour.distance = min(neighbour.distance, next_node.distance+distance)
                        heap._repairUp(neighbour.index)


######################## MAIN ##########################

N = int(input())
time_sightseing = map(int, input().split())

