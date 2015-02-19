#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Number Exponeniation in Logarithmic Time
######################################################################################

import sys
import time

# Usual Logarithmic Algorithm:
def pow(number, exponent):
    if exponent % 2 == 1:
        b = pow(number, exponent // 2)
        return number*b*b
    else:
        if exponent > 0:
            b = pow(number, exponent // 2)
            return b*b
        else:
            return 1


#---------------- MAIN -----------------#

# See if arguments are correct
if len(sys.argv) != 3:
    print("Sintax: pow.py <number> <exponent>")
    sys.exit()

number = int(sys.argv[1]); exponent = int(sys.argv[2])

# Execute the Exponentiation Algorithm
start_time = time.time()
sol = pow(number, exponent)

print("--- %f seconds ---" % (time.time() - start_time))
print(number, "^", exponent, "=", sol)
