import mesa
from mesa import Model
from agents.enemy import enemy
from utils.load import load
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid

priorities = { 
    "← ↓ ↑ →": ["Izquierda", "Abajo", "Arriba", "Derecha"],
    "→ ↓ ↑ ←": ["Derecha", "Abajo", "Arriba", "Izquierda"],
    "→ ↑ ← ↓": ["Derecha", "Arriba", "Izquierda", "Abajo"],
    "↑ → ← ↓": ["Arriba", "Derecha", "Izquierda", "Abajo"],
    "↓ ↑ → ←": ["Abajo", "Arriba", "Derecha", "Izquierda"],
    "↑ ← ↓ →": ["Arriba", "Izquierda", "Abajo", "Derecha"],
    "↓ ← → ↑": ["Abajo", "Izquierda", "Derecha", "Arriba"],
    "← → ↓ ↑": ["Izquierda", "Derecha", "Abajo", "Arriba"],
    "← ↑ → ↓": ["Izquierda", "Arriba", "Derecha", "Abajo"] 
}

class model(Model):
    def __init__(self, number_of_agents, width, height, map_file, algorithm, priority, heuristic, goal_pos):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.goal = None
        self.map_file = f"maps/{map_file}"
        self.algorithm = algorithm
        self.priority = priorities[priority]
        self.heuristic = heuristic

        load.load_map(self, self.map_file, algorithm, self.priority, heuristic, tuple(goal_pos))
        print("La posición de las rocas es la siguiente: ",self.rocks)

    def step(self) -> None:
        self.schedule.step()

        agents_in_cell = self.grid.get_cell_list_contents(self.newBombermanAgent.pos)
        
        for a in agents_in_cell:
            if isinstance(a, enemy):
                print("Bomberman ha sido derrotado")
                self.running = False
        
        if self.newBombermanAgent.pos == self.goal:
            self.running = False