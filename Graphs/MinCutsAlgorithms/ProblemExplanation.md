Minimum Cut Problem
===================

Given a graph G = (V,E), a cut is a partition of V in two not empy sets which elements are joined by at least one edge. The minimum cut is the cut with the smallest number of edges between elements of both set.

The [Contraction Algorithm](http://en.wikipedia.org/wiki/Karger%27s_algorithm) developped by David Karger in 1993. It is a randomized algorithm that find in one iteration the minimum cut with probability 2 / ( |V| * (|V|-1) ). This iteration is implemented in O(|V|^2) (with Hash tables). Doing |V|^2 log |V| iterations the minimum cut is found with probabilty greater than 1 - 1/|V|.