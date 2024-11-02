from mesa import Agent
from agents.grass import grass
from agents.bomb import bomb
from agents.explosion import explosion
from algoritms.BFS import BFS
from algoritms.DFS import DFS
from algoritms.UC import UC
from algoritms.Astar import AStar
from algoritms.HillClimbing import HillClimbing

class bomberman(Agent):
    def __init__(self, unique_id, model, search_type, priority):
        super().__init__(unique_id, model)
        self.first_move = True
        self.path = []
        self.search_type = search_type
        self.priority = priority
        self.waiting_for_explosion = False
        self.rocks = []

    def step(self) -> None:
        if self.pos != self.model.goal:
            self.move_towards_goal()

    def move_towards_goal(self) -> None:
        self.check_explosion_status()
        if self.first_move:
            path_finder = self.get_path_finder()
            if path_finder:
                self.path, self.rocks = path_finder.find_path()
            self.first_move = False
            print("Las rocas encontradas son las siguientes: ", self.rocks)

        if self.path:
            next_position = self.path[0]
            if next_position in self.rocks:
                self.place_bomb(next_position)
            if not self.waiting_for_explosion:
                new_position = self.path.pop(0)
                self.model.grid.move_agent(self, new_position)
                print(f"Me muevo a {new_position}")

                cell_agents = self.model.grid.get_cell_list_contents([new_position])
                for agent in cell_agents:
                    if isinstance(agent, grass):
                        agent.visited = 1 
            else:
                print("Estoy esperando...")
        else:
            self.model.running = False
            
            print("No hay camino disponible o ya se alcanzó la meta.")
    
    def place_bomb(self, next_position):
        self.rocks.remove(next_position)
        bomb_agent = bomb(self.model.schedule.get_agent_count(), self.model, 1, self.pos)
        self.model.schedule.add(bomb_agent)
        self.model.grid.place_agent(bomb_agent, self.pos)
        self.waiting_for_explosion = True

    def check_explosion_status(self):
        bombs = [agent for agent in self.model.schedule.agents if isinstance(agent, bomb)]
        explosions = [agent for agent in self.model.schedule.agents if isinstance(agent, explosion)]
        if not bombs and not explosions:
            print("Bomba explotó, recalculando ruta.")
            self.waiting_for_explosion = False

    def get_path_finder(self):
        if self.search_type == "BFS":
            return BFS(self.model.grid, self.pos, self.model.goal, self.priority)
        elif self.search_type == "DFS":
            return DFS(self.model.grid, self.pos, self.model.goal, self.priority)
        elif self.search_type == "UC":
            return UC(self.model.grid, self.pos, self.model.goal, self.priority)
        elif self.search_type == "A*":
            return AStar(self.model.grid, self.pos, self.model.goal, self.priority)
        elif self.search_type == "Hill Climbing":
            return HillClimbing(self.model.grid, self.pos, self.model.goal, self.priority)
        else:
            print("Tipo de búsqueda no válido.")
            return None
