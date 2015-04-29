#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, May, 2015
# Project Euler - 19
#######################################################################

import math

T = int(input())

months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

for t in range(0, T):
    line = input()
    Y1 = int(line.split()[0]); M1 = int(line.split()[1]); D1 = int(line.split()[2])
    line = input()
    Y2 = int(line.split()[0]); M2 = int(line.split()[1]); D2 = int(line.split()[2])
    # Get the current week day (0 to 6). Take into account 365 mod 7 = 1
    num_years = Y1-1900
    current_day = (num_years + (num_years-1)//4 - (num_years-1)//100 + (num_years+299)//400) % 7
    # Now we pass the time from year Y1 to year Y2 and count the sundays:
    sundays = 0
    #print(sundays, current_day, M1, Y1)
    if Y1 < Y2:
        for m in range(1,13):
            if current_day == 6 and (m > M1 or (m == M1 and D1 == 1)):
                sundays += 1
            current_day = (current_day + months[m]) % 7
            # In february count the extra day
            if m == 2 and Y1 % 4 == 0 and (Y1 % 100 != 0 or Y1 % 400 == 0):
                current_day = (current_day + 1) % 7
            #print(sundays, current_day, m, Y1)
        for y in range(Y1+1, Y2):
            for m in range(1,13):
                if current_day == 6:
                    sundays += 1
                current_day = (current_day + months[m]) % 7
                # In february count the extra day
                if m == 2 and y % 4 == 0 and (y % 100 != 0 or y % 400 == 0):
                    current_day = (current_day + 1) % 7
                #print(sundays, current_day, m, Y1)
        for m in range(1,M2+1):
            if current_day == 6:
                sundays += 1
            current_day = (current_day + months[m]) % 7
            # In february count the extra day
            if m == 2 and Y2 % 4 == 0 and (Y2 % 100 != 0 or Y2 % 400 == 0):
                current_day = (current_day + 1) % 7
            #print(sundays, current_day, m, Y1)
    else:
        for m in range(1, M2+1):
            if current_day == 6 and (m > M1 or (m == M1 and D1 == 1)):
                sundays += 1
            current_day = (current_day + months[m]) % 7
            # In february count the extra day
            if m == 2 and Y1 % 4 == 0 and (Y1 % 100 != 0 or Y1 % 400 == 0):
                current_day = (current_day + 1) % 7
            #print(sundays, current_day, m, Y1)
    print(sundays)