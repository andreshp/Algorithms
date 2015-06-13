object Solution {
    // Num of rectangles in a nxm grid
    def numRectangles(n: Int,m: Int) :Int = (n*(n+1)*m*(m+1))/4
    def numRectangles(pair: (Int, Int)) :Int = numRectangles(pair._1,pair._2)
    
    // Check if an approximation is better than other one
    def isBetterApprox(a: Int, n1: Int, m1: Int, n2: Int, m2: Int) :Boolean = {
        Math.abs(numRectangles(n1,m1) - a) < Math.abs(numRectangles(n2,m2) - a) ||
        (Math.abs(numRectangles(n1,m1) - a) == Math.abs(numRectangles(n2,m2) - a) && 
         n1 * m1 > n2 * m2)
    }

    // Best approximation to a for grids with n rows
    def bestNumRectangles(a: Int, n: Int) : Int = {
        var m = 1
        var best_m = 1
        while (numRectangles(n,m) < a){
            m += 1
            if (isBetterApprox(a,n,m,n,best_m)){
                best_m = m
            }
        }
        best_m
    }

    // Solve the problem for the value a
    def solve(a: Int) :Int ={
        var n = 1
        var best_approx :(Int,Int) = (1,1)

        while (n*(n+1)/2 < a){
            var m = bestNumRectangles(a,n)
            if (isBetterApprox(a,n,m,best_approx._1,best_approx._2)){
                best_approx = (n,m)
            }
            n += 1
        }
        best_approx._1 * best_approx._2        
    } 

    // Solve the T queries
    def solveQueries(T: Int) = {
        for (i <- 1 to T){
            println(solve(readInt))
        }
    }        

    def main(args: Array[String]) {
        solveQueries(readInt)
    }
}