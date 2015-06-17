////////////////////////////////////////////////////////////////////////////
// Author: Andrés Herrera Poyatos
// Universidad de Granada, June, 2015
// Project Euler
// Problem 35
/////////////////////////////////////////////////////////////////////////////

import scala.collection.mutable.UnrolledBuffer
import scala.collection.immutable.HashSet

object Solution {

    // Compute all the primes number from 1 to 1000000
    def primes() : UnrolledBuffer[Int] = {
        var primes = UnrolledBuffer(2)

        def isPrime(i: Int) :Boolean = {
            for (p <- primes){
                if (p > Math.sqrt(i))
                    return true
                else if (i % p == 0)
                    return false
            }
            true
        }

        for (i <- 3 to 10000){
            if (isPrime(i)){
                primes += i
            }
        }
        primes
    }

    def computeSolutions(): Array[Int] = {
        var pr = primes().toArray
        var computableNumbers = HashSet[Int]()

        def buildSet() : Unit = {
            var x1 = 0; var x2 = 0

            def internalLoop(i: Int) : Unit = {
                for (j <- 0 to pr.size-1) {
                    x2 = pr(j)*pr(j)*pr(j) + x1
                    if (x2 <= 10000000){
                        for (k <- 0 to pr.size-1){
                            computableNumbers += {pr(k)*pr(k) + x2}
                        }
                    }
                    else return
                }                
            }

            for (i <- 0 to pr.size-1){
                x1 = pr(i)*pr(i)*pr(i)*pr(i)
                if (x1 <= 10000000){
                    internalLoop(i)
                }
                else return
            }
        }
 
        buildSet()

        var cN = computableNumbers.toArray.sorted
        var solutions = Array.ofDim[Int](10000001)
        var i = 0; solutions(1) = 0
        for (n <- 2 to solutions.size-1){
            solutions(n) = solutions(n-1)
            while (i < cN.size && cN(i) <= n) { solutions(n) += 1; i +=1}
        }
        solutions
    }

    // Solves T test cases
    def solve(T: Int) : Unit = {
        val solutions = computeSolutions()
        def solveCase(N: Int) {
            println(solutions(N))
        }
        1 to T foreach { _ => solveCase(readInt) }
    }
    
    // Main Program
    def main(args: Array[String]) {
        solve(readInt)
    }
}