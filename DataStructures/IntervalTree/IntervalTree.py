#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Date: June, 2015
# Interval Tree Implementation
#######################################################################

#----------------- INTERVAL TREE IMPLEMENTATION -----------------#

class Interval:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
    def getBegin(self):
        return self.begin
    def getEnd(self):
        return self.end
 
class Node:
    def __init__(self, x_center, s_center, left_node, right_node):
        self.x_center = x_center
        self.s_center = sort_by_begin(s_center)
        self.left_node = left_node
        self.right_node = right_node
 
def sort_by_begin(intervals):
    return sorted(intervals, key=lambda x: x.getBegin())

# Interval Tree class
class IntervalTree:

    # Build an interval tree
    def __init__(self, intervals):
        self.top_node = self.divide_intervals(intervals)
 
    def divide_intervals(self, intervals):
 
        if not intervals:
            return None
 
        x_center = self.center(intervals)
 
        s_center = []
        s_left = []
        s_right = []
 
        for k in intervals:
            if k.getEnd() < x_center:
                s_left.append(k)
            elif k.getBegin() > x_center:
                s_right.append(k)
            else:
                s_center.append(k)
 
        return Node(x_center, s_center, self.divide_intervals(s_left), self.divide_intervals(s_right))
        
 
    def center(self, intervals):
        fs = sort_by_begin(intervals)
        length = len(fs)
 
        return fs[int(length/2)].getBegin()
 
    def search(self, begin, end=None):
        if end:
            result = []
 
            for j in xrange(begin, end+1):
                for k in self.search(j):
                    result.append(k)
                result = list(set(result))
            return sort_by_begin(result)
        else:
            return self._search(self.top_node, begin, [])

    def _search(self, node, point, result):
        
        for k in node.s_center:
            if k.getBegin() <= point <= k.getEnd():
                result.append(k)
        if point < node.x_center and node.left_node:
            for k in self._search(node.left_node, point, []):
                result.append(k)
        if point > node.x_center and node.right_node:
            for k in self._search(node.right_node, point, []):
                result.append(k)
 
        return list(set(result))
 