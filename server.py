import os
import tkinter as tk
from tkinter import filedialog
from mesa.visualization.ModularVisualization import ModularServer
from models.model import model
from agents.bomberman import bomberman
from agents.metal import metal
from agents.salida import salida
from agents.grass import grass
from mesa.visualization.modules import CanvasGrid
from mesa.visualization import Choice
from utils.load import load

root = tk.Tk()
root.withdraw()  

map_file_path = filedialog.askopenfilename(
    initialdir="maps/", title="Seleccione un archivo de mapa", filetypes=[("Text Files", "*.txt")]
)

if not map_file_path:
    print("No se seleccionó ningún archivo de mapa.")
    exit()  

map_file_name = os.path.basename(map_file_path)

height, width = load.get_map_dimensions(f"maps/{map_file_name}")
SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

# Simulation parameters
simulation_params = {
    "number_of_agents": 1,
    "width": width,
    "height": height,
    "map_file": map_file_name,  
    "algorithm": Choice(
        name='Método de búsqueda',
        description="Seleccione el método de búsqueda para llegar a la meta",
        choices=["BFS", "DFS"],
        value="BFS"
    )
}

def agent_portrayal(agent):
    if isinstance(agent, metal):
        return {"Shape": "images/paredMetal.jpg", "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, bomberman):
        return {"Shape": "images/bomberman.png", "Layer": 1, "w": 1, "h": 1}
    elif isinstance(agent, salida):
        return {"Shape": "images/salida.png", "Layer": 1, "w": 1, "h": 1}
    elif isinstance(agent, grass):
        if agent.visited == 0:
            return {"Shape": "images/grass.png", "Layer": 1, "w": 1, "h": 1, "text": agent.label, "text_color": "black"}
        if agent.visited == 1:
            return {"Shape": "images/blanco.png", "Layer": 1, "w": 1, "h": 1, "text": agent.label, "text_color": "black"}

grid = CanvasGrid(agent_portrayal,
                  width,
                  height,
                  SIZE_OF_CANVAS_IN_PIXELS_X,
                  SIZE_OF_CANVAS_IN_PIXELS_Y)


server = ModularServer(model, [grid], "Bomberman", model_params=simulation_params)

server.port = 8521
server.launch()
