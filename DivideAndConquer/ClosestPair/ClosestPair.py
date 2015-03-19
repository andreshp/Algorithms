#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Closest Pair of Points Algorithm
#######################################################################

# This program read points of the plane from a file and execute 
# the Closest Pair of Points algorithm on it returning the 2 closest
# points according to the euclidian distance.
# The algorithm is recursive and O(n log n), where n is the number of points.

import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program
import math # For sqrt

#-----------------------------------------------------------------------------------------------

# Euclidean distance between two points of the plane
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

#-----------------------------------------------------------------------------------------------

# Function that get the Closest Pair of Points of the split part of the algorithm.
# 
# array_x : List with all the points sorted by x-coordinates.
# array_y : List with just the points of the target sublist sorted by y-coordinates.
# middle : Index in array_x of the element that split the sublist [begin, end[ (see
#          function call for knowing the sublist).
# min_distance : Minimum Distance got in the previos recursive steps.
# 
# It returns he Closest Pair formed by one point of [begin,middle[
# and another from [middle,end[ in case that it is better than min_distance.
# Else it returns the best pair found (not necessaryly one from each sublist).
# The eficiency is O(len(array_y)).
def closestSplit(array_x, array_y, middle, min_distance):
    x_lower_bound = array_x[middle-1][0] - min_distance
    x_upper_bound = array_x[middle-1][0] + min_distance
    best_distance = float("inf"); candidates = [ ]

    # Get candidates list (elements with element[0] in ]x_lower_bound, x_upper_bound[ )
    for point in array_y:
        if point[0] > x_lower_bound and point[0] < x_upper_bound:
            candidates.append(point)

    # Find in candidates list the possible better pair of points.
    # In case of existing, both points don't differs more than 8 indexes.    
    for i in range(0, len(candidates)):
        for j in range(i+1, min(i+8, len(candidates))):
            new_distance = distance(candidates[i], candidates[j])
            if best_distance > new_distance:
                best_distance = new_distance; best_pair = [ candidates[i], candidates[j] ]

    return best_pair

#-----------------------------------------------------------------------------------------------

# Function that return the closest pair of the of points array [begin, end[.
#
# array_x : List with all the points sorted by x-coordinates.
# array_y : List with just the points of the target sublist sorted by y-coordinates.
# begin, end : delimiters of the target sublist in array_x ([begin, end[).
def closestPairRecursive(array_x, array_y, begin, end):

    # Divide the sublist in two of half size.
    middle = (begin + end) // 2
    Ly = [ ]; Ry = [ ];
    for point in array_y:
        if point[0] >= array_x[middle][0]:
            Ry.append(point)
        else:
            Ly.append(point)

    min_distance = float("inf")

    # If there is more than a point in the left sublist, the closest pair is computed.
    if middle - begin > 1:
        pair = closestPairRecursive(array_x, Ly, begin, middle)
        new_distance = distance(pair[0], pair[1])
        if min_distance > new_distance:
            min_distance = new_distance; best_pair = pair

    # If there is more than a point in the right sublist, the closest pair is computed.
    if end - middle > 1:
        pair = closestPairRecursive(array_x, Ry, middle, end)
        new_distance = distance(pair[0], pair[1])
        if min_distance > new_distance:
            min_distance = new_distance; best_pair = pair

    # If there are at least 3 elements in the subarray, the closest pair between 
    # both partitions is computed, in which case the best pair of all computed
    # is returned. Otherwise both points are return as the best pair found.
    if (end - begin > 2):
        pair = closestSplit(array_x, array_y, middle, min_distance)
        new_distance = distance(pair[0], pair[1])
        if min_distance > new_distance:
            min_distance = new_distance; best_pair = pair
        return best_pair
    elif middle - begin == 1 and end - middle == 1:
        return [ array_x[begin], array_x[begin+1] ]

#-----------------------------------------------------------------------------------------------

# Closest Pair of Points algorithm.
# Returns the closest pair of points in array.
def closestPair(array):
    array.sort(key=lambda element: element[0])
    y = sorted(array, key=lambda element: element[1])
    return closestPairRecursive(array, y, 0, len(array))

#-----------------------------------------------------------------------------------------------

######################## MAIN ##########################

# See if arguments are correct.
if len(sys.argv) < 2:
    print("Error: Needs the array.txt as argument")
    sys.exit()

# Read array.
numbers = open(sys.argv[1], "r")    
array = [ ]
for line in numbers:
    array.append([ int(x) for x in line.split() ])

# Execute closestPair and count the time wasted.
start_time = time.time()
print("Closest Pair Found: ", closestPair(array))
print("--- %f seconds ---" % (time.time() - start_time) )

numbers.close()
