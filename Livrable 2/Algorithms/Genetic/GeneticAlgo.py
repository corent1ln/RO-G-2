import random
import time
import numpy as np
import networkx as nx
from Algorithms.AbstractAlgo import AbstractAlgo
from functools import lru_cache


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
            # Mélange les noeuds pour créer une solution aléatoire
            shuffled = random.sample(nodes, len(nodes))
            solution = [[] for _ in range(self.num_vehicles)]
            for i, node in enumerate(shuffled):
                # Répartit les noeuds entre les véhicules
                solution[i % self.num_vehicles].append(node)
            # Ajoute le noeud de départ et de retour à chaque route
            full_solution = [[self.start_node] + route + [self.start_node] for route in solution]
            solutions.append(full_solution)
        return solutions

    @lru_cache(maxsize=None)
    def get_shortest_path_length(self, source, target):
        # Calcule le chemin le plus court entre deux noeuds
        # Vérifie si une arête directe existe entre source et target
        if self.graph.has_edge(source, target):
            return self.graph[source][target]["weight"]
        # Sinon, calcule le chemin le plus court
        path = nx.shortest_path(self.graph, source=source, target=target, weight="weight")
        length = nx.path_weight(self.graph, path, weight="weight")
        return length

    def evaluate_solution(self, solution):
        # Évalue une solution en calculant les distances totales et l'écart-type
        vehicle_distances = [
            sum(self.get_shortest_path_length(route[i], route[i+1]) for i in range(len(route) - 1))
            for route in solution
        ]
        total = sum(vehicle_distances)  # Distance totale
        std = np.std(vehicle_distances)  # Écart-type des distances
        return total, std, vehicle_distances

    def crossover(self, parents):
        # Effectue le croisement entre les solutions parentales
        new_solutions = []
        while len(new_solutions) + len(parents) < self.solutions_in_parallel:
            # Sélectionne deux parents aléatoires
            p1, p2 = random.sample(parents, 2)
            child = [[] for _ in range(self.num_vehicles)]
            assigned = set()

            # Ajoute une partie des noeuds du premier parent
            for i in range(self.num_vehicles):
                middle = p1[i][1:-1][:len(p1[i])//2]  # Exclut le dépôt
                for node in middle:
                    if node not in assigned:
                        child[i].append(node)
                        assigned.add(node)

            # Complète avec les noeuds du second parent
            for i in range(self.num_vehicles):
                for node in p2[i][1:-1]:
                    if node not in assigned:
                        child[i].append(node)
                        assigned.add(node)

            # Ajoute les noeuds manquants
            all_nodes = set(self.graph.nodes) - {self.start_node}
            missing = list(all_nodes - assigned)
            for node in missing:
                shortest = min(child, key=len)
                shortest.append(node)

            # Ajoute le dépôt au début et à la fin de chaque route
            full_child = [[self.start_node] + route + [self.start_node] for route in child]
            new_solutions.append(full_child)
        return parents + new_solutions

    def mutate(self, solutions):
        # Applique des mutations aléatoires aux solutions
        new_solutions = []
        for sol in solutions:
            mutated = [route[:] for route in sol]
            for route in mutated:
                # Échange deux noeuds aléatoires dans une route avec une certaine probabilité
                if len(route) > 3 and random.random() < self.mutation_rate:
                    i, j = sorted(random.sample(range(1, len(route) - 1), 2))
                    route[i], route[j] = route[j], route[i]
            new_solutions.append(mutated)
        return new_solutions

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
                        vehicle_distance += self.graph[vehicle[i]][vehicle[i + 1]]["weight"]
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


