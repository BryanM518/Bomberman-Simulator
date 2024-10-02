from collections import deque
from agents.metal import metal
from agents.grass import grass

def find_path(grid, start, goal):
    queue = deque([start])
    came_from = {start: None}
    visited = set()
    counter = 0

    while queue:
        current = queue.popleft()
        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        agents_in_cell = grid.get_cell_list_contents([current])
        for agent in agents_in_cell:
            if isinstance(agent, grass):
                agent.label = counter
                counter += 1

        possible_steps = grid.get_neighborhood(current, moore=False, include_center=False)
        for next_pos in possible_steps:
            if next_pos not in visited and next_pos not in queue and is_accessible(grid, next_pos):
                queue.append(next_pos)
                came_from[next_pos] = current

    return None

def is_accessible(grid, position):
    # Verifica si la celda está vacía o no contiene una pared
    agent = grid.get_cell_list_contents([position])
    return all(not isinstance(a, metal) for a in agent)

def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path[1:]
