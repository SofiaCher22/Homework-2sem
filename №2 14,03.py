from collections import deque

def min_edge(bipartite_graph, U, V):

    match= max_match(bipartite_graph, U, V)
    
    uncovered_U = U - {u for u, v in match}
    uncovered_V = V - {v for u, v in match}
    

    edge_cover = set(match)
    
    for u in uncovered_U:
        for v in bipartite_graph[u]:
            edge_cover.add((u, v))
            break  
    
    for v in uncovered_V:
        for u in [u for u in bipartite_graph if v in bipartite_graph[u]]:
            edge_cover.add((u, v))
            break  
    
    return edge_cover

def max_match(graph, U, V):

    pair_U = {u: None for u in U}
    pair_V = {v: None for v in V}
    
    def bfs():
        queue = deque()
        for u in U:
            if pair_U[u] is None:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = float('inf')
        dist[None] = float('inf')
        
        while queue:
            u = queue.popleft()
            if dist[u] < dist[None]:
                for v in graph[u]:
                    if dist[pair_V[v]] == float('inf'):
                        dist[pair_V[v]] = dist[u] + 1
                        queue.append(pair_V[v])
        return dist[None] != float('inf')
    
    def dfs(u):
        for v in graph[u]:
            if pair_V[v] is None or (dist[pair_V[v]] == dist[u] + 1 and dfs(pair_V[v])):
                pair_U[u] = v
                pair_V[v] = u
                return True
        dist[u] = float('inf')
        return False
    
    dist = {}
    match = set()
    
    while bfs():
        for u in U:
            if pair_U[u] is None:
                if dfs(u):
                    pass
    
    match = {(u, v) for u, v in pair_U.items() if v is not None}
    return match