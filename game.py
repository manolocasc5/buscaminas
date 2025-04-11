from cell import Cell
from board import Board

class Game:
    def __init__(self, width: int, height: int, num_mines: int):
        self.board = Board(width, height, num_mines)
        self.game_over = False
        self.width = width
        self.height = height
        self.num_mines = num_mines

    def make_move(self, x, y, flag=False):
        # Realiza un movimiento en el juego
        if flag:
            if self.board.grid[x][y].is_flagged:
                self.board.grid[x][y].unflag()
                print("Celda desmarcada")
            else:
                self.board.grid[x][y].flag()
                print("Celda maracada con bandera")
        else:
            if self.board.grid[x][y].is_mine:
                print("Perdiste!! Has tocado una mina")
                self.board.print_board(debug=True)
                self.game_over = True
            else:
                self.board.reveal_cell(x, y)
                if self.board.is_won():
                    print("Ganaste!! Has revelado todas las celdas sin minas")
                    self.game_over = True

    def play(self):
        # Inicia el juego
        print("Bienvenido al Buscaminas!")
        while not self.game_over:
            self.board.print_board()
            action = input("Ingresa 'f y 'x para colocar una bandera en la celda (x y), o'x y' para revelar la celda: ").split()
            try:
                if action[0] == 'f':
                    x, y = map(int, action[1:])
                    self.make_move(x, y, flag=True)
                else:
                    x, y = map(int, action)
                    self.make_move(x, y)
            except ValueError:
                print("Entrada inválida. Ingresa dos números.")
            # try:
            #     x, y = map(int, input("Ingresa las coordenadas (x y): ").split())
            #     self.make_move(x, y)
            # except ValueError:
            #     print("Entrada inválida. Ingresa dos números.")

