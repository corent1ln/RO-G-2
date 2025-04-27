import networkx as nx
from abc import ABC, abstractmethod
import uuid
import copy
import random

class AbstractGraph(nx.Graph,ABC):
    def __init__(self):
        super().__init__()
        self.id = uuid.uuid4()
        self.blocked_edges = []
        self.costly_edges = []

    @abstractmethod
    def plot_graph(self, best_paths): #todo add show_all_edge boolean
        pass

    def apply_edge_blocking(self,percentage = 20):
        if (percentage < 0):
            percentage = 0
        if (percentage > 100):
            percentage = 100
        if len(self.blocked_edges) > 0:
            self.add_edges_from(self.blocked_edges)
            
        self.blocked_edges = []
        total_edges = list(self.edges(data = True))
        max_removable_edges = len(total_edges) - (len(self.nodes))
        num_edges_to_remove = int(max_removable_edges * (percentage / 100))


        edges = total_edges.copy()
        random.shuffle(edges)

        for u, v, data in edges:
            if num_edges_to_remove == 0:
                break

            if self.degree[u] > 3 and self.degree[v] > 3:
                self.remove_edge(u, v)
                if not nx.is_connected(self):
                    self.add_edge(u,v)
                else :
                    self.blocked_edges.append((u, v,data))
                    num_edges_to_remove -= 1

        print(f"Removed {len(self.blocked_edges)} edges of {len(total_edges)}")


    def apply_edge_costly(self, percentage =20, min_cost_factor = 2, max_cost_factor = 10):
        if (percentage < 0):
            percentage = 0
        if (percentage > 100):
            percentage = 100

        if len(self.costly_edges) > 0:
            for (u,v,data) in self.costly_edges:
                if self.has_edge(u,v):
                    self.edges[(u,v)]["weight"] = data["weight"]
                else:
                    for idx, blocked_edge in enumerate(self.blocked_edges):
                        if (u, v) == (blocked_edge[0], blocked_edge[1]):
                            self.blocked_edges[idx] = (u, v, data)
                            break
            
        self.costly_edges = []
        total_edges = list(self.edges(data = True))
        num_edge_to_cost = int(len(total_edges) * (percentage / 100))


        edges = total_edges.copy()
        random.shuffle(edges)

        for u, v, data in edges:
            if num_edge_to_cost == 0:
                break
            factor = random.randint(min_cost_factor,max_cost_factor)
            self.costly_edges.append((u, v,data))
            self.edges[(u,v)]["weight"] *= factor
            num_edge_to_cost -= 1


        print(f"Costed {len(self.costly_edges)} edges of {len(total_edges)}")