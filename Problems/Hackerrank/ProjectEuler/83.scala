object Solution {
    def main(args: Array[String]) {
        var N = readLine().toInt
        var matrix = Array.ofDim[Long](N,N)
        var sol = Array.ofDim[Long](N,N)

        // Read matrix
        for(i <- 0 to N-1 ){ matrix(i) = readLine().split(" ")map(_.toLong) }        

        // Initializes solution matrix
        for {
            i <- 0 to N-1
            j <- 0 to N-1
        } sol(i)(j) = Long.MAX_LONG   
        sol(0)(0) = matrix(0)(0)
                
        // We loop 10 times, each time be get a better answer
        for (k <- 0 to 9) {
            for (j <- 0 to N-1) {
                for (i <- 0 to N-1) {
                    
                    if (j > 0)          sol(i)(j) = math.min(sol(i)(j), sol(i)(j-1) + matrix(i)(j))
                    if (j < N - 1)   sol(i)(j) = math.min(sol(i)(j), sol(i)(j+1) + matrix(i)(j))
                    if (i > 0)          sol(i)(j) = math.min(sol(i)(j), sol(i-1)(j) + matrix(i)(j))
                    if (i < N - 1)   sol(i)(j) = math.min(sol(i)(j), sol(i+1)(j) + matrix(i)(j))
                }
            }
        }
        
        println(sol(N-1)(N-1))
    }
}