import networkx as nx
from dimacs import *
from networkx.algorithms.planarity import check_planarity

def create_graph(V,L):
    G = nx.Graph()
    for i in range (V):
        G.add_node(i)

    for v,u in L:
        G.add_edge(u-1,v-1)
    return G

def main(V,L):
    G = create_graph(V,L)
    return check_planarity(G)

V, L = loadDirectedWeightedGraph("lab5/graphs-lab2/flow/clique5")
print(main(V,L))