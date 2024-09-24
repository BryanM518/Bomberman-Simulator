from mesa import Agent
from algoritms.BFS import BFS

class bomberman(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self) -> None:
        if self.pos != self.model.goal:
            self.move_towards_goal()

    def move_towards_goal(self) -> None:
        path = BFS(self.model.grid, self.pos, self.model.goal)  # Pasa la cuadrícula como argumento
        if path:
            new_position = path[0]  # Move to the next position in the path
            self.model.grid.move_agent(self, new_position)
            print(f"Me muevo a {new_position}")
