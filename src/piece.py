import os


class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if self.color == 'white' else -1
        self.value = value_sign * value
        self.moves = [] #a list of Move objects Move(Square(initial_row, initial_col), Square(final_row, final_col))
        self.moved = False #for pawn moves and en_passant
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False
        super().__init__('pawn', color, 1.0)


class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000)


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 10)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5)
