#!/usr/bin/env python

###################################################################
# Author: Andrés Herrera Poyatos
# Email:  andreshp9@gmail.com
# Date:   2015-06-22
# Last Modified by:   andreshp
# Last Modified time: 2015-06-22
# File Name: DynamicPrograming-QuadraticSolution.py
###################################################################

#----------------------- SOLUTION EXPLANATION ------------------------#

# Let's denote LIS[i] the length of the longest increasing sequence
# ending at component i. 
# 
# We want to find the value LIS[i] for all i. It is trivial that the longest
# increasing sequence length is the maximum of LIS[i] for all i.
# 
# We have:
# - LIS[0] = 1 
# - LIS[i] = max(LIS[j] + 1 for al j in J) if J not empty else 1
#   where J = {j: i > j, A[i] > A[j]}
# 
# This allows us to compute LIS[i] for all i easily in O(n²) and, thus,
# the longest increasing subsequence length.

def longestIncreasingSubsequenceLength(A):
    LIS = [1] * len(A)
    for i in range(1, len(A)):
        for j in range(0, i):
            if A[j] < A[i]:
                LIS[i] = max(LIS[i], LIS[j]+1)
    return max(LIS)

# But we can also keep the track of the longest increasing subsequence
# during the process. In order to do so let's define P[i] as the 
# component before i in the longest increasing subsequence ending at i.
# At the beginning of each step, P[i] = -1. When we update LIS[i] with
# LIS[j]+1, we update P[i] to j, getting at the end the desired index.
# This keeps the track of the longest increasing subsequence ending at 
# component i: [i, P[i], P[P[i]], ..., ] until we get a -1. 
# 
# Once the algorithm has ended, we choose the component i which maximizes
# LIS and [i, P[i], P[P[i]], ..., ] is the longest increasing subsequence.

def longestIncreasingSubsequenceIndexes(A):
    LIS = [1] * len(A)
    P = [-1] * len(A)

    for i in range(1, len(A)):
        for j in range(0, i):
            if A[j] < A[i] and LIS[i] < LIS[j]+1:
                LIS[i] = LIS[j]+1
                P[i] = j

    i = LIS.index(max(LIS))
    sol = []
    while i != -1:
        sol.append(i)
        i = P[i]
    return  sol[::-1]

#------------------------------ MAIN -------------------------------#

V = [1,2,4,6,3,5]
print("Longest incresing subsequence of ", V)
print([V[i] for i in longestIncreasingSubsequenceIndexes(V)])
print("Length of the longest incresing subsequence of ", V)
print(longestIncreasingSubsequenceLength(V))
