import numpy as np
from Algorithms.AbstractAlgo import AbstractAlgo

class GreedyAlgo(AbstractAlgo):
    def __init__(self, graph, max_iterations=100, convergence_threshold=5):
        super().__init__(graph, max_iterations, convergence_threshold)
    
    def run(self):
        current_node = list(self.graph.nodes)[0]
        visited = [current_node]
        path = [current_node]
        
        for _ in range(len(self.graph.nodes) - 1):
            next_node = self.get_nearest_neighbour(current_node, visited)
            path.append(next_node)
            visited.append(next_node)
            current_node = next_node
        
        if self.graph.has_edge(current_node, path[0]):
                path.append(path[0])
                return path
        else:
             return None
    
    def get_nearest_neighbour(self, current_node, visited):
        neighbours = []

        #find all neighbors not visited
        for n in self.graph.neighbors(current_node):
            if n not in visited:
                neighbours.append(n)

        nearest = None 
        shortest_distance = float('inf')

        #find the nearest neighbor
        for n in neighbours:
            distance = self.graph[current_node][n]['weight']
            if distance < shortest_distance:
                nearest = n
                shortest_distance = distance
                
        return nearest