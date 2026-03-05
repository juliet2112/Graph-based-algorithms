from data import runtests
from math import log10, inf, sqrt
from collections import deque

def add_edge(G, u, v, cap):
    G[u].append([v, cap, len(G[v])])
    G[v].append([u, 0, len(G[u]) - 1])



def residual_net(V,num):
    memo_for = {}
    memo_back = {}
    n = V+len(num)
    next_id = 2 #0 - start, 1 - end
    is_prime = [True for _ in range (V+2)]
    G = [[] for _ in range (n)]
    is_prime[0] = is_prime[1] = False
    for i in range(2, V+2):
        if is_prime[i]:
            times = 1 
            id = next_id
            memo_for[(i,times)] = id 
            memo_back[id] = [i,times]
            next_id+=1
            cost = 5*log10(i)
            add_edge(G,id,1,cost)
            prev = i

            for j in range(i*i, V+2, i):
                is_prime[j] = False
                if j%prev == 0:
                    times+=1 
                    id = next_id
                    memo_for[(i,times)] = id 
                    memo_back[id] = [i,times]
                    next_id+=1
                    add_edge(G,id,1,cost)
                    add_edge(G,id,memo_for[(i,times-1)],inf)
                    prev = j
                

    for n,luck in num:
        id = next_id
        memo_for[n] = id 
        memo_back[id] = n
        next_id+=1
        add_edge(G,0,id,luck)
        for i in range (2,V+2):
            if is_prime[i]:
                times = 0
                j = i
                while n%j == 0 and j < V+2:
                    times+=1 
                    j*=i
                if times > 0:
                    add_edge(G,id,memo_for[(i,times)],inf)
            
    return memo_back,G,next_id

def reachable_from_s(R):
    n = len(R)
    visited = [False] * n
    Q = deque([0])
    visited[0] = True

    while Q:
        v = Q.popleft()
        for u,w,_ in R[v]:
            if not visited[u] and w > 0:
                visited[u] = True
                Q.append(u)
    return visited

def dinic(G,n):
    level = []
    s = 0
    t = 1
    def bfs():
        """Buduje graf warstwowy (Level Graph). Zwraca True jeśli t jest osiągalne."""
        nonlocal level
        level = [-1 for _ in range(n)]
        level[s] = 0
        queue = deque([s])
        
        while queue:
            u = queue.popleft()
            for v, cap, _ in G[u]:
                if cap > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[t] >= 0
    
    def dfs(u, pushed, ptr):
        """Wypycha przepływ (Blocking Flow)."""
        if pushed == 0 or u == t:
            return pushed
        
        for i in range(ptr[u], len(G[u])):
            ptr[u] = i # Aktualizacja wskaźnika (Pointer Optimization)
            v, cap, rev_idx = G[u][i]
            
            if level[v] != level[u] + 1 or cap == 0:
                continue
            
            tr = dfs(v, min(pushed, cap), ptr)
            if tr == 0:
                continue
            # Aktualizacja przepływów
            G[u][i][1] -= tr
            G[v][rev_idx][1] += tr
            return tr
            
        return 0
    
    max_flow = 0
    
    while bfs():
        ptr = [0] * n
        while True:
            pushed = dfs(s, inf, ptr)
            if pushed == 0:
                break
            max_flow += pushed
            
    return max_flow,G


def solve(scores):
    max_luck = 0
    V = 0
    for x, luck in scores:
        max_luck += luck
        V = max(V, x)
    memo,R,n = residual_net(V,scores)


    _,G = dinic(R,n)
    reachable = reachable_from_s(G)

    result = 1

    for node_id, data in memo.items():
        if isinstance(data, list):  # [prime, power]
            p, _ = data

            if reachable[node_id]:
                    result *= p

    return result
       

runtests(solve)
