import random
import numpy as np
import networkx as nx
from Algorithms.AbstractAlgo import AbstractAlgo

class GeneticAlgo:
    def __init__(self, graph, name = None, iterations = 100, trucks = 1, solutions_in_parallel = 10):
        self.graph = graph
        self.name = name
        self.iterations = iterations
        self.trucks = trucks
        self.solutions_in_parallel = solutions_in_parallel
        self.get_distance_matrix()

    def get_distance_matrix(self):
        self.distance_matrix = {}
        for i in range(len(list(self.graph.nodes))):
            self.distance_matrix[list(self.graph.nodes)[i]] = {}
            for j in range(len(list(self.graph.nodes))):
                self.distance_matrix[list(self.graph.nodes)[i]][list(self.graph.nodes)[j]] = nx.shortest_path_length(self.graph, source=list(self.graph.nodes)[i], target=list(self.graph.nodes)[j], weight="weight")


    def get_random_solutions(self):
        # Generate a list(solution) of lists(containing the destination per truck)
        # Each truck will have a random path
        # The path will be a random permutation of the nodes

        solutions = []

        for i in range(self.solutions_in_parallel):
            nodes = list(self.graph.nodes)[1:]
            solution = [[] for i in range(self.trucks)]
            while len(nodes) > 0:
                for i in range(self.trucks):
                    if len(nodes) == 0:
                        break
                    node = random.choice(nodes)
                    solution[i].append(node)
                    nodes.remove(node)
                
            for i in range(len(solution)):
                if len(solution[i]) == 0:
                    continue
                solution[i].insert(0, list(self.graph.nodes)[0])
                solution[i].append(list(self.graph.nodes)[0])
            
                solutions.append(solution)
        
        return solutions
    
    def get_distance_per_truck(self, solution):
        # Calculate the distance for each truck
        distances = []
        for i in range(len(solution)):
            distance = 0
            for j in range(len(solution[i])):
                if j == len(solution[i]) - 1:
                    break
                distance += nx.shortest_path_length(self.graph, source=solution[i][j], target=solution[i][j+1], weight="weight")
            distances.append(distance)
        return distances
    
    def get_total_distance(self, solution):
        # Calculate the total distance of the solution
        total_distance = 0
        for i in range(len(solution)):
            total_distance += self.get_distance_per_truck(solution)[i]
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
                    node1 = random.choice(solution[i]).copy()
                    node2 = random.choice(solution[i]).copy()
                    random_index1, random_index2 = random.randint(1, len(node1)-2), random.randint(1, len(node2)-2)
                    if node1 == node2:
                        node1[random_index1], node1[random_index2] = node1[random_index2], node1[random_index1]
                        solution.append([node1])
                    else:
                        node1[random_index1], node2[random_index2] = node2[random_index2], node1[random_index1]
                        if(random.random() < 0.5): solution.append([node1])
                        else: solution.append([node2])
        return solution
    
    def run(self):
        # Run the genetic algorithm
        # Generate a random solution
        solutions = self.get_random_solutions()
        
        
        for i in range(self.iterations):
            # Sort solutions by their total distance
            solutions = sorted(solutions, key=lambda s: self.get_total_distance(s))
            solutions_distances = [self.get_total_distance(s) for s in solutions]
            solutions = solutions[:len(solutions)//2] 
            solutions_distances = [self.get_total_distance(s) for s in solutions]

            # Create new solutions by combining the best solutions
            solutions = self.mutate(solutions)

        value = sorted(solutions, key=lambda s: self.get_total_distance(s))[0]
        value2 = self.get_total_distance(value)
        return sorted(solutions, key=lambda s: self.get_total_distance(s))[0]