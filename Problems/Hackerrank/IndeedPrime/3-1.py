#!/usr/bin/python

#######################################################################
# Author: Andrés Herrera Poyatos
# Universidad de Granada, June, 2015
# Indeed Prime Challengue
# Problem 3 - 1
########################################################################

#----------------- SEGMENT TREE IMPLEMENTATION -----------------#

# Node of the Segment Tree.
# It represent the statictics associated with a 
# subinterval or range of the array.
# 
# It allows setting and getting the statictics and
# merge its children statistics to form a parent node.
class SegmentTreeNodeMin(object):
    # Init the node. 
    # Its attribute value is initialized to Node.
    def __init__(self):
        self.index = None
        self.value = None
        self.ones_places = None
        self.most_to_left = None
        self.most_to_right = None

    # Given the value of an input array element,
    # build aggregate statistics for this leaf node.
    def assignLeaf(self, index, value):
        self.index = index
        self.value = value
        if value != 1:
            self.ones_places = (-2, -2)
        else:
            self.ones_places = (index, index)
        self.most_to_left = self.ones_places
        self.most_to_right = self.ones_places
        
    
    # Merge the aggregate statistics of left and right
    # children to form the aggregate statistics of
    # their parent node.
    def merge(self, left, right):

        # Set value and index
        self.value = min(left.value, right.value)
        if self.value == left.value:
            self.index = left.index
        else:
            self.index = right.index

        # Set ones_places, most_to_left and most_to_right
        interval3 = (-2,-2)

        # If there is an interval with elements form left and rigth it is built.
        if left.most_to_right[1] + 1 == right.most_to_left[0]:
            interval3 = (left.most_to_right[0], right.most_to_left[1])

        self.ones_places = (-2,-2); self.most_to_left = self.ones_places; self.most_to_right = self.ones_places

        if left.ones_places[0] != -2:
            self.ones_places = left.ones_places
            if interval3[0] != -2:
                    if interval3[1] - interval3[0] > self.ones_places[1] - self.ones_places[0]:
                        self.ones_places = interval3

        if right.ones_places[0] != -2:            
            if self.ones_places[0] == -2 or right.ones_places[1] - right.ones_places[0] > self.ones_places[1] - self.ones_places[0]:
                self.ones_places = right.ones_places
                if interval3[0] != -2:
                    if interval3[1] - interval3[0] >= self.ones_places[1] - self.ones_places[0]:
                        self.ones_places = interval3

        if interval3[0] != -2 and interval3[0] == left.most_to_left[0]:
            self.most_to_left = interval3
        else:
            self.most_to_left = left.most_to_left
        if interval3[0] != -2 and interval3[1] == right.most_to_right[1]:
            self.most_to_right = interval3
        else:
            self.most_to_right = right.most_to_right

    # Return the value of required aggregate statistic
    # associated with this node.
    def getValue(self):
        return self.index, self.value, self.ones_places

