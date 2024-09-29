from mesa import Agent

class bomb(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pd = 1
        self.cooldown = 3