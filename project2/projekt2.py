from data import runtests
def solve(friendships, costs):
    n = len(costs)
    adj = [[] for _ in range(n + 1)]
    for u, v in friendships:
        adj[u].append(v)
        adj[v].append(u)

    partition = [set(range(1, n + 1))]
    peo = []
    
    v_to_part = {v: 0 for v in range(1, n + 1)}

    while partition:
        v = partition[-1].pop()
        if not partition[-1]:
            partition.pop()
        peo.append(v)
        
        to_split = {}
        for neighbor in adj[v]:
            if neighbor in v_to_part:
                p_idx = v_to_part[neighbor]
                if p_idx not in to_split:
                    to_split[p_idx] = set()
                to_split[p_idx].add(neighbor)
        
        for p_idx in sorted(to_split.keys(), reverse=True):
            neighbors_in_p = to_split[p_idx]
            original_p = partition[p_idx]
            
            if len(neighbors_in_p) < len(original_p):
                original_p.difference_update(neighbors_in_p)
                partition.insert(p_idx + 1, neighbors_in_p)
                for node in neighbors_in_p:
                    v_to_part[node] = p_idx + 1
                for i in range(p_idx + 2, len(partition)):
                    for node in partition[i]:
                        v_to_part[node] = i
            
        del v_to_part[v]

    peo_rev = peo[::-1]
    pos = [0] * (n + 1)
    for i, v in enumerate(peo_rev):
        pos[v] = i

    adj_lower = [[] for _ in range(n + 1)]
    for u in range(1, n + 1):
        u_pos = pos[u]
        for v in adj[u]:
            if pos[v] < u_pos:
                adj_lower[u].append(v)


    y = [0.0] * (n + 1)
    for v in peo_rev:
        lower_y_sum = 0
        for neighbor in adj_lower[v]:
            lower_y_sum += y[neighbor]
        
        y[v] = max(0, costs[v-1] - lower_y_sum)

    independent_set_weight = 0
    in_independent_set = [False] * (n + 1)
    
    for v in reversed(peo_rev):
        if y[v] > 0:
            can_add = True
            for neighbor in adj[v]:
                if in_independent_set[neighbor]:
                    can_add = False
                    break
            if can_add:
                in_independent_set[v] = True
                independent_set_weight += costs[v-1]

    return sum(costs) - independent_set_weight

runtests(solve)