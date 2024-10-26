import heapq
from algoritms.PathFinder import PathFinder

class AStar(PathFinder):
    def find_path(self):
        # Inicializa la cola de prioridad con (costo acumulado + heurística, paso inverso, posición)
        queue = [(0, 0, self.start)]
        cost_so_far = {self.start: 0}
        step_counter = 0  # Para controlar el orden de inserción

        while queue:
            current_priority, _, current = heapq.heappop(queue)
            if current == self.goal:
                return self.reconstruct_path(current)

            self.visited.add(current)
            ##self.label_grass(current)

            possible_steps = self.grid.get_neighborhood(current, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, current)
            print(f"Posición actual {current}, Pasos: {ordered_steps}")

            for next_pos in ordered_steps:
                new_cost = cost_so_far[current] + 10
                if next_pos not in self.visited and self.is_accessible(next_pos):
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        step_counter -= 1  # Ahora el paso es negativo, por lo que los nuevos tienen mayor prioridad
                        heuristic = self.manhattan_distance(next_pos, self.goal)
                        priority = new_cost + heuristic
                        heapq.heappush(queue, (priority, step_counter, next_pos))
                        self.label_grass(next_pos)
                        self.came_from[next_pos] = current
                    
                    print(f"Evaluating node {next_pos}, cost: {new_cost}, heuristic: {heuristic}, priority: {priority}")

        return None

    def manhattan_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return (abs(x1 - x2) + abs(y1 - y2)) * 10
