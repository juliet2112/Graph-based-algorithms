from dimacs import *
from testy import run_all_tests
from heapq import heappop,heappush
from math import inf
from collections import deque

class Node:
  def __init__(self):
    self.edges = {}  
    self.merged = set()
    self.active = True

  def addEdge( self, to_v, weight):
    self.edges[to_v] = self.edges.get(to_v,0) + weight  
                                                    
  def delEdge( self, to ):
    self.edges.pop(to, None)

def create_graph(V,L):
    G = [ Node() for i in range(V) ]

    for (x,y,c) in L:
        G[x-1].addEdge(y-1,c)
        G[y-1].addEdge(x-1,c) 
    return G


def mergeVertices( G, x, y ):                        
    for v in G[y].edges:
        if v == x:
           continue 
        if v not in G[x].edges:
            new_w = G[y].edges[v]
            G[x].addEdge(v,new_w)
        else:
           new_w = G[x].edges[v] + G[y].edges[v]
           G[x].edges[v] = new_w

        G[v].addEdge(x,new_w)

    G[y].active = False 
    G[y].edges = {}

    G[x].merged.add(y)

def minimumCutPhase(G,n):
    for i in range(len(G)):
       if G[i].active:
          a = i
          break
          
    S = {a}
    order = [a]
    Q = []
    d = [0 for _ in range(len(G))]

    for i in G[a].edges:
        if i not in S:
            d[i] += G[a].edges[i]
            heappush(Q,(-d[i],i))

    while len(S) < n:
        w,v = heappop(Q)

        if v in S:
           continue

        for i in G[v].edges:
            if G[i].active:
                d[i] += G[v].edges[i]
                heappush(Q,(-d[i],i))

        if len(S) == n-1:
            result = -w
        S.add(v)
        order.append(v)

    s = order[-1]
    t = order[-2]


    mergeVertices(G,s,t)
    return result



def connectivity(V,L):
    G = create_graph(V,L)
    result = inf
    for i in range (V-1):
       result = min(result, minimumCutPhase(G,len(G)-i))

    return result


#V, L = loadDirectedWeightedGraph("lab3/graphs-lab3/clique20")
#print(connectivity(V,L))

if __name__ == "__main__":
    run_all_tests(connectivity)