import random
import numpy as np
import networkx as nx
from Algorithms.AbstractAlgo import AbstractAlgo

class GeneticAlgo(AbstractAlgo):
    def __init__(self, graph, name = None, num_vehicles = 5, solutions_in_parallel = 10, min_iterations = 0, max_iterations = 100, convergence_threshold = 5):
        super().__init__(graph=graph, name=name, num_vehicles=num_vehicles, min_iterations=min_iterations, max_iterations=max_iterations, convergence_threshold=convergence_threshold)
        self.solutions_in_parallel = solutions_in_parallel
        self.get_distance_matrix()

    def get_distance_matrix(self):
        self.distance_matrix = {}
        for i in range(len(list(self.graph.nodes))):
            self.distance_matrix[list(self.graph.nodes)[i]] = {}
            for j in range(len(list(self.graph.nodes))):
                self.distance_matrix[list(self.graph.nodes)[i]][list(self.graph.nodes)[j]] = nx.shortest_path_length(self.graph, source=list(self.graph.nodes)[i], target=list(self.graph.nodes)[j], weight="weight")


    def get_random_solutions(self):
        # Generate a list(solution) of lists(containing the destination per vehicle)
        # Each vehicle will have a random path
        # The path will be a random permutation of the nodes

        solutions = []

        for solution_index in range(self.solutions_in_parallel):
            nodes = list(self.graph.nodes)[1:]
            solution = [[] for i in range(self.num_vehicles)]
            while len(nodes) > 0:
                for i in range(self.num_vehicles):
                    if len(nodes) == 0:
                        break
                    node = random.choice(nodes)
                    solution[i].append(node)
                    nodes.remove(node)
                
            for j in range(len(solution)):
                if len(solution[j]) == 0:
                    continue
                solution[j].insert(0, list(self.graph.nodes)[0])
                solution[j].append(list(self.graph.nodes)[0])
            
            solutions.append(solution)
        
        return solutions
    
    def get_distance_per_vehicle(self, solution):
        # Calculate the distance for each vehicle
        distances = 0
        for i in range(len(solution)-1):
            distances += nx.shortest_path_length(self.graph, source=solution[i], target=solution[i+1], weight="weight")
        return distances
    
    def get_total_distance(self, solution):
        # Calculate the total distance of the solution
        total_distance = 0
        for i in range(len(solution)):
            total_distance += self.get_distance_per_vehicle(solution[i])
        return total_distance
    
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
                    if node1 == node2:
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
        # Run the genetic algorithm
        # Generate a random solution
        solutions = self.get_random_solutions()
        self.distance_history = [] #TODO
        
        
        for i in range(self.max_iterations):
            # Sort solutions by their total distance
            solutions = sorted(solutions, key=lambda s: self.get_total_distance(s))
            solutions = solutions[:len(solutions)//2] 
            solutions_distances = [self.get_total_distance(s) for s in solutions]
            self.distance_history.append(solutions_distances[0])

            # Create new solutions by combining the best solutions
            solutions = self.mutate(solutions)

        paths = sorted(solutions, key=lambda s: self.get_total_distance(s))[0]
        self.paths = sorted(solutions, key=lambda s: self.get_total_distance(s))[0]
        self.distance = self.get_total_distance(self.paths)
        self.iterations_needed = -1 #TODO
        self.total_interations_realized = 100
