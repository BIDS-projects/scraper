import networkx as nx   # graph analysis rather than graph visualization
import json

# TODO: Look into graph analysis algorithms and see anything seems useful: https://networkx.github.io/documentation/latest/reference/algorithms.html

with open('example.json') as in_file:
    data = json.load(in_file)

g = nx.DiGraph(data) # makes directed graph
# TODO (wait until the correct json file): Analysis - PageRank 