class SegmentTree(object):

    # Initializes a Segment Tree.
    # array : Array from which the segment tree is built.
    # SegmentTreeNode : Class that will be used as a segment 
    #     tree node. It gets the desired statictics from the
    #     array.
    def __init__(self, array, SegmentTreeNode):
        self.SegmentTreeNode =  SegmentTreeNode
        self.size = SegmentTree.getSegmentTreeSize(len(array))
        self.nodes = [self.SegmentTreeNode() for i in range(0,self.size+1)]
        self.array = array
        self._buildTree(array, 1, 0, len(array)-1)

    # Build a segment tree from the given array.
    # array: Array from which the segment tree is built.
    # st_index: current segment tree node
    # lo and hi : Range of input array that this node is responsible of.
    def _buildTree(self, array, st_index, lo, hi):
        if lo == hi:
            self.nodes[st_index].assignLeaf(lo, array[lo])
        else:
            left = 2 * st_index
            right = left + 1
            mid = (lo + hi) // 2
            self._buildTree(array, left, lo, mid)
            self._buildTree(array, right, mid + 1, hi)
            self.nodes[st_index].merge(self.nodes[left], self.nodes[right])

    # Get the segment tree size for a input of size N    
    def getSegmentTreeSize(N):
        size = 1
        while size < N:
            size <<= 1
        return size << 1

    # Get the value associated with the range [lo, hi]
    def getValue(self, lo, hi):
        result = self._getValue(1, 0, len(self.array)-1, lo, hi)
        return result.getValue()
 
    # Get recursively a SegmentTreeNode with the value associated with
    # the range [lo, hi].
    # stIndex : Current Segment Tree Node. It is responsible of [left, right] range.
    def _getValue(self, stIndex, left, right, lo, hi):
        # Check if the range is the current node in the tree.
        # In that case return it.
        if left == lo and right == hi:
            return self.nodes[stIndex]

        # Look for the range in the children of the current node
        # if it could be just there.
        mid = (left + right) // 2
        if lo > mid:
            return self._getValue(2*stIndex+1, mid+1, right, lo, hi)
        if hi <= mid:
            return self._getValue(2*stIndex, left, mid, lo, hi)

        # If we keep executing the method then the range is divided between the left
        # child and the right child of the current node. Let's get each part of the range
        # and merge it.           
        leftResult = self._getValue(2*stIndex, left, mid, lo, mid);
        rightResult = self._getValue(2*stIndex+1, mid+1, right, mid+1, hi);
        result = self.SegmentTreeNode()
        result.merge(leftResult, rightResult)
        return result

    # Update the segment tree. 
    # The given value is assigned to the array's
    # component at index place. The segment tree is updated accordingly. 
    # index : Array's component to be updated.
    # value : New value for the array's component to update.
    def update(self, index, value):
        self._update(1, 0, len(self.array)-1, index, value)
        self.array[index] = value

    # Update the segment tree. 
    # The given value is assigned to the array's component at index place. T
    # he segment tree is updated accordingly in a recursive way. 
    # stIndex : Current segment tree node's index.
    # lo and hi : The current range is [lo, hi]
    # index : Array's componen to be updated.
    # value : New value for the array's component to update.
    def _update(self, stIndex, lo, hi, index, value):
        # If current node is a leaf we have ended the search and assign 
        # the value to the leaf.
        if lo == hi:
            self.nodes[stIndex].assignLeaf(lo, value)
        # If the current node is not a leaf, the search is continued recursively
        # and the current node statictics are updated afterwards.
        else:
            left = 2 * stIndex
            right = left + 1
            mid = (lo + hi) // 2

            # Continue the search by the right path
            if index <= mid:
                self._update(left, lo, mid, index, value)
            else:
                self._update(right, mid+1, hi, index, value)
            # Update current node statictics
            self.nodes[stIndex].merge(self.nodes[left], self.nodes[right])

#---------------------- QUERIES ------------------------#

# Solves query 1. 
# Print the minimum product subinterval.
def solveQuery1(st, u, v):
    # Gets the minimum value of array[u,v] and its position.
    index, min_value, places = st.getValue(u,v)

    # Print the sol according to the minimum value 
    if min_value > 1:
        print(min_value, index+1, index+1)
    elif min_value == 0:
        print(0, u+1, v+1)
    else:
        print(1, places[0]+1, places[1]+1)

# Solves querie 2.
# Updates array[u] to v in both segment trees.
def solveQuery2(st, u, v):
    st.update(u,v)

#---------------------- MAIN ------------------------#

N, Q = [int(x) for x in input().split()]
array = [int(x) for x in input().split()]
st = SegmentTree(array, SegmentTreeNodeMin)

for i in range(0, Q):
    q, u, v = [int(x) for x in input().split()]
    if q == 1:
        solveQuery1(st, u-1, v-1)
    else:
        solveQuery2(st, u-1, v)
