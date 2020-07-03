# PageRank
# Language: Python
# Input: CSV (network)
# Output: NOA (central nodes and centrality values)
# Tested with: PluMA 1.1, Python 3.6
# Dependencies: numpy==1.16.0, networkx==2.2

PluMA plugin to compute Page Rank centrality (Page, 1999).  The plugin accepts 
as input a network in the form of a CSV file, where rows and columns each represent
nodes and entry (i, j) contains the weight of the edge from i to j.

The plugin produces as output a NOde Attribute (NOA) file, which can be imported
into Cytoscape.  Centrality then becomes a Cytoscape attribute for every node,
and can be used for further downstream analysis and visualization.
