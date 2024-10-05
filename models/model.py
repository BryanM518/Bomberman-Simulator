import mesa
from mesa import Model
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
}

class model(Model):
    def __init__(self, number_of_agents, width, height, map_file, algorithm, priority):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.goal = None
        self.map_file = f"maps/{map_file}"
        self.algorithm = algorithm
        self.priority = priorities[priority]

        # Leer el mapa desde el archivo
        load.load_map(self, self.map_file, algorithm, self.priority)

    def step(self) -> None:
        self.schedule.step()
        
        # Verificar si Bomberman ha llegado a la salida
        if self.newBombermanAgent.pos == self.goal:
            self.running = False