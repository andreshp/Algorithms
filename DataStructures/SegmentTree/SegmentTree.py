#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Date: February, 2015
# Segment Tree Implementation
#######################################################################

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
        self.value = None

    # Given the value of an input array element,
    # build aggregate statistics for this leaf node.
    def assignLeaf(self, value):
        self.value = value
        
    
    # Merge the aggregate statistics of left and right
    # children to form the aggregate statistics of
    # their parent node.
    def merge(self, left, right):
        self.value = min(left.value, right.value)

    # Return the value of required aggregate statistic
    # associated with this node.
    def getValue(self):
        return self.value

class SegmentTree(object):

    # Build a segment tree from the given array.
    # array: Array from which the segment tree is built.
    # st_index: current segment tree node
    # lo and hi : Range of input array that this node is responsible of.
    def _buildTree(self, array, st_index, lo, hi):
        if lo == hi:
            self.nodes[st_index].assignLeaf(array[lo])
        else:
            left = 2 * st_index
            right = left + 1
            mid = (lo + hi) // 2
            self._buildTree(array, left, lo, mid)
            self._buildTree(array, right, mid + 1, hi)
            self.nodes[st_index].merge(self.nodes[left], self.nodes[right])

    # Get the segment tree size for a input of size N    
    def _getSegmentTreeSize(N):
        size = 1
        while size < N:
            size <<= 1
        return size << 1

    # Initializes a Segment Tree.
    # array : Array from which the segment tree is built.
    # SegmentTreeNode : Class that will be used as a segment 
    #     tree node. It gets the desired statictics from the
    #     array.
    def __init__(self, array, SegmentTreeNode):
        self.SegmentTreeNode =  SegmentTreeNode
        self.size = SegmentTree._getSegmentTreeSize(len(array))
        self.nodes = [self.SegmentTreeNode() for i in range(0,self.size+1)]
        self.array = array
        self._buildTree(array, 1, 0, len(array)-1)

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
            self.nodes[stIndex].assignLeaf(value)
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

#----------------------- EXAMPLE MAIN -----------------------#

array = [1,2,3,4,5,6,7,8]
st = SegmentTree(array, SegmentTreeNodeMin)
print(st.getValue(0,3))
st.update(3,-28)
print(st.getValue(0,7))
