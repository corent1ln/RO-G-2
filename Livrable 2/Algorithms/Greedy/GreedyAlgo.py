import numpy as np
from Algorithms.AbstractAlgo import AbstractAlgo

class GreedyAlgo(AbstractAlgo):
    def __init__(self, graph, name = None, min_iterations=0,max_iterations=100, convergence_threshold=5):
        super().__init__(graph, name, min_iterations,max_iterations, convergence_threshold)
    
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
    
    def greedy(self):
        current_node = list(self.graph.nodes)[0]
        visited = [current_node]
        path = [current_node]
        total_distance = 0
        
        for _ in range(len(self.graph.nodes) - 1):
            next_node = self.get_nearest_neighbour(current_node, visited)
            if(next_node is None):
                break
            path.append(next_node)
            visited.append(next_node)
            total_distance += self.graph[current_node][next_node]['weight']
            current_node = next_node
        
        if self.graph.has_edge(current_node, path[0]):
                path.append(path[0])
                total_distance += self.graph[current_node][path[0]]['weight']
        
        return path, total_distance
    
    def run(self):
        best_path = None
        best_distance = np.inf
        best_distance_history = []
        similar_results_count = 0

        for iteration in range(self.max_iterations):
            path, total_distance = self.greedy()
            if total_distance < best_distance:
                best_distance = total_distance
                best_path = path

            best_distance_history.append(best_distance)

            if len(best_distance_history) > 1 and best_distance_history[-1] == best_distance_history[-2]:
                similar_results_count += 1
            else:
                similar_results_count = 0

            if similar_results_count >= self.convergence_threshold and iteration > self.min_iterations:
                break

    
        self.total_interations_realized = iteration
        self.iterations_needed = iteration - similar_results_count
        self.path = best_path
        self.distance = best_distance
        self.distance_history = best_distance_history