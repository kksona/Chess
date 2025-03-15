class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece is not None

    def is_empty(self):
        return self.piece is None

    def is_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def is_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def is_empty_or_rival(self, color):
        return self.is_empty() or self.is_rival_piece(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True

