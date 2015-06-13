object Solution {
    def compute(S: Array[Int], i: Int) :Int = {
        var x = 0
        var sign = -1
        for (k <- 1 to i) {
            if (k*(3*k-1)/2 <= i){
                sign = -sign
                x += sign * S(i - k*(3*k-1)/2)
                if (k*(3*k+1)/2 <= i){
                    x += sign * S(i - k*(3*k+1)/2)
                }
            }
            else{ return x }
        }
        return x
    }
    def solve(MAX_N: Int) : Array[Int] = {
        var S = Array.ofDim[Int](MAX_N+1)

        S(0) = 1; S(1) = 1; S(2) = 2
        for (i <- 3 to MAX_N) {
            S(i) = compute(S,i)
        }    
        return S
    }

    def main(args: Array[String]) {
        var MAX_N = 60000
        var sol = solve(MAX_N)

        var T = readInt
        for (i <- 1 to T) { println(sol(readInt)) }
    }
}