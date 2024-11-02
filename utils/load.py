from agents.bomberman import bomberman
from agents.salida import salida
from agents.metal import metal
from agents.grass import grass
from agents.rock import rock
from agents.enemy import enemy

class load:
    def load_map(self, map_file, algorithm, priority):
        with open(map_file, "r") as f:
            lines = f.readlines()
            lines = lines[::-1]  # Invertir las líneas para darle vuelta al mapa verticalmente
            self.rocks = []
            
            for y, line in enumerate(lines):
                line = line.strip().split(",")  
                for x, cell in enumerate(line):
                    if cell == "M":
                        wall_agent = metal(self.schedule.get_agent_count(), self)
                        self.schedule.add(wall_agent)
                        self.grid.place_agent(wall_agent, (x, y))
                    else:
                        grass_agent = grass(self.schedule.get_agent_count(), self)
                        self.schedule.add(grass_agent)
                        self.grid.place_agent(grass_agent, (x, y))
                        
                    if cell == "B":
                        bomberman_agent = bomberman(self.schedule.get_agent_count(), self, algorithm, priority)
                        self.schedule.add(bomberman_agent)
                        self.grid.place_agent(bomberman_agent, (x, y))
                        self.newBombermanAgent = bomberman_agent
                    elif cell == "E":
                        enemy_agent = enemy(self.schedule.get_agent_count(), self, priority)
                        self.schedule.add(enemy_agent)
                        self.grid.place_agent(enemy_agent, (x,y))
                    elif cell == "R":
                        rock_agent = rock(self.schedule.get_agent_count(), self)
                        self.schedule.add(rock_agent)
                        self.grid.place_agent(rock_agent, (x,y))
                        self.rocks.append((x,y)) 
                    elif cell == "C_g":
                        goal_agent = salida(self.schedule.get_agent_count(), self)
                        self.schedule.add(goal_agent)
                        self.grid.place_agent(goal_agent, (x, y))
                        self.goal = (x, y)
    
    def get_map_dimensions(map_file):
        with open(map_file, "r") as f:
            lines = f.readlines()
            height = len(lines)  # Número de líneas es la altura
            width = len(lines[0].strip().split(",")) if height > 0 else 0  # Longitud de la primera línea es el ancho
        return width, height
