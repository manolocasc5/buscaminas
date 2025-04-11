#Buscaminas:
from cell import Cell
import random

class Board:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        #self.mines_placed = False
        self.place_mines()
        self.calculate_adjacent_mines()

    def place_mines(self):
        # Coloca las minas en el tablero
        positions = [(x, y) for x in range(self.height) for y in range(self.width)]
        mine_positions = random.sample(positions, self.num_mines)
        for x, y in mine_positions:
            self.grid[x][y].set_mine()
        self.mines_placed = True


    def calculate_adjacent_mines(self):
        # Calcula el número de minas adyacentes para cada celda
        for x in range(self.height):
            for y in range(self.width):
                if self.grid[x][y].is_mine:
                    continue
                count = 0
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if self.in_bounds(nx, ny) and self.grid[nx][ny].is_mine:
                            count += 1
                self.grid[x][y].set_adjacent_mines(count)

    
    def reveal_cell(self, x, y):
        #Revela la celda seleccionada y expande si es vacía
        if not self.in_bounds(x, y):
            return
        cell = self.grid[x][y]
        if cell.is_revealed:
            return
        cell.reveal()
        if cell.is_empty() and not cell.is_mine:
            self.reveal_neightbors(x, y)
                
    def reveal_neightbors(self, x, y):
        # Revela recursivamente las celdas adyacentes si la celda es vacía
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if (dx != 0 or dy != 0) and self.in_bounds(nx, ny):
                    neighbor = self.grid[nx][ny]
                    if not neighbor.is_revealed and not neighbor.is_mine:
                        neighbor.reveal()
                        if neighbor.is_empty():
                            self.reveal_neightbors(nx, ny)
    
    def in_bounds(self, x, y):
        # Verifica si las coordenadas están dentro de los límites del tablero
        return 0 <= x < self.height and 0 <= y < self.width
    
    def print_board(self, debug=False):
        # Imprime el tablero en la consola
        print("   " + " ".join(str(i) for i in range(self.width)))
        for i, row in enumerate(self.grid):
            row_str = []
            for cell in row:
                if debug:
                    if cell.is_mine:
                        row_str.append("💣")
                    else:
                        row_str.append(str(cell.adjacent_mines))
                else:
                    row_str.append(str(cell))
            print(f"{i:2} " + " ".join(row_str))

    def is_won(self):
        # Verifica si todas las celdas no-minas han sido reveladas
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
    
    
    
    
    #Podemos añadir un método para comprobar si perdió, pues mostrarle un mensaje