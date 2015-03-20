#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, March, 2015
# Scheduling Problem
#######################################################################

# This program solves the Scheduling Problem in O(n log n).
# 
# Statement of the problem: 
# We are given a set of jobs {j_1, ..., j_n} each of those with its importance w_i
# and the time it takes to be completed t_i.
# Given an order in which doing the jobs x = (j_i_1, j_i_2, ..., j_i_n), we define
# C_k = \sum_{r=1}^{k} t_i_r, the time the job has been waiting until finish
# in that order. We have to minimize f(x) = \sum_{k=1}^{n} w_k * C_k.
# 
# Solution:
# We define a ratio r_i = w_i / t_i that is proportional to the importance of the jobs
# and inversely proportional to the times it needs to be completed. We says that
# a job is less than another if it has higher ratio. With this order we sort
# the jobs. This order gives us the optimal solution.
# 
# **Proof**
# Let's x be the order given by the algorithm before x = (j_1, ..., j_n)
# without loss of generality. Let's x' = (j_i_1, j_i_2, ..., j_i_n) be
# another order. We are going to proof that x is as least as good than x'.
# If x != x', exist k such as r_i_k <= r_i_k+1. If we exchange the position
# of jobs j_i_k and j_i_k+1, the cost or improves or remains the same, that is,
# let's x'' be x' with both jobs exchanges. Then, f(x'') = f(x') + w_i_k * t_i_k+1 - w_i_k+1 * t_i_k.
# But w_i_k * t_i_k+1 - w_i_k+1 * t_i_k <= 0 since r_i_k+1 >= r_i_k. Thus 
# f(x') <= f(x''). Let's denote x' = x''. We can repeat this iteration until x'
# is equal to x (at most n(n-1)/2 iterations). Thus f(x) <= f(x').


import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program
import math # For sqrt

#--------------------------------------------------------------------------------#

def schedulingProblemOptimum(jobs):
    # Sort by ratio
    jobs.sort(key=lambda job: -job[0]/job[1])
    
    # Calculate f(x):
    current_time=0
    sum_f = 0
    for j in jobs:
        current_time += j[1]
        sum_f += j[0] * current_time

    return (sum_f, jobs)

#--------------------------------------------------------------------------------#

######################## MAIN ##########################

# See if arguments are correct.
if len(sys.argv) < 2:
    print("Error: Needs the array.txt as argument")
    sys.exit()

# Read the jobs.
# The file has the following structure:
# [number_of_jobs]
# [job_1_weight] [job_1_length]
# [job_2_weight] [job_2_length]
# ...
f_jobs = open(sys.argv[1], "r")    
jobs = [ ]
n_jobs = int(f_jobs.readline())
for line in f_jobs:
    jobs.append([int(x) for x in line.split()])

# Execute the algorithm for the Scheduling Problem and count the time wasted.
start_time = time.time()

print("Minimum Solution: ", schedulingProblemOptimum(jobs)[0])

print("--- %f seconds ---" % (time.time() - start_time) )