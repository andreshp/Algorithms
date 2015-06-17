#!/usr/bin/python

#######################################################################
# Author: Andrés Herrera Poyatos
# Universidad de Granada, June, 2015
# Indeed Prime Challengue
# Problem 4
########################################################################

import queue

def solve(tree, shorcuts, D, K):

    root = 1
    # Initializes leaves to 0
    for i in range(1, N+1):
        if len(tree[i]) <= 1:
            D[i][0] = 0

    # Initializes distances to distances with no shorcuts.
    # A BFS compute the distance just going down.
    # Then a DFS compute the distance using a node parent.
    BFS(tree,D,0)
    DFS(tree,D,0,root)

    # For each number of feasible shorcuts:
    # - For each node take the better shorcut.
    # - Update all the distances with the BFS and DFS scheme
    for j in range(1,K+1):
        for i in range(1,N+1):
            D[i][j] = D[i][j-1]
            for neighbour, distance in shorcuts[i]:
                D[i][j] = min(D[i][j], D[neighbour][j-1] + distance)
        BFS(tree,D,j)
        DFS(tree,D,j,root)
    
    for i in range(1, N+1):
        print(D[i][K])

# BFS updating the nodes distance to exit from bottom to top.
# It is implemented in an iterative way.
def BFS(tree, D, j):
    # Adds the leaves to the queue
    q = queue.Queue()
    for i in range(1, N+1):
        if len(tree[i]) == 1:
            q.put((i, -1))
    # Go up in the tree updating the distances
    while not q.empty():
        node, predecesor = q.get()
        for parent, distance in tree[node]:
            if parent != predecesor and D[parent][j] > D[node][j] + distance:
                q.put((parent, node))
                D[parent][j] = D[node][j] + distance

# DFS updating the nodes distance to exit from top to bottom.
# It is implemented in an iterative way.
def DFS(tree, D, j, root):
    stack = queue.LifoQueue()
    stack.put((root, -1))
    while not stack.empty():
        node, predecesor = stack.get()
        for child, distance in tree[node]:
            if child != predecesor:
                D[child][j] = min(D[child][j], D[node][j] + distance)
                stack.put((child, node))

#-------------------------- MAIN ----------------------------#

# Read the constrains
N, E, K = [int(x) for x in input().split()]

# Read the tree and shorcuts
tree = [[] for i in range(0,N+1)]  
shorcuts = [[] for i in range(0,N+1)]

for i in range(0,N-1):
    edge = [int(x) for x in input().split()]
    tree[edge[0]].append((edge[1], edge[2]))
    tree[edge[1]].append((edge[0], edge[2]))

for i in range(0,E):
    edge = [int(x) for x in input().split()]
    shorcuts[edge[0]].append((edge[1], edge[2]))
    shorcuts[edge[1]].append((edge[0], edge[2]))

# Build a matrix for the solution
D = [[]]*(N+1)
for i in range(0,N+1):
    D[i] = [1000000000]*(K+1)

solve(tree, shorcuts, D, K)


