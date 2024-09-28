from mesa import Agent
from agents.grass import grass
from algoritms.DFS import DFS
from algoritms.BFS import BFS

class bomberman(Agent):
    def __init__(self, unique_id, model, search_type):
        super().__init__(unique_id, model)
        self.first_move = True  # Indica si es el primer movimiento
        self.path = []
        self.search_type = search_type

    def step(self) -> None:
        if self.pos != self.model.goal:
            self.move_towards_goal()

    def move_towards_goal(self) -> None:
        # Sólo calcular el camino si es el primer movimiento
        if self.first_move:
            if self.search_type == "BFS":
                self.path = BFS(self.model.grid, self.pos, self.model.goal)
            elif self.search_type == "DFS":
                self.path = DFS(self.model.grid, self.pos, self.model.goal)
            self.first_move = False

        if self.path:
            new_position = self.path.pop(0)  # Obtén y elimina el siguiente paso
            self.model.grid.move_agent(self, new_position)
            print(f"Me muevo a {new_position}")

            # Verifica si hay un agente 'grass' en la nueva posición
            cell_agents = self.model.grid.get_cell_list_contents([new_position])
            for agent in cell_agents:
                if isinstance(agent, grass):  # Asumiendo que el agente 'grass' se llama 'Grass'
                    agent.visited = 1  # Marca el 'grass' como visitado

        else:
            print("No hay camino disponible o ya se alcanzó la meta.")
