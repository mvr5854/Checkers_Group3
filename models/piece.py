class Piece:
    def __init__(self, player, id, position):
        self.player = player
        self.id = f"{player}{id}"
        self.ix, self.iy = position
        self.x, self.y = position
        self.is_king = False

    def is_become_king(self):
        if self.iy <= 2 and self.y == 7:
            self.is_king = True
        elif self.iy >= 5 and self.y == 0:
            self.is_king = True

    def available_moves(self):
        moves = []
        if self.iy <= 2 or self.is_king:
            moves.append((self.id, self.x + 1, self.y + 1))
            moves.append((self.id, self.x - 1, self.y + 1))
        if self.iy >= 5 or self.is_king:
            moves.append((self.id, self.x + 1, self.y - 1))
            moves.append((self.id, self.x - 1, self.y - 1))
        return moves

    def move(self, new_position):
        self.x, self.y = new_position
        self.is_become_king()

    def __str__(self):
        return f"Piece {self.id} at ({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Piece {self.id} at ({self.x}, {self.y})"
