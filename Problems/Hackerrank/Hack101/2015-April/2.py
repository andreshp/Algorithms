#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, May, 2015
# Hack 101 - April 2015
######################################################################################


######################## MAIN ##########################

N = int(input())

line = input()
array = [int(x) for x in line.split()]

sol = 0
for i in range(0,N-2):
    greater = 0
    for j in range(i+1,N):
        if array[j] > array[i]:
            greater += 1
        elif array[j] < array[i]:
            sol += greater
print(sol)