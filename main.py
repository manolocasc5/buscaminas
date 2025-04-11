from game import Game
from board import Board
from cell import Cell

def main():
    width = 10
    height = 10
    num_mines = 10
    size = input("Elige el tamaño del tablero (pequeño, mediano, grande): ").lower()
    if size == "pequeño":
        width, height, num_mines = 5, 5, 5
    elif size == "mediano":
        width, height, num_mines = 10, 10, 10
    elif size == "grande":
        width, height, num_mines = 15, 15, 20
    else:
        width, height, num_mines = 10, 10, 10
        print("Tamaño no válido. Usando tamaño por defecto (10x10).")
    game = Game(width, height, num_mines)
    game.play()

if __name__ == "__main__":
    main()