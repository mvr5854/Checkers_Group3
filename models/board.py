from models.piece import Piece
import copy

class Board:
    def __init__(self):
        # Create an 8x8 grid of None
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup(["W", "B"])  # Initialize the board with two players
    
    def setup(self, players):
        """
        Place the pieces on the board.
        For this implementation:
          - Pieces for players[1] are placed in the top three rows.
          - Pieces for players[0] are placed in the bottom three rows.
        A counter is used to generate unique IDs for each Piece.
        """
        counters = {players[0]: 1, players[1]: 1}
        # Set up pieces for players[1] (top rows).
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = Piece(players[1], counters[players[1]], (row, col))
                    counters[players[1]] += 1
                    self.grid[row][col] = piece
        # Set up pieces for players[0] (bottom rows).
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = Piece(players[0], counters[players[0]], (row, col))
                    counters[players[0]] += 1
                    self.grid[row][col] = piece

    def copy(self):
        """
        Return a deep copy of the board.
        """
        return copy.deepcopy(self)
    
    def print_board(self, players):
        """
        Print the board in a readable format.
        Empty squares are denoted by '.', while pieces use a letter:
          - Lowercase for normal pieces.
          - Uppercase for kings.
        """
        for row in self.grid:
            line = ""
            for cell in row:
                if cell is None:
                    line += ". "
                else:
                    if cell.player == players[0]:
                        line += ("W " if cell.is_king else "w ")
                    else:
                        line += ("B " if cell.is_king else "b ")
            print(line)