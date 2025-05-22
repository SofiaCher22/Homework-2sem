from collections import deque

n = int(input())

G = {i: {} for i in range(n)}
G['S'] = {}
G['F'] = {}

for i in range(n):
    ai, bi = map(int, input().split())
    G['S'][i] = ai
    G[i]['F'] = bi
    G[i]['S'] = 0
    G['F'][i] = 0

m = int(input())

for i in range(m):
    vi, vj, cij = map(int, input().split())
    G[vi][vj] = cij
    G[vj][vi] = 0

def bfs(G, start, finish, parent):
    visited = set()
    queue = deque()
    queue.append(start)
    visited.add(start)
    
    while queue:
        u = queue.popleft()
        for v in G[u]:
            if v not in visited and G[u][v] > 0:
                parent[v] = u
                if v == finish:
                    return True
                visited.add(v)
                queue.append(v)
    return False

def edmonds_karp(G, start, finish):
    parent = {}
    max_flow = 0
    
    while bfs(G, start, finish, parent):
        path_flow = float('Inf')
        v = finish
        
        while v != start:
            u = parent[v]
            path_flow = min(path_flow, G[u][v])
            v = u
        
        v = finish
        while v != start:
            u = parent[v]
            G[u][v] -= path_flow
            G[v][u] += path_flow
            v = u
        
        max_flow += path_flow
        parent = {}
    
    visited = set()
    queue = deque()
    queue.append(start)
    visited.add(start)
    
    while queue:
        u = queue.popleft()
        for v in G[u]:
            if v not in visited and G[u][v] > 0:
                visited.add(v)
                queue.append(v)
    
    prog = visited - {'S', 'F'}
    mat = set(G.keys()) - visited - {'S', 'F'}
    
    return max_flow, mat, prog

max_flow, mat, prog = edmonds_karp(G, 'S', 'F')
print(f"Max flow: {max_flow}")
print(f"Mathematicians: {mat}")
print(f"Programmers: {prog}")