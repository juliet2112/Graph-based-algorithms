from data import runtests
from math import log10, inf, sqrt
from collections import deque


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


def Ford_Fulkerson(R, memo):
    max_flow = 0
    s = 0
    t = 1

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
        

    return R

def residual_net(V,num):
    memo_for = {}
    memo_back = {}
    n = V+len(num)
    next_id = 2 #0 - start, 1 - end
    is_prime = [True for _ in range (V+2)]
    G = [[0 for _ in range (n)] for _ in range (n)]
    is_prime[0] = is_prime[1] = False
    for i in range(2, V+2):
        if is_prime[i]:
            times = 1 
            id = next_id
            memo_for[(i,times)] = id 
            memo_back[id] = [i,times]
            next_id+=1
            cost = 5*log10(i)
            G[id][1] = cost
            prev = i

            for j in range(i*i, V+2, i):
                is_prime[j] = False
                if j%prev == 0:
                    times+=1 
                    id = next_id
                    memo_for[(i,times)] = id 
                    memo_back[id] = [i,times]
                    next_id+=1
                    G[id][1] = cost
                    G[id][memo_for[(i,times-1)]] = inf
                    prev = j
                

    for n,luck in num:
        id = next_id
        memo_for[n] = id 
        memo_back[id] = n
        next_id+=1
        G[0][id] = luck
        for i in range (2,V+2):
            if is_prime[i]:
                times = 0
                j = i
                while n%j == 0 and j < V+2:
                    times+=1 
                    j*=i
                if times > 0:
                    G[id][memo_for[(i,times)]]=inf
            
    return memo_back,G

def reachable_from_s(R):
    n = len(R)
    visited = [False] * n
    Q = deque([0])
    visited[0] = True

    while Q:
        v = Q.popleft()
        for u in range(n):
            if not visited[u] and R[v][u] > 0:
                visited[u] = True
                Q.append(u)
    return visited

def solve(scores):
    max_luck = 0
    V = 0
    for x, luck in scores:
        max_luck += luck
        V = max(V, x)


    memo,R = residual_net(V,scores)
    G = Ford_Fulkerson(R,memo)
    reachable = reachable_from_s(G)

    result = 1

    for node_id, data in memo.items():
        if isinstance(data, list):  # [prime, power]
            p, _ = data

            if reachable[node_id]:
                    result *= p

    return result
       

runtests(solve)
