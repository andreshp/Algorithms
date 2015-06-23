#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Date: June, 2015
# Segment Tree Implementation
#######################################################################

#----------------- SEGMENT TREE IMPLEMENTATION -----------------#

# Template for a Segment Tree Node.
# A node contains the information related with a vector subinterval.
class SegmentTreeNode(object):
    
    # Init the node. 
    # info = Subinterval information
    def __init__(self):
        self.info = None

    # Given the value of an array element,
    # build the information for this leaf.
    def assignLeaf(self, value):
        pass# Insert the code to build the leaf information
            
    # Merge the information of left and right
    # children to form the parent node information.
    def merge(self, left, right):
        pass# Insert the merge code

    # Return the information contained in this node.
    def getInfo(self):
        return self.info

    # Check if the info contained is the same that the given info
    def isSameInfo(self, info):
        pass# Insert comparation code

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
        self.info = None

    # Given the value of an input array element,
    # build aggregate statistics for this leaf node.
    def assignLeaf(self, value):
        self.info = value
    
    # Merge the aggregate statistics of left and right
    # children to form the aggregate statistics of
    # their parent node.
    def merge(self, left, right):
        self.info = min(left.info, right.info)

    # Return the value of required aggregate statistic
    # associated with this node.
    def getInfo(self):
        return self.info

    # Check if the info contained is the same that the given info
    def isSameInfo(self, info):
        return self.info == info

class SegmentTree(object):

    # Build a segment tree from the given array.
    # array: Array from which the segment tree is built.
    # st_index: current segment tree node index.
    # lo and hi : Range of input array subinterval that this node is responsible of.
    def _buildTree(self, array, st_index, lo, hi):
        self.nodes[st_index] = self.SegmentTreeNode()
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
        self.nodes = [None for i in range(0,self.size)]
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
            self.nodes[st_index].assignLeaf(value)

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

    # Update the segment tree. 
    # The given value is assigned to the array's
    # component at index place. The segment tree is updated accordingly. 
    # index : Array's component to be updated.
    # value : New value for the array's component to update.
    def update2(self, index, value):
        st_index = self.size // 2 + index # Leaf index
        # Update leaf and array
        self.array[index] = value
        self.nodes[st_index].assignLeaf(value) 
        # Update leaf ancestors
        st_index = st_index // 2
        while st_index > 0:
            # Get current info and update it with a merge from the children
            current_info = self.nodes[st_index]
            self.nodes[st_index].merge(self.nodes[2*st_index], self.nodes[2*st_index+1])
            # If the info has not changed then the algorithm ends
            if self.nodes[st_index].isSameInfo(current_info):
                break
            # Go to node's parent
            st_index = st_index // 2

#----------------------- EXAMPLE MAIN -----------------------#

array = [1,2,3,4,5,7,8]
st = SegmentTree(array, SegmentTreeNodeMin)
print(st.getInfo(0,3))
print(array)
print(list(map(lambda x: x.getInfo(), st.nodes)))
st.update(3,-28)
print(list(map(lambda x: x.getInfo(), st.nodes)))
print(array)
print(st.getInfo(0,6))
