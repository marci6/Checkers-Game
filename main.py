# CHECKERS

import pygame
from pygame import mixer
from utils.minimax import AI
from utils.minimax_iter import AI as AI_iter
from utils.menu import MainMenu, OptionsMenu, CreditsMenu
from copy import deepcopy as dp
# CONSTANTS
WIDTH, HEIGHT = 800,800
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH//COLS
# COLORS
GREEN = (60, 207, 143)
PLAYER2 = 'human'
PLAYER1 = 'ai'
BLUE = (0,0,255)
GREY = (200,200,200)
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (224, 110, 108)

FPS = 60
VOLUME = 0.5
DEPTH = 4
ITERATIVE_DP = True
# LOAD UTILITIES
KING1 = pygame.transform.scale(pygame.image.load('assets/checker1_king.png'), (70,70))
KING2 = pygame.transform.scale(pygame.image.load('assets/checker2_king.png'), (70,70))
PIECE1 = pygame.transform.scale(pygame.image.load('assets/checker1.png'), (70,70))
PIECE2 = pygame.transform.scale(pygame.image.load('assets/checker2.png'), (70,70))

pygame.init()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Checkers')
background = mixer.Sound('assets/music_background.mp3')
tense = mixer.Sound('assets/tense.mp3')

#AI OPPONENT INSTANTIATION
if ITERATIVE_DP:
    opponent = AI_iter()
else:
    opponent = AI()
    
    
