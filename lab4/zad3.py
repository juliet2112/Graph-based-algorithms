from dimacs import *
from testy import run_all_tests
from collections import deque
from math import inf

class Node:
  def __init__(self, idx):
    self.idx = idx
    self.edges = set()             

  def connect_to(self, v):
    self.edges.add(v)

def LexBfs(G):
    partition = [set(G)]
    order = []

    while partition:
        last = partition[-1]
        v = last.pop()

        if not last:
            partition.pop()

        order.append(v)

        new_partition = []
        for u in partition:
            neighbors = u & v.edges
            not_neighbors = u - v.edges

            if not_neighbors:
               new_partition.append(not_neighbors)

            if neighbors:
               new_partition.append(neighbors)

        partition = new_partition

    return order

def color(vs):
    n = len(vs)
    node_colors = [0 for _ in range (n)]
    colors = {i for i in range (1,n+1)}

    for v in vs:
        used = {node_colors[u.idx] for u in v.edges if node_colors[u.idx] > 0}
        c = min(colors - used)
        node_colors[v.idx] = c

    return max(node_colors)
  

def main(V,L):
    G = [Node(i) for i in range(0, V)] 

    for (u, v, _) in L:
        G[u-1].connect_to(G[v-1])
        G[v-1].connect_to(G[u-1])

    vs = LexBfs(G)
    return color(vs)

#V, L = loadWeightedGraph("lab4/graphs-lab4//chordal/AT")
#print(main(V,L))

if __name__ == "__main__":
    run_all_tests(main, "graphs-lab4/coloring")