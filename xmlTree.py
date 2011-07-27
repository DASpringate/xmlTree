#!/usr/bin/python2
"""
Python2 Tools for building and visualising trees of xml file structures
D A Springate 2011
requires: networkx (http://networkx.lanl.gov/index.html), 
matplotlib (http://matplotlib.sourceforge.net/).
usage: xmlTree.py xmlFile tree-depth(0 for no pruning) [graphic file to save to] [nolabels]
e.g. xmlTree.py article.xml 3 testy.png nolabels.
"""

import networkx as nx
from networkx import graphviz_layout
import matplotlib.pyplot as plt
from xml.etree.ElementTree import ElementTree
import sys

class xmlTreeBuilder:
    """
    parses an xml file and gives lists of nodes and edges suitable for 
    inputting into a graphing library e.g. networkx.
    """
    def __init__(self, xmlFile):
        self.xmlTree = self.parseXml(xmlFile)
        nodes = []
        edges = []
        counter = 0
        for i in self.xmlTree.iter():
            nodes.append(i)
            counter += 1
            
        for node in nodes:
            kids = list(node) 
            if len(kids) > 0:
                edges.extend([(node, kids[i]) for i in range(len(kids))])

        self.nodeNames = [str(i) + ": " + nodes[i].tag for i in range(len(nodes))]
        self.edgeNames = [(self.nodeNames[nodes.index(edges[i][0])], 
                                self.nodeNames[nodes.index(edges[i][1])]) 
                                for i in range(len(edges))]
    def parseXml(self, xmlFile):
        """parses xml file using elementTree."""
        tree = ElementTree()
        return(tree.parse(xmlFile))

class xmlTreeViewer:
    """
    takes lists of nodes and edges, constructs a graph and then outputs 
    using matplotlib or saves to file.
    """
    def __init__(self, Tree, treeDepth = 0):
        self.nodeNames = Tree.nodeNames
        self.edgeNames = Tree.edgeNames
        if treeDepth == 0:
            self.xmlGraph = self.basicTree(self.nodeNames, self.edgeNames)
        elif treeDepth > 0:
            self.xmlGraph = self.egoTree(self.nodeNames, self.edgeNames, 
                                                                treeDepth)
        else:
            sys.stderr.write("That level of nesting is impossible!\n")
            sys.exit(1)
            
    def basicTree(self, nodeNames, edgeNames):
        """Constructs an unpruned tree."""
        gr = nx.balanced_tree(1,2)
        gr.add_nodes_from(nodeNames)
        gr.add_edges_from(edgeNames)
        return (gr)
        
    def egoTree(self, nodeNames, edgeNames, treeDepth):
        """Constructs a tree pruned to treeDepth from the root."""
        gr = nx.balanced_tree(1,2)
        gr.add_nodes_from(nodeNames)
        gr.add_edges_from(edgeNames)
        return(nx.ego_graph(gr, nodeNames[0], treeDepth))
        
    def drawTree(self, xmlGraph, savePlot = False, Size = (8,8), 
                                                    Labels = True):
        """Visualises tree in matplotlib or as a graphics file."""
        pos = nx.graphviz_layout(xmlGraph,prog='twopi',args='')
        plt.figure(figsize = Size)
        nx.draw(xmlGraph,pos,node_size=50,alpha=0.5,node_color="blue", 
                                                    with_labels = Labels)
        nx.draw_networkx_nodes(xmlGraph,pos,nodelist=[self.nodeNames[0]], 
                                                node_size=200,node_color='r')
        if savePlot:
            plt.savefig(savePlot)
            sys.stderr.write("xml tree written to " + savePlot + " ...\n")
            sys.exit(0)
        else:
            plt.show()

if __name__ == "__main__":
    if "help" in " ".join(sys.argv[1:]) or len(sys.argv) < 2:
        print """XML tree viewer DA Springate 2011
usage: xmlTree.py xmlFile tree-depth(0 for no pruning) [graphic file to save to] [nolabels]"""
        sys.exit(0)
    else:
        xmlFile = sys.argv[1]
        treeDepth = int(sys.argv[2])
    if len(sys.argv) > 3 and sys.argv[3] not in ["nolabels"]:
        savePlot = sys.argv[3]
    else:
        savePlot = False
    if "nolabels" in " ".join(sys.argv[1:]):
        Labels = False
    else:
        Labels = True

    theTree = xmlTreeBuilder(xmlFile)
    View = xmlTreeViewer(theTree, treeDepth)
    Viz = View.drawTree(View.xmlGraph, savePlot = savePlot, Labels = Labels)

