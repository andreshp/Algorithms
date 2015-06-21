#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Date: June, 2015
# Hackerrank - Summer Epic Code - Square Array
#######################################################################

# Problem Statement
# https://www.hackerrank.com/contests/epiccode/challenges/square-array

#----------------- SEGMENT TREE IMPLEMENTATION -----------------#

# Segment Tree Node for the range sum problem.
# A node contains the information related with a vector subinterval.
class SegmentTreeNode(object):

    # Init the node. 
    # info = Subinterval information
    def __init__(self):
        # This node is responsible of the [start, end] segment.
        self.start = -1
        self.end = -1
        self.info = None 
        self.hasPending = False
        self.pendingUpdateInfo = [0,0,0]

    # Given the value of an array element,
    # build the information for this leaf.
    def assignLeaf(self, value, index):
        self.info = value
        self.start = index
        self.end = index
    
    def pendingUpdateSum(self):
        delta = (self.end - self.start + 1)
        p = self.pendingUpdateInfo[2] * delta
        p += delta * (delta-1) * self.pendingUpdateInfo[1]
        p += ( ((2*delta-1)*(delta-1)*delta)//6 + ((delta-1)*delta)//2 )* self.pendingUpdateInfo[0]
        return p

    # Merge the information of left and right
    # children to form the parent node information.
    def merge(self, left, right):
        self.start = left.start
        self.end = right.end
        self.info = left.info + right.info
        self.info += left.pendingUpdateSum()
        self.info += right.pendingUpdateSum()

    # Return the information contained in this node.
    def getInfo(self):
        return self.info

    # Check if the node has a pending update.
    def hasPendingUpdate(self):
        return self.hasPending
    
    # Apply the pending update to the node.
    def applyPendingUpdate(self):
        self.info += self.pendingUpdateSum()
        self.pendingUpdateInfo = [0,0,0]
        self.hasPending = False

    # Add a pending update to the node.
    def _addUpdate(self, newUpdate, start):
        delta = (self.start-start)
        self.pendingUpdateInfo[0] += newUpdate[0]
        self.pendingUpdateInfo[1] += newUpdate[1] + newUpdate[0] * delta
        self.pendingUpdateInfo[2] += newUpdate[2] + 2 * delta * newUpdate[1] + newUpdate[0] * delta*(delta+1)
        self.hasPending = True

    # Add a pending update to the node.
    def addUpdate(self, first_number):
        self.pendingUpdateInfo[0] += 1
        self.pendingUpdateInfo[1] += first_number
        self.pendingUpdateInfo[2] += first_number*(first_number+1)
        self.hasPending = True

    # Get the node pending update info.
    def getPendingUpdate(self):
        return self.pendingUpdateInfo

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
    # Check if time can be saved with lazy propagation.
    # st_index : Current Segment Tree Node. It is responsible of [left, right] range.
    def _getInfo(self, st_index, left, right, lo, hi):

        # If current node range is the same that the asked range,
        # resolves its pending updates and return it.
        if left == lo and right == hi:
            if self.nodes[st_index].hasPendingUpdate():
                self.nodes[st_index].applyPendingUpdate()
            return self.nodes[st_index]
 
        mid = (left + right) // 2
        left_child = 2 * st_index
        right_child = left_child + 1

        # Look for the range in the children of the current node
        # if it could be just there.
        if lo > mid:
            result = self._getInfo(right_child, mid+1, right, lo, hi)
        elif hi <= mid:
            result = self._getInfo(left_child, left, mid, lo, hi)
        else:
            # If we keep executing the method then the range is divided between 
            # the left child and the right child of the current node. Let's get 
            # each part of the range and merge it.
            left_result = self._getInfo(left_child, left, mid, lo, mid)
            right_result = self._getInfo(right_child, mid+1, right, mid+1, hi)
            result = self.SegmentTreeNode()
            result.merge(left_result, right_result)

        # If current node has a pending update then we have to update our result
        # accordingly.
        if self.nodes[st_index].hasPendingUpdate():
            result._addUpdate(self.nodes[st_index].getPendingUpdate(), self.nodes[st_index].start)
            result.applyPendingUpdate()

        return result

    # Get the value associated with the range [lo, hi]
    def getInfo(self, lo, hi):
        result = self._getInfo(1, 0, len(self.array)-1, lo, hi)
        return result.getInfo() 

    # Update a range of the segment tree with lazy propagation. 
    # The given value is assigned to the array's components
    # in range [lo,hi]. The segment tree is updated accordingly. 
    # st_index: Current segment tree node.
    # [left, right]: Range which the node st_index is responsible of.
    # [lo, hi]: Array's components to be updated.
    # first_number : Number in wich the sum starts.
    def _updateRange(self, st_index, left, right, lo, hi, first_number):
        if lo == hi:
            self.nodes[st_index].addUpdate(first_number)
            self.nodes[st_index].applyPendingUpdate()
        if left == lo and right == hi:
            self.nodes[st_index].addUpdate(first_number)
        else:
            # Get the middle point and left and right children
            mid = (left + right) // 2
            left_child = 2 * st_index
            right_child = left_child + 1

            # If [lo,hi] nested in [mid+1,right]
            if lo > mid:
                self._updateRange(right_child, mid+1, right, lo, hi, first_number)
            # If [lo,hi] nested in [left,mid]
            elif hi <= mid:
                self._updateRange(left_child, left, mid, lo, hi, first_number)
            else:
                # Divides the update in both parts
                self._updateRange(left_child, left, mid, lo, mid, first_number)
                self._updateRange(right_child, mid+1, right, mid+1, hi, first_number+mid-lo+1)

            # Merge the children info
            self.nodes[st_index].merge(self.nodes[left_child], self.nodes[right_child])

    # Update a range of the segment tree with lazy propagation. 
    # The given value is assigned to the array's components
    # in range [lo,hi]. The segment tree is updated accordingly. 
    # [lo, hi]: Array's components to be updated.
    # value : New value for the array's components in previous range.
    def updateRange(self, lo, hi):
        self._updateRange(1,0,len(self.array)-1,lo,hi,1)

#----------------------- MAIN -----------------------#

N, Q = [int(x) for x in input().split()]
array = [0]*N
st = SegmentTree(array, SegmentTreeNode)

for q in range(0,Q):
    t, x, y = [int(x) for x in input().split()]
    if t == 1:
        st.updateRange(x-1,y-1)
    else:
        print(st.getInfo(x-1,y-1))