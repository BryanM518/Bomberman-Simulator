import os
import tkinter as tk
from tkinter import filedialog
from mesa.visualization.ModularVisualization import ModularServer
from models.model import model
from agents.bomberman import bomberman
from agents.metal import metal
from agents.salida import salida
from agents.grass import grass
from agents.rock import rock
from agents.enemy import enemy
from mesa.visualization.modules import CanvasGrid
from mesa.visualization import Choice
from utils.load import load

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
MAP_DIR = "maps/"
DEFAULT_ALGORITHM = "BFS"
DEFAULT_PRIORITY = "← ↑ → ↓"

def get_map_file_path():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        initialdir=MAP_DIR, title="Seleccione un archivo de mapa", filetypes=[("Text Files", "*.txt")]
    )


def load_map_dimensions(file_path):
    if not file_path:
        print("No se seleccionó ningún archivo de mapa.")
        exit()
    map_file_name = os.path.basename(file_path)
    width, height = load.get_map_dimensions(f"{MAP_DIR}/{map_file_name}")
    return map_file_name, width, height


def create_simulation_params(width, height, map_file_name):
    return {
        "number_of_agents": 1,
        "width": width,
        "height": height,
        "map_file": map_file_name,
        "algorithm": Choice(
            name='Método de búsqueda',
            description="Seleccione el método de búsqueda para llegar a la meta",
            choices=["BFS", "DFS", "UC"],
            value=DEFAULT_ALGORITHM
        ),
        "priority": Choice(
            name='Prioridad de búsqueda',
            description="Seleccione el orden de prioridad de búsqueda que tendrá el agente",
            choices=[
                "→ ↓ ↑ ←", "→ ↑ ← ↓", "↑ → ← ↓", "↑ ← ↓ →", 
                "↓ ↑ → ←", "↓ ← → ↑", "← → ↓ ↑", "← ↓ ↑ →",
                "← ↑ → ↓"
            ],
            value=DEFAULT_PRIORITY
        )
    }


def agent_portrayal(agent):
    portrayal_map = {
        metal: {"Shape": "images/paredMetal.jpg", "Layer": 0, "w": 1, "h": 1,},
        rock: {"Shape": "images/pared.webp", "Layer": 0, "w": 1, "h": 1,},
        bomberman: {"Shape": "images/agentBomberman.png", "Layer": 1,},
        enemy: {"Shape": "images/enemy.png", "Layer": 1},
        salida: {"Shape": "images/salida.png", "Layer": 1, "w": 1, "h": 1},
        grass: lambda a: {
            "Shape": "images/grass.png" if a.visited == 0 else "images/blanco.png",
            "Layer": 1, "w": 1, "h": 1, "text": a.label, "text_color": "black",
        }
    }

    agent_type = type(agent)
    if agent_type in portrayal_map:
        portrayal = portrayal_map[agent_type]
        return portrayal(agent) if callable(portrayal) else portrayal


map_file_path = get_map_file_path()
map_file_name, width, height = load_map_dimensions(map_file_path)

grid = CanvasGrid(agent_portrayal, width, height, CANVAS_WIDTH, CANVAS_HEIGHT)
simulation_params = create_simulation_params(width, height, map_file_name)
server = ModularServer(model, [grid], "Bomberman", model_params=simulation_params)
server.port = 8521
server.launch()

