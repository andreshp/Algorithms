import scala.collection.immutable.HashSet

object Solution {

    // Compute all the primes number from 1 to 1000000
    def primes() : Array[Int] = {
        var primes = Array(2)

        def isPrime(i: Int) :Boolean = {
            for (j <- 0 until primes.size){
                if (primes(j) > Math.sqrt(i))
                    return true
                else if (i % primes(j) == 0)
                    return false
            }
            true
        }

        for (i <- 3 to 999999){
            if (isPrime(i)){
                primes = primes :+ i
            }
        }
        primes
    }

    // Solve the task for n and k
    def solve(n: Int, k: Int) = {
        val pr = primes().filter(_ > 1000)
        val set = HashSet() ++ pr

        // Check progressions starting at prime        
        def checkProgressions(prime: Int) = {
            var perms_ = prime.toString.permutations.toArray.map(_.toInt).sorted.filter(x => x > prime && set.contains(x))
            var perms = HashSet() ++ perms_
            for (element <- perms_){
                var solution = prime.toString + element.toString
                val difference = element - prime
                if (perms.contains(element + difference)){
                    solution = solution + (element+difference).toString
                    if (k == 4 && perms.contains(element+2*difference)){
                        println(solution + (element+2*difference).toString)
                    }
                    else if (k == 3) {
                        println(solution)
                    }
                }
            }
        }

        var i = 0
        while(i < pr.size && pr(i) < n){
            checkProgressions(pr(i)); i+=1
        }
    }
    
    def main(args: Array[String]) {
        val Array(n,k) = readLine.split(" ").map(_.toInt)
        solve(n,k)
    }
}