class Game:
    def __init__(self,win):
        self.selected = 0 # SELECTED PIECE
        self.board = Board()
        self.turn = PLAYER2
        self.valid_moves = {} #DICTIONARY OF VALID MOVES FOR SELECTED PIECE
        self.win = win
        # menu
        self.cleverness = 'Advance'
        self.music = ['Off','Game']
        self.Hints='On'
        self.game_on = False
        self.running = True
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.font_name = 'assets/font.TTF'
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.menu = MainMenu(self)
        
    def update(self):
        self.board.draw(self.win)
        # draw selected
        if self.selected!=0 and self.selected!=None:
            pygame.draw.rect(self.win, RED, (self.selected.col*SQUARE_SIZE, self.selected.row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            self.selected.draw(self.win)
            if self.Hints == 'On':
                self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        
    def reset(self):
        self.selected = None
        self.board = Board()
        self.turn = PLAYER2
        self.valid_moves = {}
        
    def select(self, row, col):
        # IF A PIECE IS SELECTED BY THE CURRENT PLAYER
        if self.selected:
            # CHECK VALIDITY MOVE
            result = self._move(row, col)
            if not result: # MOVE NOT VALID
                self.selected = None # reset
                self.select(row, col) # repeat
        # IF A PIECE IS NOT SELECTED BY THE CURRENT PLAYER
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.player == self.turn: # VALIDITY
            self.selected = piece
            self.valid_moves = self.board.valid_moves[piece]
            return True
        return False
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row,col) in self.valid_moves:
            # PERFORM MOVE
            self.board.move(self.selected, row, col)
            captured = self.valid_moves[(row, col)]
            if captured:
                self.board.remove(captured, selected = self.selected)
            self.change_turn()
        else:
            return False
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col*SQUARE_SIZE+SQUARE_SIZE//2, row*SQUARE_SIZE+SQUARE_SIZE//2), 15)
            
    def change_turn(self):
        self.valid_moves={}
        if self.turn == PLAYER2:
            self.turn = PLAYER1
        else:
            self.turn = PLAYER2
    
    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.change_turn()
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.game_on = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        
    def draw_text(self, text, size, x, y, color_text=WHITE ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color_text)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.win.blit(text_surface,text_rect)
        
    def set_music(self, background, tense):
        if self.music[0] == 'Off':
            background.set_volume(0)
            tense.set_volume(0)
        elif self.music[1] == 'On':
            if self.music == 'Game':
                background.set_volume(VOLUME)
                tense.set_volume(0)
            else:
                tense.set_volume(VOLUME)
                background.set_volume(0)
        
class Piece:
    PADDING = 15
    OUTLINE = 2
    def __init__(self,row,col, player):
        self.row = row
        self.col = col
        self.player = player
        self.king = False
        if self.player == PLAYER2:
            self.direction = -1
        else:
            self.direction = 1
            
        self.x = 0
        self.y = 0
        self.calc_pos()
        
    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row + SQUARE_SIZE//2
        
    def make_king(self):
        self.king = True

    def draw(self,win):
        if self.player == PLAYER1:
            win.blit(PIECE1, (self.x-PIECE1.get_width()//2, self.y-PIECE1.get_height()//2))
        else:
            win.blit(PIECE2, (self.x-PIECE2.get_width()//2, self.y-PIECE2.get_height()//2))
        if self.king and self.player == PLAYER1:
            win.blit(KING1, (self.x-KING1.get_width()//2, self.y-KING1.get_height()//2))
        elif self.king and self.player == PLAYER2:
            win.blit(KING2, (self.x-KING2.get_width()//2, self.y-KING2.get_height()//2))
    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
        
# class defining the board state
class Board:
    def __init__(self):
        self.board = [] # contains the rows
        self.PLAYER1_left = self.PLAYER2_left = 12 # pieces per player
        self.PLAYER1_kings = self.PLAYER2_kings = 0 # kings per player
        self.PLAYER1_safe = self.PLAYER2_safe = 3 # pieces on the edge
        self.PLAYER1_safekings = self.PLAYER2_safekings = 0 # king on the edge
        self.PLAYER1_dist = self.PLAYER2_dist = 72 # summed distance from promotion line
        self.PLAYER1_back = self.PLAYER2_back = 12 # pieces on first 3 rows
        self.PLAYER1_mid = self.PLAYER2_mid = 0 # pieces in the centre
        self.PLAYER1_vul = self.PLAYER2_vul = 0 # vulnerable pieces
        self.valid_moves = {}
        self.create_board()
        
    def draw_squares(self,win):
        win.fill(GREEN)
        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(win, GREY, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        if row == ROWS -1 or row == 0:
            if piece.player == PLAYER1 and piece.king is False:
                self.PLAYER1_kings+=1
            if piece.player == PLAYER2 and piece.king is False:
                self.PLAYER2_kings+=1
            piece.make_king()
                
    def remove(self, pieces, selected=None):
        for piece in pieces:
            if piece != 0:
                # Regicide
                if piece.king==True and selected != None:
                    selected.make_king()
                if piece.player == PLAYER2:
                    self.PLAYER2_left-=1
                else:
                    self.PLAYER1_left-=1
                self.board[piece.row][piece.col] = 0
                    
    def winner_check(self):
        if self.PLAYER2_left<=0:
            return PLAYER1
        if self.PLAYER1_left<=0:
            return PLAYER2
        return None
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def create_board(self):
        for row in range(ROWS): # adds rows
            self.board.append([])
            for col in range(COLS): # adds pieces
                # if the col is equal to the row plus/minus 1 (even odd columns)
                if col%2 == ((row+1)%2):
                    if row < 3: # adds PLAYER1
                        self.board[row].append(Piece(row,col, PLAYER1))
                    elif row > 4: # adds PLAYER2
                        self.board[row].append(Piece(row,col, PLAYER2))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
                    
    def draw(self, win):
        # draw board
        self.draw_squares(win)
        # draw pieces
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def get_valid_moves(self, piece):
        moves = {}
        left_col = piece.col - 1
        right_col = piece.col + 1
        row = piece.row
        if piece.player == PLAYER2 or piece.king:
            moves.update(self._move_left(row -1, max(row-3, -1), -1, piece.player, left_col, piece.king))
            moves.update(self._move_right(row -1, max(row-3, -1), -1, piece.player, right_col, piece.king))
        if piece.player == PLAYER1 or piece.king:
            moves.update(self._move_left(row +1, min(row+3, ROWS), 1, piece.player, left_col, piece.king))
            moves.update(self._move_right(row +1, min(row+3, ROWS), 1, piece.player, right_col, piece.king))
        return moves

    def _move_left(self, start, stop, dn, player, left, is_king, captured=[]):
        moves = {} # list of all possible moves on left diagonal
        jumped = [] 
        for r in range(start, stop, dn):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0: # if left diag is free
                if captured and not jumped: # not valid second jump
                    break
                elif captured:
                    moves[(r, left)] = jumped + captured
                else:
                    moves[(r, left)] = jumped
                
                if jumped:
                    if dn == -1: # PLAYER2 is moving
                        row = max(r-3, -1)
                    else: # PLAYER1 is moving
                        row = min(r+3, ROWS)
                    moves.update(self._move_left(r+dn, row, dn, player, left-1,is_king,captured=jumped))
                    moves.update(self._move_right(r+dn, row, dn, player, left+1,is_king,captured=jumped))
                    
                break
            elif current.player == player:
                break
            else: # jump over and capture
                jumped = [current] # jumped moves

            left -= 1
        
        return moves

    def _move_right(self, start, stop, dn, player, right, is_king, captured=[]):
        moves = {} # list of all possible moves on right diagonal
        jumped = []
        for r in range(start, stop, dn):
            if right >= COLS:
                break
            # GET THE SQUARE ON THE BOARD
            current = self.board[r][right]
            # IF IT'S FREE
            if current == 0:
                # CHECK CONDITION FOR DOUBLE JUMP => TWO PIECES MUST BE CAPTURED
                if captured and not jumped:
                    break
                # ADD DOUBLE JUMP
                elif captured:
                    moves[(r,right)] = jumped + captured
                # FIRST FREE SQUARE OR ONE JUMP/CAPTURE
                else:
                    moves[(r, right)] = jumped
                # CHECK IF CAN DOUBLE JUMP
                if jumped:
                    if dn == -1: # player 2
                        row = max(r-3, -1)
                    else: # player 1
                        row = min(r+3, ROWS)
                    # REPEAT TO CHECK FOR DOUBLE JUMPS
                    moves.update(self._move_left(r+dn, row, dn, player, right-1,is_king, captured=jumped))
                    moves.update(self._move_right(r+dn, row, dn, player, right+1, is_king, captured=jumped))

                    
                break
            # IF IT'S OCCUPIED BY THE SAME PLAYER
            elif current.player == player:
                break
            # IF IT'S OCCUPIED BY THE OPPONENT
            else:
                # SAVE TO CHECK DOUBLE JUMP
                jumped = [current]

            right += 1
        
        return moves
    
    def set_valid_moves(self, player):
        only_capture = {}
        all_moves = {}
        flag = False
        # get all possible moves on the board
        for piece in self.get_all_pieces(player): # for all pieces
            possible_moves = self.get_valid_moves(piece)
            all_moves[piece] = possible_moves
            # check if there are jumps
            temp_dict = {}
            for move, jump in possible_moves.items():
                if jump:
                    temp_dict[move] = jump
                    flag = True
            only_capture[piece] = temp_dict
        # IF THERE ARE POSSIBLE CAPTURES
        if flag:
            self.valid_moves = only_capture
        else:
            self.valid_moves = all_moves
    
    def evaluate(self, opponent, game):
        # score of the board
        if game.cleverness == 'Beginner':
            score = self.PLAYER1_left - self.PLAYER2_left + (self.PLAYER1_kings*0.5 - self.PLAYER2_kings*0.5)
        elif game.cleverness == 'Medium':
            score = self.PLAYER1_left - self.PLAYER2_left + (self.PLAYER1_kings*0.5 - self.PLAYER2_kings*0.5) + (0.5*self.PLAYER1_vul-0.5*self.PLAYER2_vul)
        else:
            score = self.score_players(opponent, game)
        return score
    
    def score_players(self, opponent, game):
        # back pieces
        self.PLAYER1_back = 0
        self.PLAYER2_back = 0
        for c in range(0,COLS):
            piece = self.get_piece(0, c)
            if piece == 0:
                continue
            if piece.player == PLAYER1:
                self.PLAYER1_back += 1
            elif piece.player == PLAYER2:
                self.PLAYER2_back += 1
        # centre pieces
        self.PLAYER1_mid = 0
        self.PLAYER2_mid = 0
        for r in range(3,5):
            for c in range(2,COLS-2):
                piece = self.board[r][c]
                if piece == 0:
                    continue
                if piece.player == PLAYER1:
                    self.PLAYER1_mid+=1
                elif piece.player == PLAYER2:
                    self.PLAYER2_mid+=1
        # safe pieces
        self.PLAYER1_safe = 0
        self.PLAYER2_safe = 0
        for r in range(0,ROWS):
            for c in [0,COLS-1]:
                piece = self.board[r][c]
                if piece == 0:
                    continue
                if piece.player == PLAYER1:
                    self.PLAYER1_safe += 1
                elif piece.player == PLAYER2:
                    self.PLAYER2_safe += 1
        # safe kings
        self.PLAYER1_safekings = 0
        self.PLAYER2_safekings = 0
        for r in range(0,ROWS):
            for c in [0,COLS-1]:
                piece = self.board[r][c]
                if piece == 0:
                    continue
                if piece.player == PLAYER1 and piece.king:
                    self.PLAYER1_safekings+=1
                elif piece.player == PLAYER2 and piece.king:
                    self.PLAYER2_safekings+=1
        # distance
        self.PLAYER1_dist = 0
        self.PLAYER2_dist = 0
        for r in range(0,ROWS):
            for c in range(0,COLS):
                piece = self.board[r][c]
                if piece == 0:
                    continue
                if piece.player == PLAYER1 and piece.king == False:
                    self.PLAYER1_dist+= COLS - 1 - c
                elif piece.player == PLAYER2 and piece.king == False:
                    self.PLAYER2_dist+= c
        # vulnerable pieces
        self.PLAYER1_vul = 0
        self.PLAYER2_vul = 0
        self.set_valid_moves(PLAYER1)
        for move in opponent.get_all_boards(self, PLAYER1, game):
            self.PLAYER1_vul += self.PLAYER1_left - move.PLAYER1_left
        self.set_valid_moves(PLAYER2)
        for move in opponent.get_all_boards(self, PLAYER2, game):
            self.PLAYER2_vul += self.PLAYER2_left - move.PLAYER2_left
                
        score_PLAYER1 = 7*self.PLAYER1_left + 7.75*self.PLAYER1_kings + 4*self.PLAYER1_back + 2.5*self.PLAYER1_mid - 0.5*self.PLAYER1_safe - 0.7*self.PLAYER1_safekings - 0.06*self.PLAYER1_dist + 3*self.PLAYER1_vul 
        score_PLAYER2 = 7*self.PLAYER2_left + 7.75*self.PLAYER2_kings + 4*self.PLAYER2_back + 2.5*self.PLAYER2_mid - 0.5*self.PLAYER2_safe - 0.7*self.PLAYER2_safekings - 0.06*self.PLAYER2_dist + 3*self.PLAYER2_vul
        score = score_PLAYER1 - score_PLAYER2
        return score
    
    def get_all_pieces(self, player):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece!=0 and piece.player == player:
                    pieces.append(piece)
        return pieces
    
    def check_stalemate(self, game): 
        flag = True
        for _, move in self.valid_moves.items():
            if move:
                flag = False
        return flag
    
def stalemate_display(win,game):
    game.game_on=False
    win.fill(BLACK)
    game.draw_text('Game reached a state of stalemate', 20, WIDTH/2, HEIGHT/2)
    win.blit(win, (0,0))
    pygame.display.update()

def winner_display( winner, win, game):
        game.game_on=False
        if winner == PLAYER1:
            winner_name = 'Player 1'
        else:
            winner_name = 'Player 2'
        win.fill(BLACK)
        text = winner_name + ' won the game*Congratulations*'
        game.draw_text(text, 20, WIDTH/2, HEIGHT/2)
        win.blit(win, (0,0))
        pygame.display.update()
        
def get_mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def play_game(game, clock):
    # LOOP WHILE PLAYING
    while game.game_on:
        clock.tick(FPS)
        # set valid moves
        game.board.set_valid_moves(game.turn)
        # check for a winner
        if game.board.winner_check()!= None:
            game.game_on = False
            winner_display(game.board.winner_check(), WIN, game)
            back_to_menu = False
            while back_to_menu == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game.running, game.game_on = False, False
                        game.curr_menu.run_display = False
                        back_to_menu = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        back_to_menu = True
        # check for a stalemate
        elif game.game_on==True and game.board.check_stalemate(game)==True:
            stalemate_display(WIN, game)
            game.game_on = False
            back_to_menu = False
            while back_to_menu is False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game.running, game.game_on = False, False
                        game.curr_menu.run_display = False
                        back_to_menu = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        back_to_menu = True
        #check turn
        elif game.turn == 'ai':
            if ITERATIVE_DP:
                new_board = opponent.iterative_search(game.get_board(), 'ai', game)
            else:
                alpha = float('-inf')
                beta = float('inf')
                _, new_board = opponent.step(game.board, DEPTH, 'ai', alpha, beta, game)
            game.ai_move(new_board)
            game.selected=None
        else: # human's turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running, game.game_on = False, False
                    game.curr_menu.run_display = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = get_mouse_pos(pygame.mouse.get_pos())
                    if game.turn == 'human':
                        game.select(row, col)
        # end game
        if game.board.PLAYER1_left < 5 or game.board.PLAYER2_left < 5 and game.music[0]=='On':
            game.music[1]='Endgame'
            game.set_music(background, tense)
            
        game.update()
    
def main():
    clock = pygame.time.Clock()
    game = Game(WIN)
    background.play(-1)
    tense.play(-1)
    tense.set_volume(0)
    background.set_volume(0)
    # RUN GAME
    while game.running:
        if game.music[0]=='On':
            game.music[1]='Game'
            game.set_music(background, tense)
        game.curr_menu.display_menu()
        play_game(game, clock)
        game.reset()
        
    pygame.quit()
    
main()