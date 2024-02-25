# Diego Alejandro Michel Castro | A01641907
# 23/02/2024
# Definición de un sistema multiagentes para la resolución de un problema de limpieza

import agentpy as ap
import random

#  ----------- Definición del agente para problema a resolver ------------------

class CleaningAgent(ap.Agent):

    def setup(self):
        self.pos = [1, 1]   # Establecer una posición inicial
        self.movements = 0  # Inicializar contador de movimientos

    def step(self):
        x, y = self.pos
        has_moved = False  # Variable para controlar si el agente ha realizado un movimiento exitoso
        moves = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)]
        random.shuffle(moves)  # Aleatorizar el orden de los movimientos
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.model.width and 0 <= new_y < self.model.height:
                if self.model.grid[new_y][new_x]:  # Si la celda está sucia
                    self.model.grid[new_y][new_x] = False  # Limpiar la celda
                    print(f"El agente en posicion {self.pos} limpio una celda en [{new_x}, {new_y}]. {self.model.dirty_boxes} celdas restantes.")
                    has_moved = True
                self.pos = [new_x, new_y]  # Mover a la nueva posición
                self.movements += 1  # Incrementar el contador de movimientos
                if has_moved:  # Si el agente ha realizado un movimiento exitoso, salir del bucle
                    break
        self.model.dirty_boxes = sum(sum(row) for row in self.model.grid)  # Actualizar recuento de celdas sucias


# ------------ Definición del ambiente/modelo a trabajar --------------

class CleaningModel(ap.Model):

    def setup(self):
        self.width = 20  # Establecemos el tamaño de la habitación
        self.height = 20
        self.dirty_percentage = 0.3  # Establecemos el porcentaje de celdas sucias
        self.grid = [[False] * self.width for _ in range(self.height)]  # Inicializar todas las celdas como limpias
        self.agents = [CleaningAgent(self) for _ in range(parameters["n_agents"])]
        self.dirty_boxes = int(self.dirty_percentage * self.width * self.height)
        for _ in range(self.dirty_boxes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.grid[y][x] = True  # Establecer celdas aleatorias como sucias

    def step(self):
        for agent in self.agents:
            agent.step()

    def run(self, max_time):
        self.setup()
        time_elapsed = 0  # Inicializar el tiempo transcurrido de la simulación
        while time_elapsed < max_time and self.dirty_boxes > 0:
            self.step()
            time_elapsed += 1  # Modificador para el temporizador
        self.calculate_results(time_elapsed) 

    def calculate_results(self, time_elapsed):
        # Calcular y mostrar los resultados al final de la simulación
        clean_percentage = (sum(row.count(False) for row in self.grid) / (self.width * self.height)) * 100
        total_movements = sum(agent.movements for agent in self.agents) 
        print(f"Porcentaje de celdas limpias: {clean_percentage}%")
        print(f"Numero total de movimientos realizados por todos los agentes: {total_movements}")
        print(f"Tiempo necesario hasta que todas las celdas estén limpias o se haya llegado al tiempo máximo: {time_elapsed}")


# --------- Ejecución --------------

parameters = {    # Diccionario de parámetros a usar en la simulación
    "n_agents": 100,
    "steps": 1000,
    "max_time": 100000  # Definir el tiempo máximo deseado
}

model = CleaningModel(parameters)
model.run(max_time=parameters["max_time"])
