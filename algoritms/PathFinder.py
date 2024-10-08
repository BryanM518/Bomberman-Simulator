from abc import ABC, abstractmethod
from agents.metal import metal
from agents.grass import grass

class PathFinder(ABC):
    def __init__(self, grid, start, goal, priority):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.priority = priority
        self.came_from = {start: None}
        self.visited = set()
        self.counter = 0

    @abstractmethod
    def find_path(self):
        pass

    def is_accessible(self, position):
        agents_in_cell = self.grid.get_cell_list_contents([position])
        return all(not isinstance(a, metal) for a in agents_in_cell)

    def reconstruct_path(self, current):
        path = []
        while current is not None:
            path.append(current)
            current = self.came_from[current]
        path.reverse()
        return path[1:]

    def label_grass(self, position):
        agents_in_cell = self.grid.get_cell_list_contents([position])
        for agent in agents_in_cell:
            if isinstance(agent, grass):
                agent.label = self.counter
                self.counter += 1

    def get_ordered_steps(self, possible_steps, current):
        new_possible_steps = []
        for i in self.priority:
            if i == "Derecha":
                if current[0] < possible_steps[3][0]:
                    new_possible_steps.append(possible_steps[3])
            elif i == "Izquierda":
                if current[0] > possible_steps[0][0]:
                    new_possible_steps.append(possible_steps[0])
            elif i == "Abajo":
                if current[1] > possible_steps[1][1]:
                    new_possible_steps.append(possible_steps[1])
            elif i == "Arriba":
                if current[1] < possible_steps[2][1]:
                    new_possible_steps.append(possible_steps[2])
        return new_possible_steps
