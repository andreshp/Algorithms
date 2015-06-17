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
            for (j <- 0 until primes.size){
                if (primes(j) > Math.sqrt(i))
                    return true
                else if (i % primes(j) == 0)
                    return false
            }
            true
        }

        for (i <- 3 to 1000000){
            if (isPrime(i)){
                primes += i
            }
        }
        primes
    }

    def rotate(s: String) : String = s.substring(s.size-1,s.size)+s.substring(0,s.size-1)
    def rotationsString(s: String): UnrolledBuffer[String] = rotationsString(s, 0)
    def rotationsString(s: String, iterations: Int): UnrolledBuffer[String] = {
        if (iterations >= s.size){
            return UnrolledBuffer()
        }
        return UnrolledBuffer(rotate(s)).concat(rotationsString(rotate(s), iterations+1))
    }
    
    def rotations(n: Int) : Array[Int] = {
        rotationsString(n.toString).map(_.toInt).toArray
    }
    
    // Compute all the circular primes from 1 to N
    def circularPrimes(N: Int) : UnrolledBuffer[Int] = {
        val pr = primes()
        val set = HashSet() ++ pr

        // Check if the given prime is circular    
        def isCircular(prime: Int) = {
            rotations(prime).forall(x => set.contains(x))
        }
        
        pr.filter(x => x <= N && isCircular(x))        
    }

    def solve(N: Int) = println(circularPrimes(N).sum)
    def main(args: Array[String]) {
        solve(readInt)
    }
}