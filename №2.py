import heapq
from collections import defaultdict

class Graph:
    def __init__(self, ver):
        self.V = ver
        self.graph = defaultdict(list)  

    def add_edge(self, u, v, w):
        self.graph[u].append((v, w))  

    def bellman_ford(self, src):
        distance = [float('inf')] * self.V
        distance[src] = 0

        for _ in range(self.V - 1):
            for u in range(self.V):
                for v, w in self.graph[u]:
                    if distance[u] != float('inf') and distance[u] + w < distance[v]:
                        distance[v] = distance[u] + w

        for u in range(self.V):
            for v, w in self.graph[u]:
                if distance[u] != float('inf') and distance[u] + w < distance[v]:
                    raise ValueError("содержит отрицательный цикл")

        return distance

    def dijkstra(self, src, h):
        distance = [float('inf')] * self.V
        distance[src] = 0
        priority_queue = [(0, src)]  

        while priority_queue:
            dist_u, u = heapq.heappop(priority_queue)

            if dist_u > distance[u]:
                continue

            for v, w in self.graph[u]:

                weight = w + h[u] - h[v]
                if distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    heapq.heappush(priority_queue, (distance[v], v))

        return distance

    def johnson(self):

        for u in range(self.V):
            self.graph[self.V].append((u, 0))


        h = self.bellman_ford(self.V)


        del self.graph[self.V]

        all_pairs_short_paths = []
        for u in range(self.V):
            distances = self.dijkstra(u, h)
            all_pairs_short_paths.append(distances)

        return all_pairs_short_paths


g = Graph(5)
g.add_edge(0, 1, -1)
g.add_edge(0, 2, 4)
g.add_edge(1, 2, 3)
g.add_edge(1, 3, 2)
g.add_edge(1, 4, 2)
g.add_edge(3, 1, 1)
g.add_edge(3, 4, 5)
g.add_edge(4, 3, -3)

try:
    all_pairs_short_paths = g.johnson()
    for i in range(len(all_pairs_short_paths)):
        print(f"Кратчайшие пути от вершины {i}: {all_pairs_short_paths[i]}")
except ValueError as e:
    print(e)