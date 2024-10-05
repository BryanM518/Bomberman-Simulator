from mesa import Agent
from agents.grass import grass
from algoritms import DFS
from algoritms import BFS
from algoritms import UC

class bomberman(Agent):
    def __init__(self, unique_id, model, search_type, priority):
        super().__init__(unique_id, model)
        self.first_move = True  # Indica si es el primer movimiento
        self.path = []
        self.search_type = search_type
        self.priority = priority

    def step(self) -> None:
        if self.pos != self.model.goal:
            self.move_towards_goal()

    def move_towards_goal(self) -> None:
        # Sólo calcular el camino si es el primer movimiento
        if self.first_move:
            if self.search_type == "BFS":
                self.path = BFS.find_path(self.model.grid, self.pos, self.model.goal, self.priority)
            elif self.search_type == "DFS":
                self.path = DFS.find_path(self.model.grid, self.pos, self.model.goal, self.priority)
            elif self.search_type == "UC":
                self.path = UC.find_path(self.model.grid, self.pos, self.model.goal, self.priority)
            self.first_move = False

        if self.path:
            new_position = self.path.pop(0)  # Obtén y elimina el siguiente paso
            self.model.grid.move_agent(self, new_position)
            ##print(f"Me muevo a {new_position}")

            # Verifica si hay un agente 'grass' en la nueva posición
            cell_agents = self.model.grid.get_cell_list_contents([new_position])
            for agent in cell_agents:
                if isinstance(agent, grass):  # Asumiendo que el agente 'grass' se llama 'Grass'
                    agent.visited = 1  # Marca el 'grass' como visitado
        else:
            self.model.running = False
            print("No hay camino disponible o ya se alcanzó la meta.")
