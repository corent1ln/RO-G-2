import random
import time
import numpy as np
from Algorithms.AbstractAlgo import AbstractAlgo

class GeneticAlgo(AbstractAlgo):
    def __init__(self, graph, name=None, num_vehicles=5, solutions_in_parallel=10, min_iterations=0, max_iterations=100, convergence_threshold=5, mutation_rate=0.1):
        super().__init__(graph=graph, name=name, num_vehicles=num_vehicles,
                         min_iterations=min_iterations, max_iterations=max_iterations,
                         convergence_threshold=convergence_threshold)
        self.solutions_in_parallel = solutions_in_parallel
        self.start_node = list(self.graph.nodes)[0]
        self.mutation_rate = mutation_rate

    def get_random_solutions(self):
        # Génère des solutions aléatoires initiales
        solutions = []
        nodes = list(self.graph.nodes)[1:]  # Exclut le noeud de départ
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

    def evaluate_solution(self, solution):
        # Évalue une solution en calculant les distances totales et l'écart-type
        vehicle_distances = [
            sum(self.graph[route[i]][route[i + 1]]["weight"] for i in range(len(route) - 1))
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
        # Exécute l'algorithme génétique
        start_time = time.time()  # Temps de début
        best_distance = float("inf")  # Meilleure distance trouvée
        solutions = self.get_random_solutions()  # Génère des solutions initiales
        self.distance_history = []  # Historique des distances
        similar_results_count = 0  # Compteur de convergence

        for iteration in range(1, self.max_iterations + 1):
            # Évalue toutes les solutions
            evaluations = [self.evaluate_solution(sol) for sol in solutions]
            distances = [e[0] for e in evaluations]
            stds = [e[1] for e in evaluations]

            # Calcule les scores en combinant distance et écart-type
            scores = [distances[i] + stds[i] for i in range(len(solutions))]
            sorted_indices = np.argsort(scores)

            # Sélectionne les meilleures solutions (survivants)
            survivors = [solutions[i] for i in sorted_indices[:len(solutions) // 2]]
            best_current = distances[sorted_indices[0]]  # Meilleure distance actuelle

            # Met à jour la meilleure distance si nécessaire
            if best_current < best_distance:
                best_distance = best_current
            self.distance_history.append(best_distance)

            # Vérifie la convergence
            if len(self.distance_history) > 1 and self.distance_history[-1] == self.distance_history[-2]:
                similar_results_count += 1
            else:
                similar_results_count = 0
            if similar_results_count >= self.convergence_threshold and iteration >= self.min_iterations:
                break

            # Génère les enfants par croisement et mutation
            children = self.crossover(survivors)
            solutions = self.mutate(children)

        # Évalue la solution finale
        final_solution = solutions[0]
        self.paths = final_solution
        self.distance, _, vehicle_distances = self.evaluate_solution(final_solution)
        self.distance_per_vehicles = vehicle_distances
        self.distance_average_per_vehicles = np.mean(vehicle_distances)
        self.distance_standard_deviation_per_vehicles = np.std(vehicle_distances)
        self.iterations_needed = iteration - similar_results_count
        self.total_interations_realized = iteration
        self.execution_time = time.time() - start_time  # Temps d'exécution total
