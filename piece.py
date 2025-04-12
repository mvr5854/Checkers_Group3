class Piece:
    def __init__(self, player, id, position):
        self.player = player
        self.id = f"{player}0{id}" if id < 10 else f"{player}{id}"
        self.iy, self.ix = position
        self.cy, self.cx = position
        self.is_king = False

    def is_become_king(self):
        if self.iy <= 2 and self.cy == 7:
            self.is_king = True
        elif self.iy >= 5 and self.cy == 0:
            self.is_king = True

    def available_moves(self):
        moves = []
        if self.iy <= 2 or self.is_king:
            moves.extend([(self.cy + 1, self.cx - 1), (self.cy + 1, self.cx + 1)])
        if self.iy >= 5 or self.is_king:
            moves.extend([(self.cy - 1, self.cx - 1), (self.cy - 1, self.cx + 1)])
        return [self.is_valid_move((y, x)) for y, x in moves if self.is_valid_move((y, x))]
    
    def jump_move(self, move):
        _, y, x = move
        diff_x = x - self.cx
        diff_y = y - self.cy
        return self.is_valid_move((y + diff_y, x + diff_x))

    def is_valid_move(self, move):
        y, x = move
        if x < 0 or x > 7 or y < 0 or y > 7:
            return None
        return (self.id, y, x)

    def move(self, new_position):   
        self.cy, self.cx = new_position
        self.is_become_king()

    def __str__(self):
        return f"Piece {self.id} at ({self.cy}, {self.cx})"
    
    def __repr__(self):
        return f"Piece {self.id} at ({self.cy}, {self.cx})"
