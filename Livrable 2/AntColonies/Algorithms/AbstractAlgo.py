from utils.plot import Plot
from abc import ABC, abstractmethod
class AbstractAlgo(ABC):
    def __init__(self,graph,max_iterations = 100, convergence_threshold = 5):
        super().__init__()
        self.graph = graph
        self.best_distance_history = []  # Store the best distance found in each iteration
        self.max_iterations = max_iterations # max iterations if the algorithm don't find a solution
        self.convergence_threshold = convergence_threshold # threshold to stop iterations if results are similar

    @abstractmethod
    def run(self):
        """
        must return the best path as list and the best distance as float
        """
    def plot_distance_over_iterations(self):
        Plot.plot_distance_over_iterations(self.best_distance_history)
