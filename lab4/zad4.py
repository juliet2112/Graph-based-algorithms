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

def vcover(vs):
    n = len(vs)
    I = set() #zbiór niezależny
    vs_reversed = reversed(vs)

    for v in vs_reversed:
        if I & v.edges == set():
            I.add(v)

    return n - len(I)

  

def main(V,L):
    G = [Node(i) for i in range(0, V)] 

    for (u, v, _) in L:
        G[u-1].connect_to(G[v-1])
        G[v-1].connect_to(G[u-1])

    vs = LexBfs(G)
    return vcover(vs)

#V, L = loadWeightedGraph("lab4/graphs-lab4//chordal/AT")
#print(main(V,L))

if __name__ == "__main__":
    run_all_tests(main, "graphs-lab4/vcover")