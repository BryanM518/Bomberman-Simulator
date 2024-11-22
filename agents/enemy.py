from mesa import Agent
import numpy as np
from agents.bomberman import bomberman
from algoritms.RandomMove import RandomMove
from algoritms.MinMaxEnemy import MinMaxEnemy

class enemy(Agent):
    def __init__(self, unique_id, model, priority, search_type, heuristic):
        super().__init__(unique_id, model)
        self.priority = priority
        self.search_type = search_type
        self.heuristic = heuristic
    
    def step(self) -> None:
        if self.search_type != "MinMax":
            step = RandomMove(self.model.grid, self.pos, self.model.goal, self.priority, "")
            step = step.find_path()
            self.model.grid.move_agent(self, step)
        
        else:
            minmax = MinMaxEnemy(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
            _, step = minmax.find_path(1, -np.inf, np.inf, 0, self.pos, self.model.newBombermanAgent.pos)
            self.model.grid.move_agent(self, step)
        
        agents_in_cell = self.model.grid.get_cell_list_contents(step)

        for a in agents_in_cell:
            if isinstance(a, bomberman):
                print("Bomberman ha sido derrotado")
                self.model.running = False