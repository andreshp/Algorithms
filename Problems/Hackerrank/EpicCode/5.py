#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-20
# Last Modified by:   andreshp
# Last Modified time: 2015-06-22
# File Name: 5.py
###################################################################

from bisect import *

#---------------------------- FUNCTIONS ----------------------------#

def longestIncreasingSubsequenceLength(A):
    S = [A[0]]
    S_index = [0]
    for i in range(1,len(A)):
        if A[i] > S[-1]:
            S.append(A[i])
            S_index.append(i)
        else:
            pos = bisect_left(S,A[i])
            if pos < len(S):
                S[pos] = A[i]
                S_index[pos] = i
    return len(S)

#------------------------------ MAIN -------------------------------#

# Read the pairs with not repeated elements (we do not care about them):
N = int(input())
pairs = set()
for i in range(0,N):
    pairs.add(input())
pairs = list(map(lambda x: tuple(map(int, x.split())), pairs))

# Sort the pairs and get the second element for every pair.
# Now if i < j and B[i] < B[j] then pairs[i] and pairs[j] are good.
# Note that if pair[i][0] = pair[j][0] then B[i] >= B[j].
# Consequently, the longest pair algorithm will not take both pairs i and j
# at the same time.
pairs.sort(key = lambda x: (x[0], -x[1]))
B = list(map(lambda x: x[1], pairs))

print(longestIncreasingSubsequenceLength(B))
