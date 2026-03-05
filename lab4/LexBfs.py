from dimacs import *
from collections import deque
from math import inf

class Node:
  def __init__(self, idx):
    self.idx = idx
    self.edges = set()            

  def connect_to(self, v):
    self.edges |= {v}
    v.edges |= {self}

def checkLexBFS(G, vs):
  n = len(G)
  pi = [None] * n
  for i, v in enumerate(vs):
    pi[v.idx] = i

  for i in range(n-1):
    for j in range(i+1, n-1):
      Ni = vs[i].edges
      Nj = vs[j].edges

      verts = [pi[v.idx] for v in Nj - Ni if pi[v.idx] < i]
      if verts:
        viable = [pi[v.idx] for v in Ni - Nj]
        if not viable or min(verts) <= min(viable):
          return False
  return True


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
  

def main(V,L):
    G = [Node(i) for i in range(0, V)] 

    for (u, v, _) in L:
        G[u-1].connect_to(G[v-1])
        G[v-1].connect_to(G[u-1])

    vs = LexBfs(G)
    return checkLexBFS(G,vs)


V, L = loadWeightedGraph("graphs-lab4\chordal\K33")
print(main(V,L))