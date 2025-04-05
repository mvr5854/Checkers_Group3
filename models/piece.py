class Piece:
    def __init__(self, player, id, position):
        self.player = player
        self.id = f"{player}{id}"
        self.ix, self.iy = position
        self.cx, self.cy = position
        self.is_king = False

    def is_become_king(self):
        if self.iy <= 2 and self.cy == 7:
            self.is_king = True
        elif self.iy >= 5 and self.cy == 0:
            self.is_king = True

    def available_moves(self):
        moves = []
        if self.iy <= 2 or self.is_king:
            moves.extend([(self.cx + 1, self.cy + 1), (self.cx - 1, self.cy + 1)])
        if self.iy >= 5 or self.is_king:
            moves.extend([(self.cx + 1, self.cy - 1), (self.cx - 1, self.cy - 1)])
        return [self.is_valid_move((x, y)) for x, y in moves if self.is_valid_move((x, y))]
    
    def jump_move(self, move):
        _, x, y = move
        diff_x = x - self.cx
        diff_y = y - self.cy
        return self.is_valid_move((x + diff_x, y + diff_y))

    def is_valid_move(self, move):
        x, y = move
        if x < 0 or x > 7 or y < 0 or y > 7:
            return None
        return (self.id, x, y)

    def move(self, new_position):   
        self.cx, self.cy = new_position
        self.is_become_king()

    def __str__(self):
        return f"Piece {self.id} at ({self.cx}, {self.cy})"
    
    def __repr__(self):
        return f"Piece {self.id} at ({self.cx}, {self.cy})"
