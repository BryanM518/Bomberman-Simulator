from mesa import Agent
from agents.explosion import explosion  

class bomb(Agent):
    def __init__(self, unique_id, model, pd, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.pd = pd
        self.cooldown = pd + 1

    def step(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            print(f"Bomba {self.unique_id} explotó en la posición {self.pos}")

            area = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=True)
            area = self.explosion_area(area)

            for pos in area:
                new_explosion = explosion(self.model.schedule.get_agent_count(), self.model)
                self.model.grid.place_agent(new_explosion, pos)
                self.model.schedule.add(new_explosion)

            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def explosion_area(self, area):
        i = 0
        explosion_area = [self.pos]

        for pos in area:
            if i == 0 and (self.pos[0] > pos[0]):
                explosion_area.append(pos)
            elif i == 1 and (self.pos[1] > pos[1]):
                explosion_area.append(pos)
            elif i == 3 and (self.pos[1] < pos[1]):
                explosion_area.append(pos)
            elif i == 4 and (self.pos[0] < pos[0]):
                explosion_area.append(pos)
            i += 1
        
        return explosion_area