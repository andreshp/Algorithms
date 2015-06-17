////////////////////////////////////////////////////////////////////////////
// Author: Andrés Herrera Poyatos
// Universidad de Granada, June, 2015
// Indeed Prime Challengue
// Problem 4
/////////////////////////////////////////////////////////////////////////////

import scala.math
import scala.collection.mutable.ListBuffer

object Solution {

    def solve() = {
        var tree = Array.ofDim[ListBuffer[(Int, Int)]](10001)
        var shorcuts = Array.ofDim[ListBuffer[(Int, Int)]](10001)
        var N = 0; var E = 0; var K = 0

        def readInfo() = {
            var line = readLine().split(" ").map(x => x.toInt)
            N = line(0); E = line(1); K = line(2)

            for( i <- 0 to N) {
                tree(i) = new ListBuffer[(Int, Int)]
                shorcuts(i) = new ListBuffer[(Int, Int)]
            }
            for( i <- 2 to N) {
                line = readLine().split(" ").map(x => x.toInt)
                tree(line(0)) += {(line(1), line(2))}
                tree(line(1)) += {(line(0), line(2))}
            }
            for( i <- 1 to E) {
                line = readLine().split(" ").map(x => x.toInt)
                shorcuts(line(0)) += {(line(1), line(2))}
                shorcuts(line(1)) += {(line(0), line(2))}
            } 
        }        

        readInfo()
        var D = Array.ofDim[Int](N+1, K+1)
        var root = 1

        // DFS updating the nodes distance to exit from bottom to top.
        // It is implemented in the recursive way.
        def DFS1(j: Int, node: Int, predecessor: Int): Unit = {
            for ((child, distance) <- tree(node)){
                if (child != predecessor){
                    DFS1(j, child, node)
                    D(node)(j) = math.min(D(node)(j), D(child)(j) + distance)                    
                } 
            }        
        }
        
        // DFS updating the nodes distance to exit from top to bottom.
        // It is implemented in the recursive way.
        def DFS2(j: Int, node: Int, predecessor: Int): Unit = {
            for ((child, distance) <- tree(node)){
                if (child != predecessor){
                    D(child)(j) = math.min(D(child)(j), D(node)(j) + distance)
                    DFS2(j, child, node)
                }
            }        
        }
        
        // Initializes leaves to 0
        for (i <- 1 to N){
            if (tree(i).size <= 1) D(i)(0) = 0 else D(i)(0) = 1000000000

        }
    
        // Initializes distances to distances with no shorcuts.
        // A DFS compute the distance just going down.
        // Then a DFS compute the distance using a node parent.
        DFS1(0,root,-1)
        DFS2(0,root,-1)
    
        // For each number of feasible shorcuts:
        // - For each node take the better shorcut.
        // - Update all the distances with the BFS and DFS scheme
        for (j <- 1 to K){
            for (i <- 1 to N){
                D(i)(j) = D(i)(j-1)
                shorcuts(i).foreach { case (neighbour, distance) => D(i)(j) = math.min(D(i)(j), D(neighbour)(j-1) + distance)}
            }
            DFS1(j,root,-1)
            DFS2(j,root,-1)            
        }

        for (i <- 1 to N){
            println(D(i)(K))
        }
    }    

    def main(args: Array[String]) {
        solve()
    }
}
