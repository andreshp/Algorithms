# 2 Sum Problem

## Initial Problem

It is solved in `2sum.py`.

### Statement
Given an array A of n integers and an integer T, find, if it exits, a pair of numbers a, b in A such as a+b = T.

### Solution

A brute-force approach is trying every pair of numbers in A. There are n*(n-1)/2 pairs, so the solution would be quadratic.

A second approach could be sorting the array and see if it helps. Now we take a number a in A. The question is: ¿is there any number b in A that verifies a+b=T? The query is reduced to a search problem and we have our array sorted. Binary Search for b=T-a!!

However, we are only searching in a static set, one search per element. 
For this task hash tables are the best data structure. The algorihtm proposed is the following one:

1. Build a hash table with the elements of A.
2. For each element a in A, find T-a in the hash table. If it exist, return (a, T-a)
3. return Not Found

The efficiency is O(n) in average thanks to hash tables.

## Extended Problem

It is solved in `2sum_extended.py` and `2sum_extended_2.py`. One different approach is given in each code. For the array given with the problem the second approach is a way better since it uses the structure of the data to be fast. However, there are pathological data where it would fail and is better the O(n * limit) efficiency of the first approach.

### Statement

Compute the number of target values t in the interval \[-limit,limit\] (inclusive) such that there are distinct numbers x, y in the input file that satisfy x+y=t.

In the asked test n = 1000000 and limit = 10000.

### Solution

The first approach uses the initial problem, reducing the extended one to 2*limit+1 searchs. The second one try a brute-force algorithm (try every pair of elements in the array) but sorts it and uses Binary Search to find, given a number a, the elements of the array whose sum with a is in \[-limit,limit\].
