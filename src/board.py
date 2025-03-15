from const import *
from square import *
from piece import *
from move import *
import copy

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_board = copy.deepcopy(self)
        temp_piece = copy.deepcopy(piece)
        temp_board.make_move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].is_rival_piece(temp_piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for move in p.moves:
                        if isinstance(move.final.piece, King):
                            return True
        return False

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col] = Square(final.row, final.col, Queen(piece.color))

    def check_en_passant(self, initial, final):
        return abs(initial.row - final.row) == 2


    def make_move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        #pawn promotion or en_passant
        if isinstance(piece, Pawn):
            if self.check_en_passant(initial, final):
                piece.en_passant = True
            else:
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.make_move(rook, rook.moves[-1])

        piece.moved = True

        piece.clear_moves()

        self.last_move = move

    def valid_move(self, piece, move):
        if move in piece.moves:
            return True
        return False

    def calc_moves(self, piece, row, col, bool=True):

        def king_moves():
            adjs = [
                (row - 1, col + 0),  # up
                (row - 1, col + 1),  # up-right
                (row + 0, col + 1),  # right
                (row + 1, col + 1),  # down-right
                (row + 1, col + 0),  # down
                (row + 1, col - 1),  # down-left
                (row + 0, col - 1),  # left
                (row - 1, col - 1),  # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)  # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else: break
                        else:
                            piece.add_move(move)

                # castling moves
                if not piece.moved:
                    # queen castling
                    left_rook = self.squares[row][0].piece
                    if isinstance(left_rook, Rook):
                        if not left_rook.moved:
                            for c in range(1, 4):
                                # castling is not possible because there are pieces in between ?
                                if self.squares[row][c].has_piece():
                                    break

                                if c == 3:
                                    # adds left rook to king
                                    piece.left_rook = left_rook

                                    # rook move
                                    initial = Square(row, 0)
                                    final = Square(row, 3)
                                    moveR = Move(initial, final)

                                    # king move
                                    initial = Square(row, col)
                                    final = Square(row, 2)
                                    moveK = Move(initial, final)

                                    # check potential checks
                                    if bool:
                                        if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                            piece.add_move(moveK)
                                            left_rook.add_move(moveR)
                                    else:
                                        piece.add_move(moveK)
                                        left_rook.add_move(moveR)

                    # king castling
                    right_rook = self.squares[row][7].piece
                    if isinstance(right_rook, Rook):
                        if not right_rook.moved:
                            for c in range(5, 7):
                                # castling is not possible because there are pieces in between ?
                                if self.squares[row][c].has_piece():
                                    break

                                if c == 6:
                                    # adds right rook to king
                                    piece.right_rook = right_rook

                                    # rook move
                                    initial = Square(row, 7)
                                    final = Square(row, 5)
                                    moveR = Move(initial, final)

                                    # king move
                                    initial = Square(row, col)
                                    final = Square(row, 6)
                                    moveK = Move(initial, final)

                                    # check potential checks
                                    if bool:
                                        if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                            piece.add_move(moveK)
                                            right_rook.add_move(moveR)
                                    else:
                                        piece.add_move(moveK)
                                        right_rook.add_move(moveR)



        def knight_moves():
            possible_moves = [
                (row - 2, col - 1),
                (row - 2, col + 1),
                (row + 2, col - 1),
                (row + 2, col + 1),
                (row - 1, col - 2),
                (row - 1, col + 2),
                (row + 1, col - 2),
                (row + 1, col + 2)
            ]
            for possible_move in possible_moves:
                #if in range
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        #create a new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col,final_piece)
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def pawn_moves():
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for moved_row in range(start, end, piece.dir):
                if Square.in_range(moved_row) and self.squares[moved_row][col].is_empty():
                    initial = Square(row, col)
                    final = Square(moved_row, col)
                    move = Move(initial, final)

                    #check potential checks
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                else:
                    break

            #diagonal moves
            capture_row = row + piece.dir
            capture_cols = [col - 1, col + 1]
            for capture_col in capture_cols:
                if Square.in_range(capture_col, capture_row) and self.squares[capture_row][capture_col].is_rival_piece(piece.color):
                    initial = Square(row, col)
                    final_piece = self.squares[capture_row][capture_col].piece
                    final = Square(capture_row, capture_col, final_piece)
                    move = Move(initial, final)
                    # check potential checks
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)


        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        #if empty
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            move = Move(initial, final)
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        #if enemy
                        #add the move and break

                        elif self.squares[possible_move_row][possible_move_col].is_rival_piece(piece.color):
                            move = Move(initial, final)
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break

                        #if team piece then break
                        elif self.squares[possible_move_row][possible_move_col].is_team_piece(piece.color):
                            break
                    else:
                        break

                    possible_move_row += row_incr
                    possible_move_col += col_incr





        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straight_line_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
            ])

        elif isinstance(piece, Rook):
            straight_line_moves([
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ])

        elif isinstance(piece, Queen):
            straight_line_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1) # left
            ])

        elif isinstance(piece, King):
            king_moves()


    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))


        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))