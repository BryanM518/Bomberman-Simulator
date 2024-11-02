from algoritms.PathFinder import PathFinder

class HillClimbing(PathFinder):
    def find_path(self):
        past_step = None
        visited = []
        dict = {0: [(self.start, 1000)]}
        actual_level = 0
        max_level = 0
        last_step_used_by_level = {}
        expanded = []

        while True:
            new_level = []
            actual_steps = dict[actual_level]
            print(f"Para el nivel {actual_level} se obtiene {actual_steps}")

            if actual_steps == []:
                dict.pop(max_level)
                self.came_from.pop(past_step)
                max_level -= 1
                actual_level = min(dict)
                past_step = last_step_used_by_level[actual_level - 1]
            else:
                selected_step = min(actual_steps, key= lambda obj: obj[1])
                self.came_from[selected_step[0]] = past_step
                past_step = selected_step[0]
                print("Nodo seleccionado:", selected_step)
                visited.append(selected_step[0])
                actual_steps.remove(selected_step)

                ## Tener en cuenta
                self.label_grass(selected_step[0])

                if actual_steps == []:
                    dict.pop(actual_level)
                
                if selected_step[0] == self.goal:
                    print("Recorrido encontrado: ")
                    for i in visited:
                        print(i)
                    
                    print("Nivel maximo ", max_level)
                    return self.reconstruct_path(past_step)
                
                
                neighbors = self.grid.get_neighborhood(selected_step[0], moore=False, include_center=False)
                neighbors = self.get_ordered_steps(neighbors, selected_step[0])
                accessible_neighbors = []

                for n in neighbors:
                    if self.is_accessible(n) and n not in visited and n not in expanded:
                        if self.heuristic == "Manhattan":
                            accessible_neighbors.append((n, self.manhattan_distance(n, self.goal)))
                        else:
                            accessible_neighbors.append((n, self.euclidean_distance(n, self.goal)))
                        ##self.label_grass(n)
                        ##expanded.append(n) ## ?????????????
            
                new_level = accessible_neighbors

                last_step_used_by_level[actual_level] = selected_step[0]
                max_level += 1
                actual_level = max_level

                dict[max_level] = new_level