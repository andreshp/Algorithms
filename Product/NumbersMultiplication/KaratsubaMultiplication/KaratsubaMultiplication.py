######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, February, 2015
# Karatsuba Multiplication Algorithm 
######################################################################################

#   Multiplication Algorihtm is a logarithmic algorithm for number multiplication.

import sys
import time

# Karatsuba Russian Multiplicaction Algorithm:
def karatsubaMultiplication(a,b):
    if (a < 10) or (b < 10)
        return a*b
    
#    m = max(size_base10(num1), size_base10(num2))
#    m2 = m/2
    
    low1 
    z0 = karatsubaMultiplication(low1, low2)
    z1 = karatsubaMultiplication(low1+high1, low2+high2)
    z2 = karatsubaMultiplication(high1, high2)
    return 


#---------------- MAIN -----------------#

# See if arguments are correct
if len(sys.argv) != 3:
    print("Sintax: KaratsubaMultiplication.py <number 1> <number 2>")
    sys.exit()

a = int(sys.argv[1]); b = int(sys.argv[2])

# Execute the Russian Multiplicaction Algorithm
start_time = time.time()
sol = karatsubaMultiplication(a, b)

print("--- %f seconds ---" % (time.time() - start_time))
print(a, "*", b, "=", sol)
