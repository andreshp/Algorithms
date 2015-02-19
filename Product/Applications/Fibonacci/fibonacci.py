#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, F, 2015
# Fibonacci Numbers in Logarithmic Time
######################################################################################

import sys
import time

# Product of a 2x2 Matrix
def product2x2(A, B):
    C = [ [ A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1] ], [ A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1] ] ] 
    return C

# Usual Logarithmic Algorithm for 2x2 matrix exponentation:
def exp(A, exponent):
    if exponent % 2 == 0:
        B = exp(A, exponent // 2)
        return product2x2(B,B)
    else:
        if exponent > 1:
            B = exp(A, exponent // 2)
            return product2x2(A, product2x2(B,B))
        else:
            return A

# Calculate the n-th number of Fibonacci in Logarithmic Time.
# It uses the following idea:
# 
#   (1  1)  (F_{n+2} F_{n+1})  =  (F_{n+3} F_{n+2})
#   (1  0)  (F_{n+1}  F_{n} )  =  (F_{n+2} F_{n+1})
#
# Since:
# 
#   (F_{2}  F_{1})  = (1  1)
#   (F_{1}  F_{0})  = (1  0)
#
# By induction:
# 
#   (1  1) ^ k+1  =  (F_{n+2} F_{n+1})
#   (1  0)        =  (F_{n+1}  F_{n} )
def fibonacci(n):
    if n > 0:
        A = [[1, 1], [1,0]]
        A = exp(A, n-1)
        return A[0][0]
    else:
        return 0


#---------------- MAIN -----------------#

# See if arguments are correct
if len(sys.argv) != 2:
    print("Sintax: fibonacci.py <number>")
    sys.exit()

n = int(sys.argv[1])

# Execute the Fibonacci Algorithm
start_time = time.time()
sol = fibonacci(n)
print("--- %f seconds ---" % (time.time() - start_time))
print("Number", n, "of Finonacci:", sol)
