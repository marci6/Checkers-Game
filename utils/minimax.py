# AB step ALGORITHM
from copy import deepcopy as dp
import pygame

#PLAYER2 = 'human'
#PLAYER1 = 'ai'

class AI:
    
    def __init__(self):
        pass
        
    def step(self, board, depth, curr_player, alpha, beta, game):
        # CHECK DEPTH 0
        if depth == 0 or board.winner_check()!= None:
            return board.evaluate(self, game), board
        
        if curr_player == 'ai': # MAXIMIZING PLAYER
            board.set_valid_moves('ai')
            maxEval = float('-inf')
            best_board = None
            for new_board in self.get_all_boards(board, 'ai', game):
                evaluation = self.step(new_board, depth - 1, 'human', alpha, beta, game)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_board = new_board
                # PRUNING
                alpha = max(alpha, maxEval)
                if alpha >= beta:
                    break
            return maxEval, best_board
        else: # MINIMIZING PLAYER 
            board.set_valid_moves('human')
            minEval = float('inf')
            worst_board = None
            for new_board in self.get_all_boards(board, 'human', game):
                evaluation = self.step(new_board, depth - 1, 'ai', alpha, beta, game)[0]
                minEval = min(minEval,evaluation)
                if minEval == evaluation:
                    worst_board = new_board
                # PRUNING
                beta = min(beta, minEval)
                if alpha>=beta:
                    break
            return minEval, worst_board
    
    def simulate_move(self, piece, move, board, game, skip):
        # PERFORME MOVE
        board.move(piece, move[0], move[1])
        if skip:
            if any(x.king == True for x in skip):
                piece.make_king()
            board.remove(skip)
        return board
        
    def get_all_boards(self, board, player, game):
        valid_boards = []
        # GET ALL PIECES
        for piece in board.get_all_pieces(player):
            # GET VALID MOVES FOR A PIECE
            valid_moves = board.valid_moves[piece]
            # SIMULATE EACH MOVE
            for move, skip in valid_moves.items():
                temp_board =dp(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, game, skip)
                valid_boards.append(new_board)
        return valid_boards
    
    
                