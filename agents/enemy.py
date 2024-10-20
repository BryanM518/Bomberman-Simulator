from mesa import Agent
from agents.bomberman import bomberman
from algoritms.RandomMove import RandomMove

class enemy(Agent):
    def __init__(self, unique_id, model, priority):
        super().__init__(unique_id, model)
        self.priority = priority
    
    def step(self) -> None:
        step = RandomMove(self.model.grid, self.pos, self.model.goal, self.priority)
        step = step.find_path()
        self.model.grid.move_agent(self, step)

        agents_in_cell = self.model.grid.get_cell_list_contents(step)
        
        for a in agents_in_cell:
            if isinstance(a, bomberman):
                print("Bomberman ha sido derrotado")
                self.model.running = False