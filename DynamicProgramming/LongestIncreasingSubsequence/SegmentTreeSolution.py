#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-22
# Last Modified by:   andreshp
# Last Modified time: 2015-06-23
# File Name: SegmentTreeSolution.py
###################################################################

import math
import sys
import time

#----------------------------- EXPLANATION ------------------------------#

# Let's denote LIS[i] the length of the longest increasing sequence
# ending at component i. 
# 
# We want to find the value LIS[i] for all i. It is trivial that the longest
# increasing sequence length is the maximum of LIS[i] for all i.
# 
# We have:
# 1. LIS[0] = 1 
# 2. LIS[i] = max(LIS[j] + 1 for al j in J) if J not empty else 1
#   where J = {j: i > j, A[i] > A[j]}
# 
# This allows us to compute LIS[i] for all i easily in O(n²) and, thus,
# the longest increasing subsequence length.
#
# There is a solution O(n log n) for the longest increasing subsequence problem
# using the dynamic approach explained before that is just a consequence of segment trees. 
# Let's try to develop it.
# 
# We are given a vector A for which we want to compute the LIS. Now A is sorted to
# obtain B, the permutation of indexes that sorts it.
#   
# 3. If we want the longest strictly increasing subsequence then we need that if i < j and
#   A[i] = A[j] then B[i] > B[j] to avoid taking equals elements in the subsequence.
# 4. If we want the longest non-decreasing subsequence then we need that if i < j and 
#   A[i] = A[j] then B[i] < B[j]. This will allow us adding j to a subsequence ending at i,
#   obtaining the LIS (non-decreasing).
# 
# Let's build a segment tree initialized with LIS. Consequently, the i-th leaf will contain
# the length of the LIS ending at i when we finnish the algorithm. At first those value will be 0
# (we haven't computed them yet). The segment tree will allow to get the maximum of 
# those values in a subinterval.
# 
# For each element in B we can compute the LIS ending in that element. In order to do that, 
# first find the element in [0,B[i]-1] with longest LIS.
# That element has been procesed before B[i] (else its node value is 0) so it is smaller
# than B[i] (or equal if we did 4). We can get the LIS for B[i] appendig it to the
# LIS of the obtained element . Then the length of the LIS for B[i] is updated.
# This process is just 2:
# 
# LIS[B[i]] = max(LIS[j] + 1 for al j in J) where J = {j: B[i] > j, A[i] > A[j]}.
# 
# This sofisticated scheme leads us for a easy proof since it is equivalent to the dynamic
# solution operations. The difference is that at each step we get the LIS for the smallest
# element not processed yet. We can do this since bigger elements do not affect to the LIS
# of smaller ones (as 2 says). The proof is by induction: 
# - For B[0] its trivial that we have computed the LIS. 
# - Let's suppose it is true for B[j] with j < i < len(B). Then:
#   LIS[B[i]] = max(LIS[j] + 1 for al j in J) where J = {j: B[i] > j, A[i] > A[j]}.
#   But J = {B[j] with B[j] < B[i] for all j < i} and:
#   LIS[B[i]] = max(LIS[B[j]] for j < i, B[j] < b[i]) = SegmentTree.getMaximumLIS([0, B[i]-1])
#   (if j >= i then LIS[j] = 0 and won't affect to the segment tree search).
#   This is exactly what we do.



#------------------------------ FUNCTIONS -------------------------------#

def longestIncreasingSubsequenceLength(A):
    st = SegmentTree([0]*len(A),SegmentTreeNodeMax)
    B = list(map(lambda x : -x[1], sorted([(A[i],-i) for i in range(0,len(A))])))
    for i in range(0,len(B)):
        st.update(B[i],st.getInfo(0,B[i])[0]+1)
    return st.getInfo(0,len(A)-1)[0]

def longestIncreasingSubsequenceIndexes(A):
    st = SegmentTree([0]*len(A),SegmentTreeNodeMax)
    B = list(map(lambda x : -x[1], sorted([(A[i],-i) for i in range(0,len(A))])))
    P = [-1]*len(A)
    for i in range(0,len(A)):
        length, P[B[i]] = st.getInfo(0, B[i])
        st.update(B[i],length+1)

    LIS = []; i = st.getInfo(0,len(A)-1)[1]
    while  i != -1:
        print(i)
        LIS.append(i)
        i = P[i]
    return LIS[::-1]

#----------------- SEGMENT TREE IMPLEMENTATION -----------------#

