from dimacs import *
from testy import run_all_tests
from collections import deque
from math import inf

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
        G[u-1][v-1] = w
    return G

def Ford_Fulkerson(V,L,s,t):
    R = residual_net(V,L)
    cnt = 0

    while True:
        parent = bfs(R,s,t)
        if parent[t] != None:
            cnt+=1
            flow = 1
            v = t
            while v != s:
                R[parent[v]][v] -= flow
                R[v][parent[v]] += flow
                v = parent[v]
        else:
            break
        
    return cnt

def connectivity(V,L):
    result = inf
    for s in range(V-1):
        for t in range(s+1, V):
            result = min(Ford_Fulkerson(V,L,s,t), result)

    return result

V, L = loadDirectedWeightedGraph("lab3/graphs-lab3/geo100_2a")
print(connectivity(V,L))

#if __name__ == "__main__":
#    run_all_tests(connectivity)