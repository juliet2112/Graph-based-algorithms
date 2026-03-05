from lab3.dimacs import *
from test import run_all_tests

def create_graph(V,L):
    G = [[] for _ in range (V)]
    L_new = []
    for (x,y,c) in L:
        G[x-1].append((y-1,c))
        G[y-1].append((x-1,c))
        L_new.append(c)

    return G, L_new

from collections import deque
from math import inf

def bfs(G, s, t, min):
    Q = deque()
    visited = [False for _ in range(len(G))]

    visited[s] = True
    Q.append(s)

    while Q:
        v = Q.popleft()
        for u,w in G[v]:
            if w >= min and not visited[u]:
                visited[u] = True
                Q.append(u)

    return visited[t]

def dfs(G,s,t,min):
    def dfsvisit(G, v):
        visited[v] = True
        for u,w in G[v]:
            if not visited[u] and w >= min:
                dfsvisit(G, u)

    visited = [False for _ in range(len(G))]
    dfsvisit(G, s)
    return visited[t]


def lab0(V, L):
    s = 0
    t = 1
    G,L_n= create_graph(V,L)
    L_n.sort()
    maxi = len(L_n)-1
    def binary_search(maxi):
        left = 0
        right = maxi
        result = None
        while left <= right:
            mid = (left + right) // 2
            flag = bfs(G,s,t,L_n[mid])
            if flag == True:
                left = mid + 1
                result = L_n[mid]
            else:
                right = mid - 1
        return result
    return binary_search(maxi)


if __name__ == "__main__":
    run_all_tests(lab0)