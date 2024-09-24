from agents.bomberman import bomberman
from agents.salida import salida
from agents.pared import pared
from agents.grass import grass

class load:
    def load_map(self, map_file):
        with open(map_file, "r") as f:
            for y, line in enumerate(f.readlines()):
                line = line.strip().split(",")  
                for x, cell in enumerate(line):
                    if cell == "M":
                        wall_agent = pared(self.schedule.get_agent_count(), self)
                        self.schedule.add(wall_agent)
                        self.grid.place_agent(wall_agent, (x, y))
                    elif cell != "M":
                        grass_agent = grass(self.schedule.get_agent_count(), self)
                        self.schedule.add(grass_agent)
                        self.grid.place_agent(grass_agent, (x, y))
                        
                    if cell == "B":
                        bomberman_agent = bomberman(self.schedule.get_agent_count(), self)
                        self.schedule.add(bomberman_agent)
                        self.grid.place_agent(bomberman_agent, (x, y))
                        self.newBombermanAgent = bomberman_agent  
                    elif cell == "R":
                        goal_agent = salida(self.schedule.get_agent_count(), self)
                        self.schedule.add(goal_agent)
                        self.grid.place_agent(goal_agent, (x, y))
                        self.goal = (x, y)
    
    def get_map_dimensions(map_file):
        with open(map_file, "r") as f:
            lines = f.readlines()
            height = len(lines) 
        return height