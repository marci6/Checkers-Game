import pygame
WIDTH, HEIGHT = 800,800
BLACK = (0, 0, 0)
GREY = (128,128,128)
WHITE = (255,255,255)
SIZE = 11
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('X', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.win.blit(self.game.win, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.win.fill(BLACK)
            self.game.draw_text('Main Menu', 20, WIDTH / 2, HEIGHT / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.game_on = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Levels'
        self.aix, self.aiy = self.mid_w, self.mid_h + 20
        self.bx ,self.by = self.mid_w - 150, self.mid_h + 40
        self.mx ,self.my = self.mid_w, self.mid_h + 40
        self.adx ,self.ady = self.mid_w + 150, self.mid_h + 40
        self.onx, self.ony = self.mid_w-100, self.mid_h + 80
        self.offx, self.offy = self.mid_w+100, self.mid_h + 80
        self.Musicx, self.Musicy = self.mid_w, self.mid_h + 60
        self.hintsx, self.hintsy = self.mid_w, self.mid_h + 100
        self.onhx, self.onhy = self.mid_w-100, self.mid_h + 120
        self.offhx, self.offhy = self.mid_w+100, self.mid_h + 120
        self.turnx, self.turny = self.mid_w, self.mid_h + 140
        self.p1x, self.p1y = self.mid_w-100, self.mid_h + 160
        self.p2x, self.p2y = self.mid_w+100, self.mid_h + 160
        self.cursor_rect.midtop = (self.aix + self.offset, self.aiy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.win.fill((0, 0, 0))
            self.game.draw_text('Options', 20, WIDTH / 2, HEIGHT / 2 - 30)
            self.game.draw_text("AI Cleverness", 15, self.aix, self.aiy)
            self.draw_levels()
            self.game.draw_text("Music", 15, self.Musicx, self.Musicy)
            self.draw_music()
            self.draw_hints()
            self.draw_cursor()
            self.blit_screen()

    def draw_hints(self):
        self.game.draw_text("Hints", 15, self.hintsx, self.hintsy)
        if self.game.Hints == 'Off':
            self.game.draw_text('Off', 15, self.offhx, self.offhy, WHITE)
            self.game.draw_text('On', 15, self.onhx, self.offhy, GREY)
        else :
            self.game.draw_text('Off', 15, self.offhx, self.offhy, GREY)
            self.game.draw_text('On', 15, self.onhx, self.onhy, WHITE)
            
            
    def draw_music(self):
        if self.game.music[0] == 'Off':
            self.game.draw_text('Off', 15, self.offx, self.offy, WHITE)
            self.game.draw_text('On', 15, self.onx, self.offy, GREY)
        else :
            self.game.draw_text('Off', 15, self.offx, self.offy, GREY)
            self.game.draw_text('On', 15, self.onx, self.ony, WHITE)
        
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == 'Levels':
                self.state = 'Music'
                self.cursor_rect.midtop = (self.Musicx + self.offset, self.Musicy)
            elif self.state == 'Music':
                self.state = 'Hints'
                self.cursor_rect.midtop = (self.hintsx + self.offset, self.hintsy)
            elif self.state == 'Hints':
                self.state = 'Levels'
                self.cursor_rect.midtop = (self.aix + self.offset, self.aiy)
        
        elif self.game.UP_KEY:
            if self.state == 'Levels':
                self.state = 'Hints'
                self.cursor_rect.midtop = (self.hintsx + self.offset, self.hintsy)
            elif self.state == 'Music':
                self.state = 'Levels'
                self.cursor_rect.midtop = (self.aix + self.offset, self.aiy)
            elif self.state == 'Hints':
                self.state = 'Music'
                self.cursor_rect.midtop = (self.Musicx + self.offset, self.Musicy)
        
        elif self.game.RIGHT_KEY and self.state == 'Levels':
            if self.game.cleverness == 'Beginner':
                self.game.cleverness = 'Medium'
            elif self.game.cleverness == 'Medium':
                self.game.cleverness = 'Advance'
            elif self.game.cleverness == 'Advance':
                self.game.cleverness = 'Beginner'
                
        elif self.game.LEFT_KEY and self.state == 'Levels':
            if self.game.cleverness == 'Beginner':
                self.game.cleverness = 'Advance'
            elif self.game.cleverness == 'Medium':
                self.game.cleverness = 'Beginner'
            elif self.game.cleverness == 'Advance':
                self.game.cleverness = 'Medium'
                
        elif self.game.RIGHT_KEY and self.state == 'Music':
            if self.game.music[0] == 'On':
                self.game.music[0] = 'Off'
            elif self.game.music[0] == 'Off':
                self.game.music[0] = 'On'
        elif self.game.LEFT_KEY and self.state == 'Music':
            if self.game.music[0] == 'On':
                self.game.music[0] = 'Off'
            elif self.game.music[0] == 'Off':
                self.game.music[0] = 'On'
                
        elif self.game.RIGHT_KEY and self.state == 'Hints':
            if self.game.Hints == 'On':
                self.game.Hints = 'Off'
            elif self.game.Hints == 'Off':
                self.game.Hints = 'On'
        elif self.game.LEFT_KEY and self.state == 'Hints':
            if self.game.Hints == 'On':
                self.game.Hints = 'Off'
            elif self.game.Hints == 'Off':
                self.game.Hints = 'On'
                


        
    def draw_levels(self):
        if self.game.cleverness == 'Beginner':
            self.game.draw_text('Beginner', 15, self.bx, self.by, WHITE)
            self.game.draw_text('Medium', 15, self.mx, self.my, GREY)
            self.game.draw_text('Advance', 15, self.adx, self.ady, GREY)
        elif self.game.cleverness == 'Medium':
            self.game.draw_text('Beginner', 15, self.bx, self.by, GREY)
            self.game.draw_text('Medium', 15, self.mx, self.my, WHITE)
            self.game.draw_text('Advance', 15, self.adx, self.ady, GREY)
        else:
            self.game.draw_text('Beginner', 15, self.bx, self.by, GREY)
            self.game.draw_text('Medium', 15, self.mx, self.my, GREY)
            self.game.draw_text('Advance', 15, self.adx, self.ady, WHITE)
        
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.win.fill(BLACK)
            self.game.draw_text('Credits', 20, WIDTH / 2, HEIGHT / 2 - 310)
            self.game.draw_text('Made by Marcello Chiesa', 15, WIDTH / 2, HEIGHT / 2 - 290)
            # Rules
            self.game.draw_text('rules', 15, WIDTH / 2, HEIGHT / 2 - 260)
            self.game.draw_text('The black pieces move first.', SIZE, WIDTH / 2, HEIGHT / 2 - 240)
            self.game.draw_text('Pieces are always moved diagonally. The black pieces move first.', SIZE, WIDTH / 2, HEIGHT / 2 - 220)
            self.game.draw_text('Each player takes their turn by moving a piece, either:', SIZE, WIDTH / 2, HEIGHT / 2 - 200)
            self.game.draw_text('-Diagonally in the forward direction', SIZE-2, WIDTH / 2, HEIGHT / 2 - 180)
            self.game.draw_text("-By jumping over an opponent's piece into a free square. Capture is mandatory when available", SIZE-2, WIDTH / 2, HEIGHT / 2 - 160)
            self.game.draw_text("If a piece reaches the last row it becomes a king.", SIZE, WIDTH / 2, HEIGHT / 2 - 140)
            self.game.draw_text("Kings can move in both directions.", SIZE, WIDTH / 2, HEIGHT / 2 - 120)
            # Algorithm
#            self.game.draw_text('how it works', 15, WIDTH / 2, HEIGHT / 2 - 260)
#            self.game.draw_text('this game implements an intelligent opponent', 10, WIDTH / 2, HEIGHT / 2 - 240)
#            self.game.draw_text('the algorithm powering the opponent is called minimax algorithm with alpha beta pruning', 10, WIDTH / 2, HEIGHT / 2 - 220)
#            self.game.draw_text('it simulates every possible move and evaluate its effectiveness', 10, WIDTH / 2, HEIGHT / 2 - 200)
            self.blit_screen()