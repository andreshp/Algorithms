#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Date: February, 2015
# Coursera - Stanford - Algorithms: Design and Analysis, Part 1
# Week 6 - Programming Assignment - Part 1 - 2-SUM algorithm
######################################################################################

################################# PROBLEM STATEMENT ##################################
#
# Given an array A of n integers and an integer T, 
# find, if it exits, a pair of numbers a, b in A such as a+b = T
#
##################################### SOLUTION #######################################
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

###################################### CODE #########################################

import sys
import time

def sum2(A, T):
    # Build a hash table (set() in Python)
    hash_table = {a for a in A}
    # Try to find T-a for each a in A
    for a in A:
        if T-a in hash_table:
            return (a,T-a)
    # There is no pair a,b in A such as a+b=T
    raise RuntimeError

######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 3:
    print("Sintax: python3 2sum.py <txt with the arrray> <number to find>")
    sys.exit()

# Read the array and T
T = int(sys.argv[2])
numbers = open(sys.argv[1], "r")
A = [int(line) for line in numbers]

# Execute sum2 and count the time wasted
start_time = time.time()
print(len(A))
try:
    a,b = sum2(A, T)
    print(a, "+", b, "=", T)
except RuntimeError:
    print("Error: There are no numbers a,b in the array that sum", T)
print("--- %f seconds ---" % (time.time() - start_time) )
