from data import runtests
from collections import deque
from math import inf

class Node:
  def __init__(self, idx, weight):
    self.idx = idx
    self.edges = set() 
    self.weight = weight  
    self.y = 0   
    self.pos = 0 
    self.in_I = False      

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
        v_edges = v.edges
        for u in partition:
            neighbors = u & v_edges
            not_neighbors = u - v_edges

            if not_neighbors:
               new_partition.append(not_neighbors)

            if neighbors:
               new_partition.append(neighbors)

        partition = new_partition

    return order

def weighted_vcover(vs, total_weight):
    for v in vs:
        lower_neighbors_sum = 0
        for neighbor in v.edges:
            if neighbor.pos < v.pos:
                lower_neighbors_sum += neighbor.y
        
        v.y = max(0, v.weight - lower_neighbors_sum)

    independent_set_weight = 0
    for v in reversed(vs):
        if v.y > 0:
            can_add = True
            for u in v.edges:
                if u.in_I:
                    can_add = False
                    break

            if can_add:
                v.in_I = True
                independent_set_weight += v.weight


    return total_weight - independent_set_weight

  

def main(friendships, costs):
    n = len(costs)
    G = [Node(i + 1, costs[i]) for i in range(n)] 

    for edge in friendships:
        u_idx, v_idx = edge[0], edge[1]
        G[u_idx-1].connect_to(G[v_idx-1])
        G[v_idx-1].connect_to(G[u_idx-1])

    vs = LexBfs(G)[::-1]
    for i, v in enumerate(vs):
        v.pos = i

    total_cost = sum(costs)
    return weighted_vcover(vs, total_cost)


runtests(main)
