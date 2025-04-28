from abc import ABC, abstractmethod
import uuid
class AbstractAlgo(ABC):
    def __init__(self,graph, name = None, num_vehicles = 1, min_iterations = 0,max_iterations = 100, convergence_threshold = 5):
        super().__init__()
        self.graph = graph
        self.num_vehicles = num_vehicles
        self.distance = 0
        self.paths = []
        self.distance_history = []
        self.iterations_needed = 0
        self.total_interations_realized = 0
        self.min_iterations = min_iterations
        self.max_iterations = max_iterations # max iterations if the algorithm don't find a solution
        self.convergence_threshold = convergence_threshold # threshold to stop iterations if results are similar
        if name:
            self.name = name
        else:
            self.name = str(uuid.uuid4())

    @abstractmethod
    def run(self):
        pass
