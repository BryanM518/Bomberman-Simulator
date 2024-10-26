from mesa import Agent
from agents.grass import grass
from algoritms.BFS import BFS
from algoritms.DFS import DFS
from algoritms.UC import UC
from algoritms.Astar import AStar

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
        # Solo calcular el camino si es el primer movimiento
        if self.first_move:
            # Instancia el algoritmo de búsqueda correspondiente
            path_finder = self.get_path_finder()
            if path_finder:
                self.path = path_finder.find_path()
            self.first_move = False

        if self.path:
            new_position = self.path.pop(0)  # Obtén y elimina el siguiente paso
            self.model.grid.move_agent(self, new_position)
            # print(f"Me muevo a {new_position}")

            # Verifica si hay un agente 'grass' en la nueva posición
            cell_agents = self.model.grid.get_cell_list_contents([new_position])
            for agent in cell_agents:
                if isinstance(agent, grass):  # Asumiendo que el agente 'grass' se llama 'Grass'
                    agent.visited = 1  # Marca el 'grass' como visitado
        else:
            self.model.running = False
            print("No hay camino disponible o ya se alcanzó la meta.")

    def get_path_finder(self):
        """Devuelve la instancia del algoritmo de búsqueda correspondiente."""
        if self.search_type == "BFS":
            return BFS(self.model.grid, self.pos, self.model.goal, self.priority)
        elif self.search_type == "DFS":
            return DFS(self.model.grid, self.pos, self.model.goal, self.priority)
        elif self.search_type == "UC":
            return UC(self.model.grid, self.pos, self.model.goal, self.priority)
        elif self.search_type == "A*":
            return AStar(self.model.grid, self.pos, self.model.goal, self.priority)
        else:
            print("Tipo de búsqueda no válido.")
            return None
