# AB step ALGORITHM
from copy import deepcopy as dp
import pygame
import timeit

#PLAYER2 = 'human'
#PLAYER1 = 'ai'

class AI:
    
    def __init__(self):
        print('Opponent online')
    
    def iterative_search(self, board, curr_player, game):
        depth = 3
        maxValue = float('-inf')
        start = timeit.default_timer()
        while timeit.default_timer() - start < 0.7:
            alpha = float('-inf')
            beta = float('inf')
            start_board = dp(board)
            value, new_board = self.step(start_board, depth, curr_player, alpha, beta, game)
            depth += 1
            if value > maxValue:
                next_board = new_board
        return next_board
        
    def step(self, board, depth,curr_player, alpha, beta, game):
        if depth == 0 or board.winner_check() != None:
            return board.evaluate(self, game), board
        
        if curr_player == 'ai':
            board.set_valid_moves('ai')
            maxEval = float('-inf')
            best_board = None
            for new_board in self.get_all_boards(board, 'ai', game):
                evaluation = self.step(new_board, depth - 1, 'human', alpha, beta, game)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_board = new_board
                alpha = max(alpha, maxEval)
                if alpha >= beta:
                    break
            return maxEval, best_board
        else:
            board.set_valid_moves('human')
            minEval = float('inf')
            worst_board = None
            for new_board in self.get_all_boards(board, 'human', game):
                evaluation = self.step(new_board, depth - 1, 'ai', alpha, beta, game)[0]
                minEval = min(minEval,evaluation)
                if minEval == evaluation:
                    worst_board = new_board
                beta = min(beta, minEval)
                if alpha>=beta:
                    break
            return minEval, worst_board
    
    def simulate_move(self, piece, move, board, game, skip):
        board.move(piece, move[0], move[1])
        if skip:
            if any(x.king == True for x in skip):
                piece.make_king()
            board.remove(skip)
        return board
        
    def get_all_boards(self, board, player, game):
        valid_boards = []
        for piece in board.get_all_pieces(player):
            valid_moves = board.valid_moves[piece]
            for move, skip in valid_moves.items():
                temp_board =dp(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, game, skip)
                valid_boards.append(new_board)
        return valid_boards
    