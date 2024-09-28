from mesa.visualization.ModularVisualization import ModularServer
from models.model import model
from agents.bomberman import bomberman
from agents.pared import pared
from agents.salida import salida
from agents.grass import grass
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization import Choice
from utils.load import load
import os
import mesa

MAPS = os.listdir('maps')
NUMBER_OF_CELLS = load.get_map_dimensions("maps/map2.txt")
SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "number_of_agents": 1,
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
    "map_file": Choice(name='map select', description="Selecciona cuál mapa se va jugar", choices=MAPS, value="map1.txt"),
    "algorithm": Choice(name='Método de busqueda', description="Seleccione el método de busqueda para llegar a la meta", choices=["BFS", "DFS"], value="BFS")
}

map_file = simulation_params["map_file"]

def agent_portrayal(agent):
    if isinstance(agent, pared):
        return {"Shape": "images/paredMetal.jpg", "Layer" : 0, "w": 1, "h" : 1}
    elif isinstance(agent, bomberman):
        return {"Shape": "images/bomberman.png", "Layer": 1, "w":1, "h": 1}
    elif isinstance(agent, salida):
        return {"Shape": "images/salida.png", "Layer": 1, "w":1, "h": 1}
    elif isinstance(agent, grass):
        if agent.visited == 0:
            return {"Shape": "images/grass.png", "Layer": 1, "w":1, "h": 1, "text": agent.label, "text_color": "black"}
        if agent.visited == 1:
            return {"Shape": "images/blanco.png", "Layer": 1, "w":1, "h": 1, "text": agent.label, "text_color": "black"}


grid = CanvasGrid(agent_portrayal,
                  NUMBER_OF_CELLS,
                  NUMBER_OF_CELLS,
                  SIZE_OF_CANVAS_IN_PIXELS_X,
                  SIZE_OF_CANVAS_IN_PIXELS_Y
                  )

server = ModularServer(model, [grid], "Bomberman", model_params=simulation_params)
server.port = 8521
server.launch()
