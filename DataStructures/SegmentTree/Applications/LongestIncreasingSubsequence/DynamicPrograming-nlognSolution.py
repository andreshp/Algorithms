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
# From P definition the following code obtains the LIS ending at i:
#    LIS = []
#    while  i != -1:
#        LIS.append(i)
#        i = P[i]
#    return LIS[::-1]
#
# Let's proof that the algorithm is correct by induction. The induction hypothesis 
# which we want to proove at every iteration i is that after the iteration:
#   1. The length of S is the length of the longest increasing sequence for A[0:i+1].
#   2. S is sorted 
#   3. Si[-1] has the index of the last element of the A[0:i+1] LIS with smaller ending value.
#   4. P[i] let us obtain (as explained before) the LIS ending at i.
# 
# Let's proove it for every i:
#   - If i = 0 (base case) it is trivial by definition of S.
#   - Supposes the induction hypothesis for i-1 >= 0. We have 2 cases:
#      + A[i] > S[-1]. Then the LIS ending at i is any LIS for A[0:i] + A[i]. 
#        Consequently, it is easy to see that the operations keep the hypothesis.
#      + A[i] <= S[-1]. Then we can't get a longer LIS for A[0:i+1] than the one of A[0:i] since
#        if there were one then the first |S| elements would be a LIS for A[0:i] so A[i] is greater
#        than those |S| elemens. However, the greater one of those is smallest than S[-1] because of 3,
#        contradiction. So 1 is achieved. Clearly 2 is achieved after binary search and assignations.
#        3 isn't even touched. Now, we want to compute one of the LIS ending at i. Let's supose that
#        we have one, call it B of indexes Bi. Then B[:len(B)-1] is a LIS ending at Bi[-2]. But we
#        already have one computed. Furthermore, Bi[-2] < A[i]. If we find pos with the binary search,
#        the LIS computed for pos-1, call it C[:len(C)-1] and C[-1] A[i], then C is a LIS ending at i
#        (it must have the same length than B since C[-2] >= B[-2] and if C[-2] > B[-2] then C is longer, 
#        contradiction. So C[-2] = B[-2] and the length must be the same).

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