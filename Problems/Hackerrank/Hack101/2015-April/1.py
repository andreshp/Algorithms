#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, May, 2015
# Hack 101 - April 2015
######################################################################################


N = int(input())

line = input()
speed = [int(x) for x in line.split()]
line = input()
distance = [int(x) for x in line.split()]

first_rat = 0
for i in range(1,N):
    if speed[i]*distance[first_rat] < speed[first_rat]*distance[i]:
        first_rat = i

for i in range(0,N):
    if speed[i]*distance[first_rat] == speed[first_rat]*distance[i]:
        print(i+1)
    