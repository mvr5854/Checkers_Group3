import copy

from piece import Piece


class Board():
    def __init__(self, players, to_move):
        # Create an 8x8 grid of None
        self.to_move = to_move
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.players = players
        self.pieces = {players[0]: [], players[1]: []}
        self.setup()  # Initialize the board with two players
    
    def setup(self):
        """
        Place the pieces on the board.
        For this implementation:
          - Pieces for players[1] are placed in the top three rows.
          - Pieces for players[0] are placed in the bottom three rows.
        A counter is used to generate unique IDs for each Piece.
        """
        counters = {self.players[0]: 1, self.players[1]: 1}
        # Set up pieces for players[1] (top rows).
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = Piece(self.players[1], counters[self.players[1]], (row, col))
                    self.pieces[self.players[1]].append(piece)
                    counters[self.players[1]] += 1
                    self.grid[row][col] = piece
        # Set up pieces for players[0] (bottom rows).
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = Piece(self.players[0], counters[self.players[0]], (row, col))
                    self.pieces[self.players[0]].append(piece)
                    counters[self.players[0]] += 1
                    self.grid[row][col] = piece

    def get_piece_by_id(self, piece_id):
        """
        Return the piece object corresponding to the given ID.
        """
        for player in self.pieces.values():
            for piece in player:
                if piece.id == piece_id:
                    return piece
        return None

    def copy(self):
        """
        Return a deep copy of the board.
        """
        return copy.deepcopy(self)
    
    def print_board(self):
        """
        Print the board in a readable format.
        Empty squares are denoted by '.', while pieces use a letter:
          - Lowercase for normal pieces.
          - Uppercase for kings.
        """
        line_num = 0
        horizontal_line = space(5) + "+-----" * 8 + "+"
        print(horizontal_line)

        for row in self.grid:
            line = f"{line_num+1}" + space(3)
            for cell in row:
                line += " | "
                if cell is None:
                    line += space(3)
                else:
                    line += cell.id.upper() if cell.is_king else cell.id
            print(line + " |")
            print(horizontal_line)
            line_num += 1
        
        s = space(5)
        print(f"\n{space(8)}A{s}B{s}C{s}D{s}E{s}F{s}G{s}H\n")

def space(num):
    """
    Return a string of spaces.
    Used for formatting the board output.
    """
    return " " * num