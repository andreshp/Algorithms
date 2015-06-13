#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, May, 2015
# Hack 101 - April 2015
######################################################################################

T = int(input())
maxN = 3030
dp = [[0]*maxN]*(maxN+1)

for t in range(0,T):
    line = input()
    N = int(line.split()[0])
    D = int(line.split()[1])
    line = input()
    times = [int(x) for x in line.split()]
    times.sort(reverse=True)
    
    problemsC = N-1
    while problemsC >= 0:
        manC = N
        while manC >= 1:
            if manC >= N - problemsC:
                dp[manC][problemsC] = times[problemsC]
            else:
                dp[manC][problemsC] = D + dp[min(N-problemsC, manC*2)][problemsC]
                if manC > 1:
                    C = max(times[problemsC], dp[manC-1][problemsC+1])
                    dp[manC][problemsC] = min(dp[manC][problemsC], C)
            manC -= 1
        problemsC -= 1
    print(dp[1][0])