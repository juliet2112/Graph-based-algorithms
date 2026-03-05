from lab3.dimacs import *
from test import run_all_tests

class Node:
    def __init__(self,val):
        self.val = val
        self.parent = self
        self.rank = 0
        
def find(x):
    if x != x.parent:
        x.parent = find(x.parent)
    return x.parent

def union(x, y):
    x = find(x)
    y = find(y)
    if x == y:
        return
    if x.rank < y.rank:
        x.parent = y
    else:
        y.parent = x
        if x.rank == y.rank:
            x.rank += 1


def lab0(V,L):
    s = 1
    t = 2
    L.sort(key=lambda x: x[2], reverse=True)
    nodes = [Node(i) for i in range (V+1)]
    i = 0
    while find(nodes[s]) != find(nodes[t]):
        v,u,w = L[i]
        union(nodes[v],nodes[u])
        i+=1

    return L[i-1][2]

if __name__ == "__main__":
    run_all_tests(lab0)




