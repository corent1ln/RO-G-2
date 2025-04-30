import random
import time
import numpy as np
from Algorithms.AbstractAlgo import AbstractAlgo

class GeneticAlgo(AbstractAlgo):
    def __init__(self, graph, name = None, num_vehicles = 5, solutions_in_parallel = 10, min_iterations = 0, max_iterations = 100, convergence_threshold = 5):
        super().__init__(graph=graph, name=name, num_vehicles=num_vehicles, min_iterations=min_iterations, max_iterations=max_iterations, convergence_threshold=convergence_threshold)
        self.solutions_in_parallel = solutions_in_parallel


    def get_random_solutions(self):
        # Generate a list(solution) of lists(containing the destination per vehicle)
        # Each vehicle will have a random path
        # The path will be a random permutation of the nodes

        solutions = []

        for _ in range(self.solutions_in_parallel):
            nodes = list(self.graph.nodes)[1:]
            solution = [[] for i in range(self.num_vehicles)]
            while len(nodes) > 0:
                for i in range(self.num_vehicles):
                    if len(nodes) == 0:
                        break
                    node = random.choice(nodes)
                    if len(solution[i]) > 0 and not self.graph.has_edge(solution[i][-1], node):
                        continue
                    solution[i].append(node)
                    nodes.remove(node)
                
            for j in range(len(solution)):
                if len(solution[j]) == 0:
                    continue
                solution[j].insert(0, list(self.graph.nodes)[0])
                solution[j].append(list(self.graph.nodes)[0])
            
            solutions.append(solution)
        
        return solutions 
    
    def mutate(self, solution):
        # Mutate the solution by swapping two random nodes
        # This will create a new solution
        # The mutation rate is 0.1
        mutation_rate = 0.1
        while(len(solution) < self.solutions_in_parallel):
            for i in range(len(solution)):
                if random.random() < mutation_rate:
                    # Swap two random nodes
                    solution_to_mutate = solution[i].copy()
                    node1 = random.choice(solution_to_mutate).copy()
                    node2 = random.choice(solution_to_mutate).copy()
                    random_index1, random_index2 = random.randint(1, len(node1)-2), random.randint(1, len(node2)-2)
                    if node1 == node2: # only one vehicle or same vehicle
                        solution_to_mutate.remove(node1)
                        node1[random_index1], node1[random_index2] = node1[random_index2], node1[random_index1]
                        solution_to_mutate.append(node1)
                        solution.append(solution_to_mutate)
                    else:
                        solution_to_mutate.remove(node1)
                        solution_to_mutate.remove(node2)
                        node1[random_index1], node2[random_index2] = node2[random_index2], node1[random_index1]
                        solution_to_mutate.append(node1)
                        solution_to_mutate.append(node2)
                        solution.append(solution_to_mutate)
        return solution
    
    def run(self):
        best_distance = float('inf')
        start_time = time.time()
        # Run the genetic algorithm
        # Generate a random solution
        solutions = self.get_random_solutions()
        self.distance_history = []
        similar_results_count = 0
        for iteration in range(1, self.max_iterations + 1):
            distances = []
            standard_deviations = []
            # Sort solutions by their total distance
            for solution in solutions:
                total_distance = 0
                vehicle_distances = []
                for idx, vehicle in enumerate(solution): 
                    vehicle_distance = 0
                    for i in range(len(vehicle) - 1):
                        if self.graph.has_edge(vehicle[i], vehicle[i + 1]): 
                            vehicle_distance += self.graph[vehicle[i]][vehicle[i + 1]]["weight"]
                        else:
                            vehicle_distance = float('inf')
                            break
                        vehicle_distances.append(vehicle_distance)
                    total_distance += vehicle_distance
                distances.append(total_distance)
                standard_deviations.append(np.std(vehicle_distances))

            scores = [distances[i] + standard_deviations[i] for i in range(len(distances))]
            sorted_indices = np.argsort(scores)
            solutions = [solutions[i] for i in sorted_indices[:len(solutions) // 2]] #get half (the betters)
            
            current_best_distance = distances[sorted_indices[0]]
            if current_best_distance < best_distance:
                best_distance = current_best_distance
            self.distance_history.append(best_distance)
            if len(self.distance_history) > 1 and self.distance_history[-1] == self.distance_history[-2]:
                similar_results_count += 1
            else:
                similar_results_count = 0

            if similar_results_count >= self.convergence_threshold and iteration > self.min_iterations:
                break

            # Create new solutions by combining the best solutions
            solutions = self.mutate(solutions)

        self.paths = solutions[0]
        self.distance = self.distance_history[-1]
        self.iterations_needed = iteration - similar_results_count
        self.total_interations_realized = iteration
        self.distance_per_vehicles = [sum(self.graph[vehicle[i]][vehicle[i + 1]]["weight"] for i in range(len(vehicle) - 1)) for vehicle in self.paths]
        self.distance_average_per_vehicles = np.mean(self.distance_per_vehicles)
        self.distance_standard_deviation_per_vehicles = np.std(self.distance_per_vehicles)
        self.execution_time = time.time() - start_time


