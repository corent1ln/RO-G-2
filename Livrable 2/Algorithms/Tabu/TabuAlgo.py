from Algorithms.AbstractAlgo import AbstractAlgo
import numpy as np
import time

class TabuAlgo(AbstractAlgo):
    def __init__(self, graph, name = None, num_vehicles=1, size_tabou = 50, min_iterations=0,max_iterations=100, convergence_threshold=5):
        super().__init__(graph, name, num_vehicles, min_iterations,max_iterations, convergence_threshold)
        self.size_tabou = size_tabou
        if len(self.graph.nodes) < self.num_vehicles:
            self.num_vehicles = len(self.graph.nodes)-1
            print("ok")
        self.start_node = ''  

    def path_exists(self, path):

        for vehicle_path in path:
            for i in range(len(vehicle_path) - 1):
                u = vehicle_path[i]
                v = vehicle_path[i + 1]
                if not self.graph.has_edge(u, v):
                    return False
        return True

    def random_path(self):
        i = 0
        while i <(self.max_iterations * 100):
            full_node = list(self.graph.nodes()) # get random path
            self.start_node = full_node[0]
            full_node.remove(self.start_node)

            np.random.shuffle(full_node) 
            nodes_split = [full_node[i::self.num_vehicles] for i in range(self.num_vehicles)] # Split the path according to the number of vehicles
            path = [] # final path
            for nodes in nodes_split:
                nodes.insert(0, self.start_node)
                nodes.append(self.start_node)
                path.append(nodes)
            if self.path_exists(path):
                return path
            else:
                path = []
            i += 1

            if  i > self.convergence_threshold:
                break
        return None

    def get_distance_per_vehicule(self,path):
        distance_per_vehicules = []
        for vehicle_path in path:
            vehicle_distance = 0
            for i in range(len(vehicle_path) - 1):
                u = vehicle_path[i]
                v = vehicle_path[i + 1]
                if v in self.graph[u]:
                    vehicle_distance += self.graph[u][v]['weight']
                else:
                    print(f"No edge between {u} and {v}")
                    return float('inf') 
            distance_per_vehicules.append(vehicle_distance)
        return distance_per_vehicules
    
    def calculate_distance(self, path):
        distance_per_vehicules = self.get_distance_per_vehicule(path)
        return sum(distance_per_vehicules)
    
    def generate_neighbors(self, current_solution):
        neighbors = [current_solution]
        for i in range(2, len(current_solution) - 1):
            neighbor = current_solution[:]
            node_to_move = neighbor.pop(1)
            neighbor.insert(i, node_to_move)
            if self.path_exists([neighbor]):
                neighbors.append(neighbor)
        return neighbors
    
    def generate_all_neighbors(self, current_solution):
        every_neighbors = []
        for vehicle_path in current_solution: 
            neighbors = self.generate_neighbors(vehicle_path)
            every_neighbors.append(neighbors)
        return every_neighbors

    def tabou(self):
        current_sol = self.random_path()
        if current_sol is None:
            return None
        #print("current",current_sol)
        neighbors = self.generate_all_neighbors(current_sol)
        best_solution = []
        for neighbor in neighbors:
            #print("neighbor :", neighbor)
            sorted_neighbor = sorted(neighbor, key=lambda x: self.calculate_distance([x]))
            best_solution.append(sorted_neighbor[0])
        best_distance = self.calculate_distance(best_solution)
        liste_tabou = [best_solution]
        #print("liste tabou :", best_solution)
        for i in range (self.max_iterations):
            current_solution = self.random_path()
            best_neighbor = []

            for neighbor in neighbors:
                sorted_neighbor = sorted(neighbor, key=lambda x: self.calculate_distance([x]))
                best_neighbor.append(sorted_neighbor[0])
            current_distance = self.calculate_distance(best_solution)
            #print(best_neighbors)
            if best_neighbor not in liste_tabou:
                current_solution = best_neighbor
                current_distance = self.calculate_distance(current_solution)
                if current_distance < best_distance:
                    best_solution = current_solution[:]
                    best_distance = current_distance
                    liste_tabou.append(current_solution)
                if len(liste_tabou) > self.size_tabou:
                    liste_tabou.pop(0)
            #print(f"Iteration {i+1}: Best Distance = {best_distance}")

        final_path = liste_tabou[-1]
        
        return final_path


    def run(self):
        start_time = time.time()
        best_paths = []
        best_distance = np.inf
        best_distance_average_per_vehicles = np.inf
        best_distance_standard_deviation_per_vehicles = np.inf
        best_distance_per_vehicles = []
        best_distance_history = []
        similar_results_count = 0
        for iteration in range(self.max_iterations):
            paths = self.tabou()
            if paths is None:
                break
            total_distance = self.calculate_distance(paths)
            distance_per_vehicules = self.get_distance_per_vehicule(paths)
            if total_distance < best_distance and np.std(distance_per_vehicules) <= best_distance_standard_deviation_per_vehicles:
                best_distance = total_distance
                best_paths = paths
                best_distance_per_vehicles = distance_per_vehicules
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
        self.execution_time = time.time() - start_time




