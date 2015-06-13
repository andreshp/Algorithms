#!/usr/bin/python

#######################################################################
# Author: Andrés Herrera Poyatos
# Universidad de Granada, June, 2015
# Indeed Prime Challengue
# Problem 5
########################################################################

# Check the frequency and the type of wave from the input.
# The wave can be a square wave or a sin wave:
# a) Square Wave
# ----|    |----|    |----|    |----|    |----|    
#     |    |    |    |    |    |    |    |    |    
#     |    |    |    |    |    |    |    |    |    
#     |----|    |----|    |----|    |----|    |----
# b) Sin Wave
# .            .            .            .       
#   .       .    .       .    .       .    .     
#    .     .      .     .      .     .      .    
#    .     .      .     .      .     .      .    
#     .   .        .   .        .   .        .   
#       .            .            .            . 

#-------------------- FUNCTIONS ----------------------#

# Get the wave frequency
def frequency(count, length):
    return int((count / length) / 2)

#-------------------- MAIN ----------------------#

N = int(input())
wave_points = []
for i in range(0,N):
    x,y = input().split()
    wave_points.append((float(x), float(y)))

length = wave_points[-1][0]
count = 1
sign = 1

kind = 0
for i in range(0,N):
    if abs(wave_points[i][1] - 1) > 0.01 and abs(wave_points[i][1] + 1) > 0.01:
        kind = 1
    if sign * wave_points[i][1] < 0:
        sign = -sign
        count += 1

if kind == 0:
    print("square-wave")
else:
    print("sine-wave")
print(frequency(count,length))