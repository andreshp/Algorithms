# Topological Sort

An algorithm to find a topological sort of a directed graph in O(|V| + |E|).

##### Definition 
Given a directed graph (*V*,*E*), let's suppose it is **acyclic** (it has no cycles, that is, there is not a path from one node to itself). A **topological sort** of the graph is a list of the nodes, *f* : *V* -> {1,...,|*V*|}, verifying that if *v*,*u* in *V* and (*v*,*u*) in *E* then *f*(*v*) < *f*(*u*).

##### Utility
The topological sort is really helpful to do a list of jobs to do if you have some order restrictions. These restrictions conform the edges and the jobs the nodes of the graph. The topological sort gives you an order for the jobs that does not violates the initial restrictions.

##### Algorihtm
The algorithm is based on DFS. It mantains a visited nodes list and and a variable *n* = |*V*|.

The main loop iterates all the nodes of the graph. In each iteration, if the node is not visited DFS is executed on it. In the DFS execution, when it finishes in a node *v* it does f(v) = n and decrement n.

That's all the algorithm! Let's **proof** that it works. Given a pair of nodes *v*, *u* in *V*. Let's supose that (*v*,*u*) in *E* and let's see that *f*(*v*) < *f*(*u*). There are two cases:

- DFS arrives first at *v*. Then, it wil go to *u* afterwards and will not finishes the *v* branch until *u* hasn't done so. Consecuently, *f*(*v*) < *f*(*u*).
- DFS arrives first at *u*. Since the graph is acyclic, it will not arrives at *v* in the *u* branch. Then, *u* will be assigned *n* before DFS arrives to *v*. Thus, *f*(*v*) < *f*(*u*).
