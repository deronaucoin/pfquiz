#Slightly modified from: https://github.com/alexland/d3-data-adapter/blob/master/d3-graph-data-adapter.py

import os
import random as RND
import numpy as NP
import itertools
import networkx as NX
import json as JSON


#---------------------- convert adj matrix to JSON ---------------------#

def adjmatrix_tojson(adj_matrix):
    """
        returns valid JSON-encoded graph
        pass in: graph represented as adjacency matrix (python nested list)
        
    """
    G = {"links": [], "nodes": []}
    n = len(adj_matrix[0])
    keys_links = ("source", "target", "value")
    keys_nodes = {"group", "name"}
    for i, row in enumerate(adj_matrix):
        G["nodes"].append( dict(zip(keys_nodes, 
            (1, "n{0}".format(i)))) )
        for j, itm in enumerate(row):
            G["links"].append( dict(zip(keys_links, (i, j, itm))) )
    return G


#---------------------- write json-encoded graph to file ---------------------#

def write_jsongraph(graphfilename, json_graph_obj):
    """
        returns: nothing writes JSON-encoded graph to file
        whose name and location are passed in
        pass in: 'fname', file path and name of data file created
        upon execution of this fn 
    """
    with open(graphfilename, mode="w") as f:
        JSON.dump(json_graph_obj, f, indent=2)



datastring = open("matrix.txt",'r').read()
numarray = eval(datastring)
arr = NP.array(numarray)
arr= arr*10000
write_jsongraph("graph.json", adjmatrix_tojson(arr)) 
    
