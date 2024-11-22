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

            area = self.explosion_area()

            for pos in area:
                if self.model.grid.out_of_bounds(pos):
                    continue
                new_explosion = explosion(self.model.schedule.get_agent_count(), self.model)
                self.model.grid.place_agent(new_explosion, pos)
                self.model.schedule.add(new_explosion)

            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def explosion_area(self):
        """Calcula el área de explosión basada en el poder de destrucción (pd)."""
        explosion_area = [self.pos]

        for dx in range(1, self.pd + 1):
            explosion_area.append((self.pos[0] + dx, self.pos[1]))
            explosion_area.append((self.pos[0] - dx, self.pos[1]))
        for dy in range(1, self.pd + 1):
            explosion_area.append((self.pos[0], self.pos[1] + dy))
            explosion_area.append((self.pos[0], self.pos[1] - dy))

        return explosion_area
