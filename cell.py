#Buscaminas:

class Cell:
    #is_mine: si tiene una mina (booleano)
    #is_revealed: si se ha clicado en la celda (booleano)
    #adjacent_mines: las minas adyacentes (int)
    def __init__(self, is_mine = False, is_revealed= False, adjacent_mines = 0, is_flagged= False):
        self.is_mine = is_mine
        self.is_revealed = is_revealed
        self.adjacent_mines = adjacent_mines
        self.is_flagged = is_flagged

    def reveal(self):
        #revela la celda
        self.is_revealed = True

    def set_mine(self):
        #coloca una mina en la celda
        self.is_mine = True

    def set_adjacent_mines(self, adjacent_mines: int):
        #coloca el numero de minas adyacentes
        self.adjacent_mines = adjacent_mines

    def is_empty(self):
        #si la celda no tiene mina
        return self.adjacent_mines == 0
    
    def flag(self):
        #marca la celda
        self.is_flagged = True

    def unflag(self):
        #desmarca la celda
        self.is_flagged = False
    
    def __str__(self):
        #devuelve el string de la celda
        if self.is_flagged:
            return "🚩"
        elif not self.is_revealed:
            return "#" #añadir emoticonos
        elif self.is_mine:
            return "💣" #añadir emoticonos
        elif self.adjacent_mines > 0:
            return str(self.adjacent_mines)
        else:
            return " "
        
