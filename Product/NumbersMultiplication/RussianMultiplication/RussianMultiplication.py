######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, February, 2015
# Russian Multiplication Algorithm 
######################################################################################

# The Russian Multiplication Algorihtm is a logarithmic algorithm for number multiplication.

import sys
import time

# Russian Multiplicaction Algorithm:
def russianMultiplication(a,b):
    rest = 0
    while(b > 1):
        if b % 2 == 1:
            rest += a
        a = a << 1
        b = b >> 1

    return a + rest


#---------------- MAIN -----------------#

# See if arguments are correct
if len(sys.argv) != 3:
    print("Sintax: RussianMultiplication.py <number 1> <number 2>")
    sys.exit()

a = int(sys.argv[1]); b = int(sys.argv[2])

# Execute the Russian Multiplicaction Algorithm
start_time = time.time()
sol = russianMultiplication(a, b)

print("--- %f seconds ---" % (time.time() - start_time))
print(a, "*", b, "=", sol)
