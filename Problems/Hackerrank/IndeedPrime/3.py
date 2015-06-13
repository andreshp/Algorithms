#!/usr/bin/python

#######################################################################
# Author: Andrés Herrera Poyatos
# Universidad de Granada, June, 2015
# Indeed Prime Challengue
# Problem 3
########################################################################

#-------------------- FUNCTIONS ----------------------#

# Find the minimum product subinterval
def solveQuery1(array, u, v):
    min_prod = array[u]
    index = [u]
    i = 0; j = -1

    for k in range(u+1,v+1):
        if array[k] < min_prod:
            index = [k]
            min_prod = array[k]
        elif array[k] == 1 and 1 == min_prod:
            if index[-1] == k-1:
                index.append(k)
            else:
                if j-i+1 < len(index):
                    i = index[0]
                    j = index[-1]
                index = [k]

    if j-i+1 < len(index):
        i = index[0]
        j = index[-1]

    if min_prod == 0:
        print(0, u, v)
    elif min_prod == 1:
        print(1, i, j)
    else:
        print(min_prod, index[0], index[0])

# Assign v to u
def solveQuery2(array, u, v):
    array[u] = v

#---------------------- MAIN ------------------------#

# Read array and constants
N, Q = [int(x) for x in input().split()]
array = [0]*(N+1)
array[1::] = [int(x) for x in input().split()]

# Do Q queries
for i in range(0, Q):
    q, u, v = [int(x) for x in input().split()]
    if q == 1:
        solveQuery1(array, u, v)
    else:
        solveQuery2(array, u, v)
