#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, February, 2015
# Hackerrank Problem - Fibonacci GCD
######################################################################################

# The problem statement can be found in: https://www.hackerrank.com/contests/infinitum9/challenges/fibonacci-gcd

mod = 1000000007

# Greater Common Divisor of a pair
def gcd(a, b):
    while a != 0 :
        c = a; a = b % a; b = c
    return b

# Greatest Common Divisor of a list.
# It applies the definition and calculates the gcd of a pair each time.
def gcd_list(numbers):
    cur_gcd = numbers[0]
    for i in range(1, len(numbers)):
        cur_gcd = gcd(numbers[i], cur_gcd)
    return cur_gcd

# Product of a 2x2 Matrix
def product2x2(A, B):
    C = [ [ (A[0][0]*B[0][0]+A[0][1]*B[1][0]) % mod, (A[0][0]*B[0][1]+A[0][1]*B[1][1]) % mod ], [ (A[1][0]*B[0][0]+A[1][1]*B[1][0]) % mod, (A[1][0]*B[0][1]+A[1][1]*B[1][1]) % mod] ] 
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
    if n > 1:
        A = [[1, 1], [1,0]]
        A = exp(A, n-1)
        return A[0][0]
    else:
        return 0 if n == 0 else 1

#---------------- MAIN -----------------#

N = int(input())

a = []

for i in range(0,N):
    a.append(int(input()))

index = gcd_list(a)
sol = fibonacci(index)

print(sol)
