#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, May, 2015
# Hack 101 - April 2015
######################################################################################

def intersection(int1, int2):
    if int2[0] < int1[1]:
        return (max(int1[0], int2[0]), min(int1[0], int2[0]))
    else return None

######################## MAIN ##########################

T = int(input())

for t in range(0,T):
    line = input()
    n = int(line.split()[0])
    m = int(line.split()[1])
    subase = []
    for i in range(0,m):
        line = input()
        L = int(line.split()[0])
        R = int(line.split()[1])
        subase.append((L,R))
    subase.sort()
    for i in range(0,m):
        if 

