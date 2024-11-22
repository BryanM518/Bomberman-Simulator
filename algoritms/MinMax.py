
import numpy as np
from algoritms.PathFinder import PathFinder

class MinMax(PathFinder):

    def find_path(self, marcadorTurno, alpha, beta, nivel, enemy_step, bomberman_step):

        if enemy_step == bomberman_step:
            return 0, bomberman_step

        if nivel == 6:
            if self.heuristic == "Manhattan":
                ##valor = self.manhattan_distance(self.goal, bomberman_step)
                print(f"Valor: {valor}, en la posición de enemigo: {enemy_step} y posición de bomberman: {bomberman_step}")
                return valor, bomberman_step
            else:
                valor = self.euclidean_distance(self.goal, bomberman_step)
                return valor, bomberman_step
        
        if marcadorTurno % 2 == 0:
            evalmax = -np.inf
            best_move = None

            possible_steps = self.grid.get_neighborhood(bomberman_step, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, bomberman_step)

            for move in ordered_steps:
                if self.is_accessible(move):
                    val, _ = self.find_path(marcadorTurno+1, alpha, beta, nivel + 1, enemy_step, move)

                    if val > evalmax:
                        evalmax = val
                        best_move = move
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break

            return evalmax, best_move
        
        elif marcadorTurno % 2 != 0:
            evalmin = np.inf
            best_move = None

            possible_steps = self.grid.get_neighborhood(enemy_step, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, enemy_step)

            for move in ordered_steps:
                if self.is_accessible(move):
                    val, _ = self.find_path(marcadorTurno+1, alpha, beta, nivel + 1, move, bomberman_step)

                    if val < evalmin:
                        evalmin = val
                        best_move = move
                    beta = min(beta, val)

                    if beta <= alpha:
                        break
            
            return evalmin, best_move
