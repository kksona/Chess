import pygame
import pygame as p
import sys
from const import *
from game import *
from square import *
from move import *

class Main:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        p.display.set_caption('Chess')

    def main_loop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        while True:
            game.draw_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.draw_piece(screen)

            if dragger.dragging:
                dragger.update_blit(screen)
            for event in p.event.get():

                #piece selection
                if event.type == pygame.MOUSEBUTTONDOWN:

                    dragger.update_pos(event.pos)

                    clicked_row = dragger.mouseY //SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                    if game.board.squares[clicked_row][clicked_col].has_piece():
                        if game.board.squares[clicked_row][clicked_col].piece.color != game.player and game.player_played:
                            game.next_turn()

                    #check if the clicked square has a piece only if the right player has played
                    if game.board.squares[clicked_row][clicked_col].has_piece():
                        if game.player == game.board.squares[clicked_row][clicked_col].piece.color and not game.player_played:
                            piece = game.board.squares[clicked_row][clicked_col].piece
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                #piece movement (mouse movement)
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_pos(event.pos)
                        game.draw_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.draw_piece(screen)
                        dragger.update_blit(screen)

                #piece release
                elif event.type == pygame.MOUSEBUTTONUP and dragger.piece:
                    if dragger.dragging:
                        dragger.update_pos(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        captured = board.squares[released_row][released_col].has_piece()

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            board.make_move(dragger.piece, move)
                            game.play_sound(captured)
                            game.player_played = True

                            # show methods
                            game.draw_bg(screen)
                            game.draw_piece(screen)

                    dragger.undrag_piece()
                    piece.set_texture(80)

                # key press
                elif event.type == pygame.KEYDOWN:

                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()
                    if event.key == pygame.K_r:
                        game.restart()
                        game = self.game
                        screen = self.screen
                        dragger = self.game.dragger
                        board = self.game.board


                #quit application
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()

            p.display.update()

main = Main()
main.main_loop()