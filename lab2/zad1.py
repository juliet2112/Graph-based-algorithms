from dimacs import *
from testy import run_all_tests
from collections import deque
from math import inf


def dfs(G,s,t):
    def dfsvisit(G, v):
        visited[v] = True 
        if v == t:
            return parent 
        for u in range (n):
            if not visited[u] and G[v][u] > 0:
                parent[u] = v 
                dfsvisit(G, u)
    visited = [False for _ in range(len(G))] 
    parent = [None for _ in range (len(G))] 
    n = len(G) 
    dfsvisit(G, s)   
    return parent           


def bfs(G, s, t):
    n = len(G)
    Q = deque()
    visited = [False for _ in range(len(G))]
    parent = [None for _ in range(len(G))]

    visited[s] = True
    Q.append(s)

    while Q:
        v = Q.popleft()
        for u in range (n):
            if not visited[u] and G[v][u] > 0:
                visited[u] = True
                parent[u] = v
                Q.append(u)

    return parent

def residual_net(V,L):
    G = [[0 for _ in range (V)] for _ in range (V)]
    for v,u,w in L:
        G[v-1][u-1] = w
    return G

def Ford_Fulkerson(V,L):
    R = residual_net(V,L)
    max_flow = 0
    s = 0
    t = V-1

    while True:
        parent = bfs(R,s,t)
        if parent[t] != None:
            flow = R[parent[t]][t]
            v = parent[t]
            while v != s:
                flow = min(flow, R[parent[v]][v])
                v = parent[v]

            v = t
            while v != s:
                R[parent[v]][v] -= flow
                R[v][parent[v]] += flow
                v = parent[v]

            max_flow+= flow
        else:
            break
        

    return max_flow
        
#V, L = loadDirectedWeightedGraph("lab2/graphs-lab2/flow/clique5")
#print(Ford_Fulkerson(V,L))

if __name__ == "__main__":
    run_all_tests(Ford_Fulkerson)