import numpy as np
# Ant class represents an individual ant that travels across the graph
class Ant:
    def __init__(self, graph, aco):
        self.graph = graph
        self.aco = aco
        self.start_node = list(graph.nodes)[0]
        self.current_nodes = [self.start_node for _ in range(self.aco.num_vehicles)]
        self.paths = [[self.start_node] for _ in range(self.aco.num_vehicles)]
        self.distances_per_vehicles = [0 for _ in range(self.aco.num_vehicles)]
        self.total_distance = 0  # Start with zero distance traveled
        self.unvisited_nodes = list(self.graph.nodes).copy()
        self.unvisited_nodes.remove(self.start_node) # remove the initial node because the ant start on it

    def select_vehicle(self):
        return np.random.randint(0, self.aco.num_vehicles)
    # Select the next node for the ant to travel to, based on pheromones and distances
    def select_next_node(self,current_node):
        # Initialize an array to store the probability for each node
        probabilities = dict()
        # For each unvisited node, calculate the probability based on pheromones and distances                    
        for neighbor in self.graph.neighbors(current_node):
            if  neighbor in self.unvisited_nodes:  # Only consider reachable nodes
                pheromone = self.aco.get_pheromone(current_node, neighbor)
                distance = self.graph[current_node][neighbor]['weight']
                # The more pheromones and the shorter the distance, the more likely the node will be chosen
                probabilities[neighbor] = (pheromone ** 2) / distance
        
        # Safeguard against division by zero
        total_prob = sum(probabilities.values())
        if total_prob == 0:
            # If all probabilities are zero, choose randomly among unvisited reachable nodes
            reachable_unvisited = [
                neighbor for neighbor in self.graph.neighbors(current_node)
                if neighbor in self.unvisited_nodes
            ]
            if reachable_unvisited:
                next_node = np.random.choice(reachable_unvisited)
            else:
                next_node = None
        else:
            # Normalize the probabilities to sum to 1
            probabilities = {node: prob / total_prob for node, prob in probabilities.items()}
            # Choose the next node based on the calculated probabilities
            next_node = np.random.choice(
                list(probabilities.keys()), p=list(probabilities.values())
            )
        
        return next_node

    # Move to the next node and update the ant's path
    def move(self):
        vehicle = self.select_vehicle()
        current_node = self.current_nodes[vehicle]
        next_node = self.select_next_node(current_node)  # Pick the next node
        if next_node is None:
            return False
        
        self.paths[vehicle].append(next_node)  # Add it to the path
        # Add the distance between the current node and the next node to the total distance
        self.total_distance += self.graph[self.current_nodes[vehicle]][next_node]["weight"]
        self.distances_per_vehicles[vehicle]+= self.graph[self.current_nodes[vehicle]][next_node]["weight"]
        self.current_nodes[vehicle] = next_node  # Update the current node to the next node
        self.unvisited_nodes.remove(next_node)  # Mark the next node as visited
        return True

    # Complete the path by visiting all nodes and returning to the starting node
    def complete_path(self):
        while self.unvisited_nodes:  # While there are still unvisited nodes
            if not self.move():
                break  # If ant blocked
        for i in range(self.aco.num_vehicles):
            if not self.unvisited_nodes:
                if self.graph.has_edge(self.current_nodes[i], self.start_node):
                    # After visiting all nodes, return to the starting node to complete the cycle
                    self.total_distance += self.graph[self.current_nodes[i]][self.start_node]["weight"]
                    self.paths[i].append(self.start_node)  # Add the starting node to the end of the path
                    self.distances_per_vehicles[i]+= self.graph[self.current_nodes[i]][self.start_node]["weight"]
