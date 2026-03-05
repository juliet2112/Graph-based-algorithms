from math import inf
from lab3.dimacs import *
from heapq import heappop, heappush
from test import run_all_tests

def create_graph(V,L):
    G = [[] for _ in range (V)]
    for (x,y,c) in L:
        G[x-1].append((y-1,c))
        G[y-1].append((x-1,c))

    return G

def dijkstra(G,s):
    n = len(G)
    d = [inf for _ in range (n)]
    PQ = []
    d[s] = inf
    heappush(PQ,(-d[s],s))

    while PQ:
        mini, v = heappop(PQ)
        mini = -mini
        if mini < d[v]: continue

        for u,w in G[v]:
            if d[u] < min(d[v],w) or d[u] == inf:
                d[u] = min(d[v],w)
                heappush(PQ,(-d[u],u))

    return d[1]

def lab0(V,L):
    G = create_graph(V,L)
    return dijkstra(G,0)
    

if __name__ == "__main__":
    run_all_tests(lab0)