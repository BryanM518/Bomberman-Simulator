import mesa
from mesa import Model
from utils.load import load
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid

mapas = {
    "Mapa 1 (10x10)": "map1.txt",
    "Mapa 2 (13x13)": "map2.txt"
}


class model(Model):

    def __init__(self, number_of_agents, width, height, map_file):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.goal = None
        self.map_file = f"maps/{mapas[map_file]}"

        # Leer el mapa desde el archivo
        load.load_map(self, self.map_file)

    def step(self) -> None:
        self.schedule.step()
        
        # Verificar si Bomberman ha llegado a la salida
        if self.newBombermanAgent.pos == self.goal:
            self.running = False