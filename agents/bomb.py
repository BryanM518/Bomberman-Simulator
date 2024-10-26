from mesa import Agent

class bomb(Agent):
    def __init__(self, unique_id, model, pd):
        super().__init__(unique_id, model)
        self.pd = pd
        self.cooldown = 3