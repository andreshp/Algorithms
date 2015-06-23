# Longest Increasing Subsequence Problem

## Explanation

The longest increasing subsequence problem consist of finding a subsequence in a given vector in which the subsequence's elements are in sorted order, lowest to highest, with the highest possible length. 

This subsequence is not necessarily contiguous or unique. For example, the vector [1,2,4,6,3,5] has two solutions, the subsequence 1,2,4,6 and the subsequence 1,2,3,5.

## Solutions

The longest increasing subsequence problem is solvable in time O(*n* log *n*), where *n* denotes the length of the input sequence. I have implemented 3 possible solutions:

1. A dynamic programming approach in O(*n²*).
2. An improvement for the O(*n²*) dynamic approach using segment trees to get O(*n* log *n*).
3. A dynamic programming approach using binary search and obtaining O(*n* log *n*).