# Node of the Segment Tree.
# It represent the statictics associated with a 
# subinterval or range of the array.
# 
# It allows setting and getting the statictics and
# merge its children statistics to form a parent node.
class SegmentTreeNodeMax(object):
    
    # Init the node. 
    # Its attribute value is initialized to Node.
    def __init__(self):
        self.info = None
        self.index = None

    # Given the value of an input array element,
    # build aggregate statistics for this leaf node.
    def assignLeaf(self, value, index):
        self.info = value
        self.index = index
    
    # Merge the aggregate statistics of left and right
    # children to form the aggregate statistics of
    # their parent node.
    def merge(self, left, right):
        if left.info >= right.info:
            self.info = left.info
            self.index = left.index
        else:
            self.info = right.info
            self.index = right.index

    # Return the value of required aggregate statistic
    # associated with this node.
    def getInfo(self):
        return self.info, (self.index if self.info != 0 else -1)

class SegmentTree(object):

    # Build a segment tree from the given array.
    # array: Array from which the segment tree is built.
    # st_index: current segment tree node index.
    # lo and hi : Range of input array subinterval that this node is responsible of.
    def _buildTree(self, array, st_index, lo, hi):
        if lo == hi: 
            # The node is a leaf responsible of V[lo,lo]
            self.nodes[st_index].assignLeaf(array[lo], lo)
        else: 
            # The node is not a leaf.
            # Both children are built and merged afterwards for this node.
            left = 2 * st_index
            right = left + 1
            mid = (lo + hi) // 2
            self._buildTree(array, left, lo, mid)
            self._buildTree(array, right, mid + 1, hi)
            self.nodes[st_index].merge(self.nodes[left], self.nodes[right])

    # Get the segment tree size for a input of size N.
    # It compute the smallest 2 to the power of m greater than N.
    def _getSegmentTreeSize(N):
        size = 1
        while size < N:
            size <<= 1
        return size << 1

    # Initializes a Segment Tree.
    # array : Array from which the segment tree is built.
    # Node : Class that will be used as a segment tree node. 
    #   It obtains the desired information from the array.
    def __init__(self, array, Node):
        self.SegmentTreeNode =  Node
        # Segment tree size (number of nodes)
        self.size = SegmentTree._getSegmentTreeSize(len(array))
        # Heap with the nodes
        self.nodes = [self.SegmentTreeNode() for i in range(0,self.size)]
        self.array = array
        # The tree is built
        self._buildTree(array, 1, 0, len(array)-1)

    # Get recursively a SegmentTreeNode with the information associated with the range [lo, hi].
    # st_index : Current Segment Tree Node. It is responsible of [left, right] range.
    def _getInfo(self, st_index, left, right, lo, hi):
        # Check if the range is the current node in the tree.
        # In that case return it.
        if left == lo and right == hi:
            return self.nodes[st_index]

        # Look for the range in the children of the current node
        # if it could be just there.
        mid = (left + right) // 2
        if lo > mid:
            return self._getInfo(2*st_index+1, mid+1, right, lo, hi)
        if hi <= mid:
            return self._getInfo(2*st_index, left, mid, lo, hi)

        # If we keep executing the method then the range is divided between 
        # the left child and the right child of the current node. Let's get 
        # each part of the range and merge it.           
        left_result = self._getInfo(2*st_index, left, mid, lo, mid)
        right_result = self._getInfo(2*st_index+1, mid+1, right, mid+1, hi)
        result = self.SegmentTreeNode()
        result.merge(left_result, right_result)
        return result

    # Get the value associated with the range [lo, hi]
    def getInfo(self, lo, hi):
        result = self._getInfo(1, 0, len(self.array)-1, lo, hi)
        return result.getInfo() 

    # Update the segment tree. 
    # The given value is assigned to the array's component at index place.
    # The segment tree is updated accordingly in a recursive way. 
    # st_index : Current segment tree node index.
    # lo and hi : The current range is [lo, hi]
    # index : Array's component to be updated.
    # value : New value for the array's component to update.
    def _update(self, st_index, lo, hi, index, value):
        # If current node is a leaf we have ended the search and assign 
        # the value to the leaf.
        if lo == hi:
            self.nodes[st_index].assignLeaf(value, lo)

        # If the current node is not a leaf, the search is continued recursively
        # and the current node information is updated afterwards.
        else:
            left = 2 * st_index
            right = left + 1
            mid = (lo + hi) // 2

            # Continue the search by the correct path
            if index <= mid:
                self._update(left, lo, mid, index, value)
            else:
                self._update(right, mid+1, hi, index, value)
            # Update current node information
            self.nodes[st_index].merge(self.nodes[left], self.nodes[right])

    # Update the segment tree. 
    # The given value is assigned to the array's
    # component at index place. The segment tree is updated accordingly. 
    # index : Array's component to be updated.
    # value : New value for the array's component to update.
    def update(self, index, value):
        self._update(1, 0, len(self.array)-1, index, value)
        self.array[index] = value

#------------------------------ MAIN -------------------------------#

V = [1,2,4,6,3,5]
print("Longest incresing subsequence of ", V)
print(list(map(lambda x: V[x], longestIncreasingSubsequenceIndexes(V))))
print("Length:", longestIncreasingSubsequenceLength(V))