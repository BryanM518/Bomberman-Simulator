import numpy as np
from algoritms.PathFinder import PathFinder
from algoritms.AllPaths import AllPaths
from algoritms.Astar import AStar
from itertools import product

class MinMaxEnemy(PathFinder):

    def find_path(self, marcadorTurno, alpha, beta, nivel, bomberman_step, max_level, enemies_positions, is_bomberman):
        if bomberman_step == self.goal:
            if is_bomberman:
                return np.inf, bomberman_step
            else:
                return -np.inf, bomberman_step
        
        if bomberman_step in enemies_positions:
            if is_bomberman:
                return np.inf, bomberman_step
            else:
                return -np.inf, bomberman_step

        if nivel == max_level:
            paths = AllPaths(self.grid, bomberman_step, self.goal, self.priority, self.heuristic)
            paths = paths.find_path()
            numpaths = len(paths) * 10
            if not is_bomberman:
                valor = 0
                # Heurística para el enemigo: minimizar la distancia a Bomberman
                for i in enemies_positions:
                    valor += self.manhattan_distance(i, bomberman_step)
                return valor - numpaths, bomberman_step
            else:
                # Heurística para Bomberman: maximizar cercanía a la meta y lejanía de los enemigos
                Astara = AStar(self.grid, bomberman_step, self.goal, self.priority, self.heuristic)
                a, _ = Astara.find_path()
                if a:
                    dist_to_goal = len(a)
                else:
                    dist_to_goal = self.manhattan_distance(bomberman_step, self.goal)
                dist_to_enemies = sum(self.manhattan_distance(bomberman_step, enemy) for enemy in enemies_positions)
                valor = 2*(-dist_to_goal) + 3*dist_to_enemies + 1*numpaths
                return valor, bomberman_step
            #######################################
            # paths = AllPaths(self.grid, bomberman_step, self.goal, self.priority, self.heuristic)
            # paths = paths.find_path()
            # numpaths = len(paths) * 10
            
            # if paths:
            #     dist_to_goal = len(min(paths, key=len)) * 10
            # else:
            #     dist_to_goal = self.manhattan_distance(bomberman_step, self.goal)
            
            # dist_to_enemies = sum(self.manhattan_distance(bomberman_step, enemy) for enemy in enemies_positions)
            # penalization_for_enemies = sum(10 / (self.manhattan_distance(bomberman_step, enemy) + 1) for enemy in enemies_positions)
            
            # if not is_bomberman:
            #     valor = (-dist_to_goal) - (dist_to_enemies) + (numpaths) - penalization_for_enemies
            #     print("Enemigos evaluando: ", numpaths, dist_to_goal, dist_to_enemies, penalization_for_enemies)
            # else:
            #     valor = (-dist_to_goal) + (dist_to_enemies) + (numpaths) - penalization_for_enemies
            #     print("Bomberman evaluando: ", numpaths, dist_to_goal, dist_to_enemies, penalization_for_enemies)
            
            # return valor, bomberman_step


        if marcadorTurno % 2 == 0:
            evalmax = -np.inf
            best_move = None

            possible_steps = self.grid.get_neighborhood(bomberman_step, moore=False, include_center=False)

            for move in possible_steps:
                validacion = self.is_valid_grass_cell(move)
                if validacion:
                    val, _ = self.find_path(marcadorTurno+1, alpha, beta, nivel + 1, move, max_level, enemies_positions, is_bomberman)

                    if val > evalmax:
                        evalmax = val
                        best_move = move
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break

            return evalmax, best_move

        else:
            evalmin = np.inf
            best_move = None
            posibles_combinaciones = []
            posibles_combinaciones = self.calculate_possible_combinations(enemies_positions)

            for move in posibles_combinaciones:
                move = list(move)
                val, _ = self.find_path(marcadorTurno+1, alpha, beta, nivel + 1, bomberman_step, max_level, move, is_bomberman)

                if val < evalmin:
                    evalmin = val
                    best_move = move
                beta = min(beta, val)

                if beta <= alpha:
                    break

            return evalmin, best_move

    def calculate_possible_combinations(self, enemy_steps):
        all_possible_steps = []
        
        for enemy_step in enemy_steps:
            neighbors = self.grid.get_neighborhood(enemy_step, moore=False, include_center=False)
            valid_steps = [step for step in neighbors if self.is_accessible_for_enemy(step)]
            
            if valid_steps:
                all_possible_steps.append(valid_steps)
            else:
                all_possible_steps.append([])

        # Generar todas las combinaciones posibles
        combinations = list(product(*all_possible_steps))

        # Filtrar combinaciones que contienen posiciones repetidas
        unique_combinations = [
            comb for comb in combinations if len(set(comb)) == len(comb)
        ]
        
        return unique_combinations