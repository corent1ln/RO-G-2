import numpy as np
from Algorithms.ACO.Ant import Ant
from Algorithms.AbstractAlgo import AbstractAlgo

# ACO (Ant Colony Optimization) class runs the algorithm to find the best path
class AcoAlgo(AbstractAlgo):
    def __init__(self, graph, num_vehicles = 1,name = None, num_ants = 100, decay=0.5, alpha=1.0, beta=2.0, min_iterations = 0, max_iterations = 100, convergence_threshold = 5):
        super().__init__(graph, name, num_vehicles,min_iterations,max_iterations, convergence_threshold)
        self.num_ants = num_ants  # Number of ants in each iteration
        self.decay = decay  # Rate at which pheromones evaporate
        self.alpha = alpha  # Strength of pheromone update
        self.beta = beta # Influence of distance in the probability calculation
        self.pheromones = {}
        self.initialize_pheromones(initial_value=1.0)
        if self.num_vehicles > len(self.graph.nodes):
            self.num_vehicles = len(self.graph.nodes)
    # Main function to run the ACO algorithm
    def run(self):
        best_paths = []
        best_distance = np.inf  # Start with a very large number for comparison
        best_distance_average_per_vehicles = np.inf
        best_distance_standard_deviation_per_vehicles = np.inf
        similar_results_count = 0
        best_distance_history = []
        best_distance_per_vehicles = []
        # Run the algorithm for the specified number of iterations
        for iteration in range(1,self.max_iterations +1):
            ants = [Ant(self.graph,self) for _ in range(self.num_ants)]  # Create a group of ants
            
            valid_ants = []

            for ant in ants:
                if(ant.complete_path()):  # Let each ant complete its path
                    valid_ants.append(ant)
                    # If the current ant's path is shorter than the best one found so far, update the best path
                    if ant.total_distance < best_distance and np.std(ant.distances_per_vehicles) <= best_distance_standard_deviation_per_vehicles: #todo add average and standard deviation
                        best_paths = ant.paths
                        best_distance = ant.total_distance
                        best_distance_per_vehicles = ant.distances_per_vehicles
                        best_distance_average_per_vehicles = np.average(best_distance_per_vehicles)
                        best_distance_standard_deviation_per_vehicles = np.std(best_distance_per_vehicles)
            self.update_pheromones(valid_ants)  # Update pheromones based on the ants' paths
            best_distance_history.append(best_distance)  # Save the best distance for each iteration
            #check if results are simular of the last iteration
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

    # Update the pheromones on the paths after all ants have completed their trips
    def update_pheromones(self, ants):
        for edge in self.pheromones:
            self.pheromones[edge] *= self.decay  # Reduce pheromones on all paths (evaporation)
        # For each ant, increase pheromones on the paths they took, based on how good their path was
        for ant in ants:
            for vehicle in range(self.num_vehicles):
                for i in range(len(ant.paths[vehicle]) - 1):
                    from_node = ant.paths[vehicle][i]
                    to_node = ant.paths[vehicle][i + 1]
                    edge = (from_node, to_node) if (from_node, to_node) in self.pheromones else (to_node, from_node)
                    # Update the pheromones inversely proportional to the total distance traveled by the ant
                    self.pheromones[edge] += self.alpha / ant.total_distance

    def initialize_pheromones(self, initial_value=1.0):
        for edge in self.graph.edges:
            self.pheromones[edge] = initial_value

    def get_pheromone(self, u, v):
        return self.pheromones.get((u, v), self.pheromones.get((v, u), 0))
    

    