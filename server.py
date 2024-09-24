from mesa.visualization.ModularVisualization import ModularServer
from models.model import model
from agents.bomberman import bomberman
from agents.pared import pared
from agents.salida import salida
from agents.grass import grass
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization import Choice
from utils.load import load
import mesa

NUMBER_OF_CELLS = load.get_map_dimensions("maps/map2.txt")
SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "number_of_agents": 1,
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
    "map_file": Choice(name='map select', description="Selecciona cuál mapa se va jugar", choices=["Mapa 1 (10x10)", "Mapa 2 (13x13)"], value="Mapa 1 (10x10)")
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
        return {"Shape": "images/grass.png", "Layer": 1, "w":1, "h": 1}


grid = CanvasGrid(agent_portrayal,
                  NUMBER_OF_CELLS,
                  NUMBER_OF_CELLS,
                  SIZE_OF_CANVAS_IN_PIXELS_X,
                  SIZE_OF_CANVAS_IN_PIXELS_Y
                  )

server = ModularServer(model, [grid], "Bomberman", model_params=simulation_params)
server.port = 8521
server.launch()
