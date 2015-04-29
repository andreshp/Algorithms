#########################################
# Author: Andrés Herrera Poyatos
#########################################

# Solution
def bestPath(N, numbers):
    for i in range(1,N):
        start = (N-i-1)*(N-i)//2 
        for j in range(0,N-i):
            numbers[start+j] += max(numbers[start+j+N-i], numbers[start+j+N-i+1])
    return numbers[0]

# MAIN
T = int(input())
for i in range(0,T):
    N = int(input())
    numbers = []
    size = N*(N+1) // 2
    for i in range(0,N):
        line = input()
        for x in line.split():
            numbers.append(int(x))
    sol = 0
    sol = bestPath(N, numbers)
    print(sol)