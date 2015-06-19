import scala.collection.mutable.ListBuffer

object Solution {

    def gcd(a: Int, b: Int) : Int = {
        (if (b == 0) a else gcd(b, a % b))
    }

    // Find all the primitive pythagorean triples with 0 < a,b <=M
    // A pythagorean triple is a triple (a,b,c) of integers with
    // a² + b² = c² 
    def primitivePythagoreanTriples(M: Int) : ListBuffer[(Int, Int)] = {
        var pyTriples: ListBuffer[(Int, Int)] = ListBuffer()
        for (m <- 2 to M / 2) {
            for (n <- math.max(1, M - m*m) to math.min(m, M/(2*m))){
                if (gcd(m,n) == 1){
                    var tuple = (m*m - n*n, 2*nm)
                    pyTriples = pyTriples += tuple
                }
            }
        }
        pyTriples
    }

    // Shortest path length to the square for a cuboid
    def shortestPathLengthSquare(a: Int, b: Int, c: Int) : Int = {
        math.min(a*a+(b+c)*(b+c), c*c+(b+a)*(b+a))
    }
    
    def solve(M: Int, pyTriples: ListBuffer[(Int,Int)]) = {
        var count = 0
        println(pyTriples.size)
        for (pair <- pyTriples) {
            if (pair._1 <= M && pair._2 <= M){
                var m = math.min(pair._1, pair._2)
                count += pair._1 * (M / m) * (M / m + 1) / 2                 
            }
        }
        println(count)
    }

    def solve(M: Int) = {
        var count = 0
        for (a <- 1 to M){
            for (b <- a to M){
                for (c <- b to M) {
                    var x = shortestPathLengthSquare(a,b,c)
                    var l = math.sqrt(x).toInt
                    if (l*l == x){
                        count += 1
                    }
                }
            }
        }
        println(count)
    }
    
    // Solves T test cases
    def solveCases(T: Int) = {
        var pyTriples = primitivePythagoreanTriples(400000)
        for (i <- 1 to T) solve(readInt, pyTriples)
    }

    def main(args: Array[String]) {
        solveCases(readInt)
    }
}