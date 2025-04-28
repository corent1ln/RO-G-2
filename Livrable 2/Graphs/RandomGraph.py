from Graphs.AbstractGraph import AbstractGraph
import random
from utils.plot import Plot

class RandomGraph(AbstractGraph):
    def __init__(self, node_number, min_weight = 1,max_weight = 10):
        super().__init__()
        self.add_nodes_from(range(node_number))
        self.add_edges_from((u, v) for u in range(node_number) for v in range(u + 1, node_number)) 

        # random weight
        for u, v in self.edges():
            self[u][v]['weight'] = random.uniform(min_weight, max_weight)

    def plot_graph(self,best_path = None):
        Plot.plot_graph(self,best_path)
    

    def plot_multiple_paths_on_map(self, best_paths):
        super().plot_multiple_paths_on_map(best_paths)


    def plot_graph(self, best_paths = None):
        if isinstance(best_paths, dict):
            Plot.plot_paths_comparison_graph(self, best_paths)
        else:
              Plot.plot_graph(self, best_paths)
                
        