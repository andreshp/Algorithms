////////////////////////////////////////////////////////////////////////////
// Author: Andrés Herrera Poyatos
// Universidad de Granada, June, 2015
// Project Euler
// Problem 49
/////////////////////////////////////////////////////////////////////////////

import scala.collection.mutable.ListBuffer
import scala.collection.immutable.HashSet
import scala.collection.mutable.HashMap

object Solution {

    // Compute all the primes number from 1 to 1000000
    def primes() : ListBuffer[Int] = {
        var primes = ListBuffer(2)

        def isPrime(i: Int) :Boolean = {
            for (j <- 0 until primes.size){
                if (primes(j) > Math.sqrt(i))
                    return true
                else if (i % primes(j) == 0)
                    return false
            }
            true
        }

        for (i <- 3 to 999999 by 2){
            if (isPrime(i)){
                primes += i
            }
        }
        primes
    }

    // Solve the task for n and k
    def solve(n: Int, k: Int) : Unit = {
        val pr = primes().filter(_ > 1000)
        val set = HashSet() ++ pr
        var prClasses = HashMap[(Int, Int), ListBuffer[Int]]()

        pr.foreach {
            x => {
                var digits = x.toString.sorted.toInt
                var num_digits = x.toString.size
                if (prClasses.contains((digits, num_digits))) prClasses((digits, num_digits)) += x else prClasses((digits, num_digits)) = ListBuffer(x)
            }
        }
        // Check progressions starting at prime        
        def checkProgressions(prime: Int) = {
            var digits = prime.toString.sorted.toInt
            var num_digits = prime.toString.size
            if (prClasses((digits, num_digits)).size >= k){
                var perms_ = prClasses((digits, num_digits)).filter(_ > prime).sorted
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
        }

        pr.foreach{x => if (x < n) checkProgressions(x) else return}
    }
    
    def main(args: Array[String]) {
        val Array(n,k) = readLine.split(" ").map(_.toInt)
        solve(n,k)
    }
}