from algoritms.PathFinder import PathFinder
import random

class RandomMove(PathFinder):
    def find_path(self):
        current = self.start
        possible_steps = self.grid.get_neighborhood(current, moore=False, include_center=False)
        possible_steps = self.get_ordered_steps(possible_steps, current)
        filtered_steps = []

        for next_pos in possible_steps:
            if self.is_accessible(next_pos):
                filtered_steps.append(next_pos)
        
        step_choice = random.choice(filtered_steps)
        print("El paso elegido", step_choice)

        return step_choice
        

