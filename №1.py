class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    def is_connect(self):
        visited = set()

        start_ver= next(iter(self.graph))
        

        self.dfs(start_ver, visited)


        for vertex in self.graph:
            if vertex not in visited and len(self.graph[vertex]) > 0:
                return False
        return True

    def dfs(self, vertex, visited):
        visited.add(vertex)
        for neighbor in self.graph[vertex]:
            if neighbor not in visited:
                self.dfs(neighbor, visited)

    def has_eulerian_path(self):
        odd_degree_count = 0

        for vertex in self.graph:
            degree = len(self.graph[vertex])
            if degree % 2 != 0:
                odd_degree_count += 1

        return (odd_degree_count == 0 or odd_degree_count == 2) and self.is_connect()

g = Graph()
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 0)
g.add_edge(1, 3)

if g.has_eulerian_path():
    print("имеет эйлеров путь.")
else:
    print("не имеет эйлеров путь.")
