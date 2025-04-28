import numpy as np
from Algorithms.AbstractAlgo import AbstractAlgo

class GreedyAlgo(AbstractAlgo):
    def __init__(self, graph, name = None, num_vehicles = 1, min_iterations=0,max_iterations=100, convergence_threshold=5):
        super().__init__(graph, name, num_vehicles, min_iterations,max_iterations, convergence_threshold)
        self.start_node = list(self.graph.nodes)[0]
        self.current_nodes = [self.start_node for _ in range(self.num_vehicles)]
        self.paths = [[self.start_node] for _ in range(self.num_vehicles)]
        self.distances_per_vehicles = [0 for _ in range(self.num_vehicles)]
        self.unvisited_nodes = list(self.graph.nodes).copy()
        self.unvisited_nodes.remove(self.start_node)
        self.current_vehicle = 0
        if self.num_vehicles > len(self.graph.nodes):
            self.num_vehicles = len(self.graph.nodes)
    
    def reset(self):
        self.start_node = list(self.graph.nodes)[0]
        self.current_nodes = [self.start_node for _ in range(self.num_vehicles)]
        self.paths = [[self.start_node] for _ in range(self.num_vehicles)]
        self.distances_per_vehicles = [0 for _ in range(self.num_vehicles)]
        self.total_distance = 0
        self.unvisited_nodes = list(self.graph.nodes).copy()
        self.unvisited_nodes.remove(self.start_node)


    def select_vehicle(self):
        return (self.current_vehicle + 1) % self.num_vehicles

    def get_nearest_neighbour(self, current_node):
        neighbours = []

        #find all neighbors not visited
        for n in self.graph.neighbors(current_node):
            if n in self.unvisited_nodes:
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
    
    def move(self):
        current_node = self.current_nodes[self.current_vehicle]
        next_node = self.get_nearest_neighbour(current_node)
        if next_node is None:
            return False

        self.paths[self.current_vehicle].append(next_node)  # Add it to the path
        # Add the distance between the current node and the next node to the total distance
        self.total_distance += self.graph[self.current_nodes[self.current_vehicle]][next_node]["weight"]
        self.distances_per_vehicles[self.current_vehicle]+= self.graph[self.current_nodes[self.current_vehicle]][next_node]["weight"]
        self.current_nodes[self.current_vehicle] = next_node  # Update the current node to the next node
        self.unvisited_nodes.remove(next_node)  # Mark the next node as visited

        self.current_vehicle = self.select_vehicle()
        return True

    def greedy(self):
        while self.unvisited_nodes: 
            if not self.move():
                self.paths = []
                self.total_distance = float('inf')
                self.distances_per_vehicles = [float('inf') for _ in range(self.num_vehicles)]
                break
        for i in range(self.num_vehicles):
            if not self.unvisited_nodes:
                if self.graph.has_edge(self.current_nodes[i], self.start_node):
                    # After visiting all nodes, return to the starting node to complete the cycle
                    self.total_distance += self.graph[self.current_nodes[i]][self.start_node]["weight"]
                    self.paths[i].append(self.start_node)  # Add the starting node to the end of the path
                    self.distances_per_vehicles[i]+= self.graph[self.current_nodes[i]][self.start_node]["weight"]
    
    def run(self):
        best_paths = []
        best_distance = np.inf  # Start with a very large number for comparison
        best_distance_history = []
        similar_results_count = 0
        best_distance_average_per_vehicles = np.inf
        best_distance_standard_deviation_per_vehicles = np.inf


        best_distance_per_vehicles = []
        for iteration in range(1,self.max_iterations + 1):
            self.reset()
            self.greedy()
            if self.total_distance < best_distance and np.std(self.distances_per_vehicles) <= best_distance_standard_deviation_per_vehicles: #todo add average and standard deviation
                best_paths = self.paths
                best_distance = self.total_distance
                best_distance_per_vehicles = self.distances_per_vehicles
                best_distance_average_per_vehicles = np.average(best_distance_per_vehicles)
                best_distance_standard_deviation_per_vehicles = np.std(best_distance_per_vehicles)

            best_distance_history.append(best_distance)

            if len(best_distance_history) > 1 and best_distance_history[-1] == best_distance_history[-2]:
                similar_results_count += 1
            else:
                similar_results_count = 0

            if similar_results_count >= self.convergence_threshold and iteration > self.min_iterations:
                break

    
        self.total_interations_realized = iteration
        self.iterations_needed = iteration - similar_results_count
        self.paths = best_paths
        self.distance = best_distance
        self.distance_history = best_distance_history
        self.distance_per_vehicles = best_distance_per_vehicles
        self.distance_average_per_vehicles = best_distance_average_per_vehicles
        self.distance_standard_deviation_per_vehicles = best_distance_standard_deviation_per_vehicles