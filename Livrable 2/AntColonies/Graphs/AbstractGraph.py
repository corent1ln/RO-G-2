import networkx as nx
from abc import ABC, abstractmethod
class AbstractGraph(nx.Graph,ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def plot_graph(self,path):
        pass