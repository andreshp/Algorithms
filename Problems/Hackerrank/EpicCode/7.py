#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-21
# Last Modified by:   andreshp
# Last Modified time: 2015-06-21
# File Name: 7.py
###################################################################

import math
import sys
import time

#----------------- SEGMENT TREE IMPLEMENTATION -----------------#

# Template for a Segment Tree Node.
# A node contains the information related with a vector subinterval.
class SegmentTreeNodeSum(object):
    
    # Init the node. 
    # info = Subinterval information
    def __init__(self):
        self.info = None

    # Given the value of an array element,
    # build the information for this leaf.
    def assignLeaf(self, value):
        self.info = value            
    
    # Merge the information of left and right
    # children to form the parent node information.
    def merge(self, left, right):
        self.info = left.info + right.info

    # Return the information contained in this node.
    def getInfo(self):
        return self.info

class SegmentTree(object):

    # Build a segment tree from the given array.
    # array: Array from which the segment tree is built.
    # st_index: current segment tree node index.
    # lo and hi : Range of input array subinterval that this node is responsible of.
    def _buildTree(self, array, st_index, lo, hi):
        if lo == hi: 
            # The node is a leaf responsible of V[lo,lo]
            self.nodes[st_index].assignLeaf(array[lo])
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

    # Update a range of the segment tree in O(hi-lo). 
    # The given value is assigned to the array's components
    # in range [lo,hi]. The segment tree is updated accordingly. 
    # st_index: Current segment tree node.
    # [left, right]: Range which the node st_index is responsible of.
    # [lo, hi]: Array's components to be updated.
    # value : New value for the array's components in previous range.
    def _updateRange(self, st_index, left, right, lo, hi, value):
        if lo == hi:
            self.nodes[st_index].info += value
        else:
            # Get the middle point and left and right children
            mid = (left + right) // 2
            left_child = 2 * st_index
            right_child = left_child + 1

            # If [lo,hi] nested in [mid+1,right]
            if lo > mid:
                self._updateRange(right_child, mid+1, right, lo, hi, value)
            # If [lo,hi] nested in [left,mid]
            elif hi <= mid:
                self._updateRange(left_child, left, mid, lo, hi, value)
            else:
                # Divides the update in both parts
                self._updateRange(left_child, left, mid, lo, mid, value)
                self._updateRange(right_child, mid+1, right, mid+1, hi, value)
            # Merge the children info
            self.nodes[st_index].merge(self.nodes[left_child], self.nodes[right_child])


    # Update a range of the segment tree in O(hi-lo). 
    # The given value is assigned to the array's components
    # in range [lo,hi]. The segment tree is updated accordingly. 
    # [lo, hi]: Array's components to be updated.
    # value : New value for the array's components in previous range.
    def updateRange(self, lo, hi, value):
        self._updateRange(1,0,len(self.array)-1,lo,hi,value)


#------------------------------ MAIN -------------------------------#

# Read constains and sets
N, S, M = [int(x) for x in input().split()]
Ssets = [[]]*(S+1)
for i in range(1,S+1):
    Ssets[i] = [int(x) for x in input().split()][1:]

# Build array and segment tree
A = [0]*(N+1)
st = SegmentTree(A, SegmentTreeNodeSum)

# Do queries
for m in range(0, M):
    # Read query data
    op = [int(x) for x in input().split()]

    # Query 1
    if op[0] == 1:
        a = op[1]; t = op[2]
        for index in Ssets[a]:
            A[index] = (A[index] + t) % 1000000009 
    # Query 2
    elif op[0] == 2:
        sol = 0; a = op[1]
        for index in Ssets[a]:
            sol = (sol + A[index]) % 1000000009
            sol = (sol + st.getInfo(A[index], A[index])) % 1000000009
        print(sol)
    # Query 3
    elif op[0] == 3:
        st.updateRange(op[1],op[2],op[3])
    # Query 4
    else:
        sol = 0; l = op[1]; r = op[2]
        for i in range(l,r+1):
            sol = (sol + A[i]) % 1000000009
        sol = (sol + st.getInfo(l, r)) % 1000000009
        print(sol)
