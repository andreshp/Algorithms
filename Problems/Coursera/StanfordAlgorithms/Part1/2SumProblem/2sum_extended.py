#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Date: February, 2015
# Coursera - Stanford - Algorithms: Design and Analysis, Part 1
# Week 6 - Programming Assignment - Part 1 - 2-SUM algorithm
######################################################################################

################################# PROBLEM STATEMENT ##################################
#
# Compute the number of target values t in the interval [-10000,10000] (inclusive) 
# such that there are distinct numbers x,y in the input file that satisfy x+y=t
#
# In the asked test n = 1000000
#
###################################### SOLUTION #######################################
#
# First we solve the following problem:
# 
# " Given an array A of n integers and an integer T, find, if it exits, 
# a pair of numbers a, b in A (distinct) such as a+b = T "
#
# A brute-force approach is trying every pair of numbers in A. There are
# n*(n-1)/2 pairs, so the solution would be quadratic.
#
# A second approach could be sorting the array and see if it helps. Now we take
# a number a in A. The question is: ¿is there any number b in A that verifies a+b=T?
# So the problem is reduced to a search problem and we have our array sorted.
# Binary Search for b=T-a!!
# 
# However, we are only searching in a static set, one search per element. 
# For this task hash tables are the best data structure. The algorihtm is the 
# following one:
# 
# 1. Build a hash table with the elements of A.
# 2. For each element a in A, find T-a in the hash table
#       if it exist, return (a, T-a)
# 3. return Not Found
# 
# The efficiency is O(n) in average thanks to hash tables.
#
# Now we can for each number a in A and t integer in [-10000,10000] find if there exits
# b in A such as b+a = t. Consecuently, we would do C * 20000 * n operations, what's less
# than the n^2 approach.


######################################## CODE ########################################

import sys
import time


def solution(A):
    
    limit = 10000
    number_t = 0
    # Build a hash table with the elements of A
    hash_table = {a for a in A}

    for t in range(-limit,limit+1):
        # For each in A, see if there is b in A such as a+b=t with a != b.
        # In that case increase number_t and break
        for a in hash_table:
            if 2*a != t and t-a in hash_table:
                number_t += 1; break

    return number_t

######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 2:
    print("Sintax: python3 2sum_extended.py <txt with the arrray>")
    sys.exit()

# Read the array
numbers = open(sys.argv[1], "r")
A = [int(line) for line in numbers]

# Execute solution and count the time wasted
start_time = time.time()
sol = solution(A)
print("--- %f seconds ---" % (time.time() - start_time) )
print("Solution:", sol)
