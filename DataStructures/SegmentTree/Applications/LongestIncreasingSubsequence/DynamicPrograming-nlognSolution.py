#!/usr/bin/env python

###################################################################
# Author: Andrés Herrera Poyatos
# Email:  andreshp9@gmail.com
# Date:   2015-06-22
# Last Modified by:   andreshp
# Last Modified time: 2015-06-22
# File Name: DynamicPrograming-nlognSolution.py
###################################################################

from bisect import *

#----------------------- SOLUTION EXPLANATION ------------------------#

# Let's take two list, S and Si initialized to [A[0]] and [0] respectively and will have
# (during all the algorithm) the following properties:
# 
# - Si has the indexes (according to A) of elements added to S. 
# - S is sorted.
# - After iteration i, the length of S (same than Si) is the length of the longest 
#   increasing sequence of A[0:i+1]. Consequently, when the algorithm finishes len(S) 
#   is our solution.
#
# Let's also keep a list P defined as follow, P[i] is the predecessor of element with index i
# in the longest increasing subsequence ending at element with index i (same P than in O(n²) approach).
#
# At iteration i (where i range from 1 to len(A)-1, both included) we have two options:
#  - If A[i] is greater than the last element in S we append it to S (and i to Si). Besides, P[i] = Si[-1]
#    (Si[-1] = last element of Si)
#  - Else we find the index pos such as:
#              S[j] < A[i] for all j < pos and S[j] >= A[i] for all j >= pos
#    We can do a binary search for this since S is supposed to be sorted.
#    Then assign A[i] to S[pos] and i to Si[pos]. Also P[i] = Si[pos-1]
#
# From P definition the following code obtains the LSI ending at i:
#    LIS = []
#    while  i != -1:
#        LIS.append(i)
#        i = P[i]
#    return LIS[::-1]
#
# Let's proof that the algorithm is correct by induction. The induction hypothesis 
# which we want to proove at every iteration i is that after the iteration:
#   - The length of S is the length of the longest increasing sequence for A[0:i+1].
#   - S is sorted 
#   - Si[-1] has the index of the last element of the A[0:i+1] LSI wich ends first.
#   - P[i] let us obtain (as explained before) the LSI ending at i.
# 
# Let's proove it for every i:
#   - If i = 0 (base case) it is trivial by definition of S.
#   - Supposes the induction hypothesis for i-1 >= 0. We have 2 cases:
#      + A[i] > S[-1]. Then the LSI ending at i is any LSI for A[0:i] + A[i]. 
#        Consequently, it is easy to see that the operations keep the hypothesis.
#      + A[i] <= S[-1]. Then we can't get a longer LSI for A[0:i+1] than the one of A[0:i] since
#        
#        

#---------------------------- FUNCTIONS ----------------------------#

def longestIncreasingSubsequence(A):
    P = [-1] * len(A)
    S = [A[0]]; Si = [0]
    for i in range(1,len(A)):
        if A[i] > S[-1]:
            S.append(A[i])
            P[i] = Si[-1]
            Si.append(i)
        else:
            pos = bisect_left(S,A[i])
            S[pos] = A[i]
            Si[pos] = i
            P[i] = Si[pos-1] if pos > 0 else -1
    LIS = []; i = Si[-1]
    while  i != -1:
        LIS.append(i)
        i = P[i]
    return LIS[::-1]

def longestIncreasingSubsequenceLength(A):
    S = [A[0]]
    Si = [0]
    for i in range(1,len(A)):
        if A[i] > S[-1]:
            S.append(A[i])
            Si.append(i)
        else:
            pos = bisect_left(S,A[i])
            S[pos] = A[i]
            Si[pos] = i
    return len(S)

#------------------------------ MAIN -------------------------------#

V = [1,2,4,6,3,5]
print("Longest incresing subsequence of ", V)
print(list(map(lambda x: V[x], longestIncreasingSubsequence(V))))
print("Length:", longestIncreasingSubsequenceLength(V))