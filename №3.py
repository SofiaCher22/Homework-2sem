import math
from collections import defaultdict

class CurrencyExchangeGraph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_exchange(self, from_currency, to_currency, rate):

        self.graph[from_currency].append((to_currency, -math.log(rate)))

    def has_negative_cycle(self):

        distances = {}
        
        for currency in self.graph:
            distances[currency] = float('inf')
        distances['RUB'] = 0  

        for _ in range(len(self.graph) - 1):
            for u in self.graph:
                for v, weight in self.graph[u]:
                    if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight

        for u in self.graph:
            for v, weight in self.graph[u]:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    return True 

        return False


exchange_graph = CurrencyExchangeGraph()


exchange_graph.add_exchange('RUB', 'USD', 0.01)  
exchange_graph.add_exchange('USD', 'EUR', 2)     
exchange_graph.add_exchange('EUR', 'RUB', 3)      

if exchange_graph.has_negative_cycle():
    print("Можно бесконечно обогатиться!")
else:
    print("Бесконечное обогащение невозможно.")