#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Simple Implementation of the Euclides Algorithm to calculate the 
# greatest common divisor of a list of integers. It also calculates
# the minimum common multiple
######################################################################################

import sys
import time

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

def mcm_list(numbers):
    sol = numbers[0] // gcd_list(numbers)
    for i in range(1, len(numbers)):
        sol *= numbers[i]
    return sol


#---------------- MAIN -----------------#

# See if arguments are correct
if len(sys.argv) < 3:
    print("Sintax: gcd.py <options> <numbers...>")
    print("  - Option -m: Calculates the mcm instead.")
    sys.exit()

# Execute the Euclides Algorithm:
start_time = time.time()
if sys.argv[1] == "-m":
    sol = mcm_list([ int(sys.argv[i]) for i in range(2,len(sys.argv))] )
else:
    sol = gcd_list([ int(sys.argv[i]) for i in range(1,len(sys.argv))] )

print("--- %f seconds ---" % (time.time() - start_time))
print("MCM:" if sys.argv[1] == "-m" else "GCD:", sol)
