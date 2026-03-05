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

def isPEO(vs):
    n = len(vs)
    pos = [None]*n
    for i in range(n):
       pos[vs[i].idx] = i
    
    for i in range (n):
        v = vs[i]
        RN_v = set() #zbiór sąsiadów wcześniej w vs niż v 
        parent_v = None
        for u in v.edges:
            if pos[u.idx] < pos[v.idx]:
                RN_v.add(u)
                if parent_v == None or pos[parent_v.idx] < pos[u.idx]:
                    parent_v = u

        if not RN_v:
            continue

        RN_parent = set()
        for u in parent_v.edges:
            if pos[u.idx] < pos[parent_v.idx]:
                RN_parent.add(u)

        #sprawdzamy czy RN_v - {parent_v} zawiera się w RN_parent
        if not(RN_v - {parent_v} <= RN_parent):
            return False
        
    return True
  

def main(V,L):
    G = [Node(i) for i in range(0, V)] 

    for (u, v, _) in L:
        G[u-1].connect_to(G[v-1])
        G[v-1].connect_to(G[u-1])

    vs = LexBfs(G)
    return isPEO(vs)

#V, L = loadWeightedGraph("lab4/graphs-lab4//chordal/AT")
#print(main(V,L))

if __name__ == "__main__":
    run_all_tests(main, "graphs-lab4/chordal")