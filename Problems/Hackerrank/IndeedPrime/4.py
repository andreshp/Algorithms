#!/usr/bin/python

#######################################################################
# Author: Andrés Herrera Poyatos
# Universidad de Granada, June, 2015
# Indeed Prime Challengue
# Problem 4
########################################################################

import queue

def expandShorcut(tree, shorcuts, sol, count_s, node):
    q = queue.Queue()
    q.put(node)
    while not q.empty():
        node = q.get()
        for neighbour, distance in tree[node]:
            if sol[neighbour] > sol[node] + distance:
                sol[neighbour] = sol[node] + distance
                count_s[neighbour] = count_s[node]
                q.put(neighbour)

def useShortcuts(tree, shorcuts, sol, count_s, K):
    for i in range(0,len(shorcuts)):
        for neighbour, distance in shorcuts[i]:
            if count_s[neighbour] <= K and sol[neighbour] > sol[i] + distance:
                sol[neighbour] = sol[i] + distance
                count_s[neighbour] += 1
                expandShorcut(tree, shorcuts, sol, count_s, neighbour)  

#-------------------------- MAIN ----------------------------#

N, E, K = [int(x) for x in input().split()]

tree = [set() for i in range(0,N+1)]  
shorcuts = [set() for i in range(0,N+1)]

for i in range(0,N-1):
    edge = [int(x) for x in input().split()]
    tree[edge[0]].add((edge[1], edge[2]))
    tree[edge[1]].add((edge[0], edge[2]))

for i in range(0,E):
    edge = [int(x) for x in input().split()]
    shorcuts[edge[0]].add((edge[1], edge[2]))
    shorcuts[edge[1]].add((edge[0], edge[2]))

sol = [1000000000]*(N+1)
count_s = [0]*(N+1)

q = queue.Queue()

for i in range(1, N+1):
    if len(tree[i]) == 1:
        sol[i] = 0
        q.put((i, None))

while not q.empty():
    node, predecesor = q.get()
    for neighbour, distance in tree[node]:
        if neighbour != predecesor and sol[neighbour] > sol[node] + distance:
            sol[neighbour] = sol[node] + distance
            q.put((neighbour, node))

useShortcuts(tree, shorcuts, sol, count_s, K)

for i in range(1, N+1):
    print(sol[i])

