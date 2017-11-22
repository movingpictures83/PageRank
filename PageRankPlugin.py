import numpy
import math
import random
import sys
import networkx
############################################################
# Dijkstra's Algorithm
# Uses Modified Classes from the Python Data Structures Module
# One modification: heap is now max-heap
# Since this modifies distances IN PLACE, have to be careful
# Must prioritize the queues based on absolute value
# But must use the actual edge weights when computing distance
# Also: "start" is now an integer i
# I have to build a different graph ON THE FLY
from pythonds.graphs import PriorityQueue, Graph, Vertex
numdiff = 0
import itertools

ALPHA=0.5

def buildNetworkXGraph(myfile):
 if (myfile[len(myfile)-3:] == "csv"):
  print "Reading CSV File: ", myfile
  G=networkx.Graph()
  ###########################################################
  # Read the file
  # Put results in filestuff
  filestuff = open(myfile, 'r')
  firstline = filestuff.readline()
  bacteria = firstline.split(',')
  bacteria.remove('\"\"')
  n = len(bacteria)
  inf = float("infinity")
  ###########################################################
  for i in range(n):
    bac = bacteria[i].strip()
    bac = bac[1:len(bac)-1]
    G.add_node(bac)
  eps = random.random()*0.0001
  ###########################################################
  # Populate the adjacency matrix, ADJ
  i = 0
  for line in filestuff:
   contents = line.split(',')
   values = numpy.zeros([n])
   for j in range(n):
      value = float(contents[j+1])
      # Anything other than pagerank, we can read as we go
      if (i != j and value != 0):
           values[j] = value
   # Pagerank cannot handle a weighted sum of zero
   # for all edges of a node.  Adding eps if that's the case
   if (numpy.sum(values) == 0):
         values[0] += eps
   for j in range(n):
           bac1 = bacteria[i].strip()
           bac2 = bacteria[j].strip()
           bac1 = bac1[1:len(bac1)-1]
           bac2 = bac2[1:len(bac2)-1]
           G.add_edge(bac1, bac2, weight=values[j])
   i = i + 1
  ############################################################
 else:
  print "Reading GML File..."
  G = networkx.read_gml(myfile)
  bacteria = G.nodes()
  print "Done."

 return bacteria, G

############################################################
####################################################################################################

class PageRankPlugin:
   def input(self, file):
      self.bacteria, self.graph = buildNetworkXGraph(file)
   def run(self):
      self.U = networkx.pagerank(self.graph, alpha=ALPHA, max_iter=100)
   def output(self, file):
     UG = []
     for key in self.U:
        UG.append((self.U[key], key)) 
     UG.sort()
     UG.reverse()
     # Formatted for Cytoscape
     outfile = open(file, 'w')
     outfile.write("Name\tCentrality\tRank\n")
     #data = [['Name', 'Centrality']]
     centvals = numpy.zeros([len(UG)])
     for i in range(len(UG)):
       print (UG[i][1], UG[i][0])
       bac = UG[i][1]
       if (bac[0] == '\"'):
          bac = bac[1:len(bac)-1]
       if (UG[i][0] != UG[len(UG)-1][0]):
         outfile.write(bac+"\t"+str(abs(UG[i][0]))+"\t"+str(len(UG)-i)+"\n")
       else:
         outfile.write(bac+"\t"+str(abs(UG[i][0]))+"\t"+"0\n")
       #if (i > 2):
       centvals[i] = abs(UG[i][0])

     print "Wrote file: ", file
     print "Min centrality: ", numpy.min(centvals)
     print "Max centrality: ", numpy.max(centvals)
     mymean = numpy.mean(centvals)
     stddev = numpy.std(centvals)
     print "Standard Deviation: ", stddev
     print "Two STDs back: ", mymean - 2*stddev
     print "One STD back: ", mymean - stddev
     print "One STD forward: ", mymean + stddev
     print "Two STDs forward: ", mymean + 2*stddev


