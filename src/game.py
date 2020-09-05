class Cell:
    # Game board cell. Contains player selection.
    def __init__(self, pos_y, pos_x):
        self.player = None
        self.position_y = pos_y
        self.position_x = pos_x
    def update_cell(self, player):
        self.player = player

class Player:
    def __init__(self, name, figure, computer=False):
        self.human = False if computer else True
        self.computer = computer
        self.name = name
        self.figure = figure

import random

# Customisable Defaults & Settings
MAX_PLAYER_LIMIT = 2
DEFAULT_BOARD_SIZE = 3
BOARD_DESIGN_Y = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
BOARD_DESIGN_X = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
BOARD_DESIGN_NONE = "-"
BOARD_NEW_LINE = "\n"

class Gameboard:
    board = list()
    players = list()
    player_turn = 0

    def __init__(self, boardsize=DEFAULT_BOARD_SIZE):
        self.boardsize = boardsize # board n x n
        self.reset_board()
    
    def reset_board(self):
        self.board.clear()
        for y in range(self.boardsize):
            for x in range(self.boardsize):
                self.board.append(Cell(y, x)) # Add empty cell
    
    def add_player(self, player):
        self.players.append(player) if len(self.players) < MAX_PLAYER_LIMIT else False

    def render_gameboard_string(self):
        # Add x axis decoration
        s = " "
        for i, d in enumerate(BOARD_DESIGN_X):
            if i < self.boardsize:
                s += " {} ".format(d)
        s += BOARD_NEW_LINE
        # Loop through cells
        for c in self.board:
            # Add Y axis decoration
            if c.position_x == 0:
                s += BOARD_DESIGN_Y[c.position_y]
            # Add cell item
            if c.player == None:
                s += " {} ".format(BOARD_DESIGN_NONE)
            else:
                s += " {} ".format(self.players[c.player].figure)
            # Add new line char
            if c.position_x == self.boardsize-1:
                s += BOARD_NEW_LINE
        return s

    def get_winning_sequencies(self):
        w = list()
        # Y lines
        for y in range(self.boardsize):
            line = list()
            for c in self.board:
                if c.position_y == y:
                    line.append([c.position_y, c.position_x])
            w.append(line)
        # X lines
        for x in range(self.boardsize):
            line = list()
            for c in self.board:
                if c.position_x == x:
                    line.append([c.position_y, c.position_x])
            w.append(line)
        # Diagonals
        line = list()
        for i in range(self.boardsize):
            line.append([i, i])
        w.append(line)
        line = list()
        for i in range(self.boardsize):
            line.append([self.boardsize - 1 - i, i])
        w.append(line)
        return w

    def check_gameover(self):
        w_sequencies = self.get_winning_sequencies()
        for w in w_sequencies:
            player = list()
            for w_c in w:
                for c in self.board:
                    if c.position_y == w_c[0] and c.position_x == w_c[1]:
                        player.append(c.player)
            if all(x==player[0] for x in player):
                if player[0] != None:
                    return True
        return False

    def player_move(self, selection):
        try:
            selected_y = BOARD_DESIGN_Y.index(selection[0])
            selected_x = BOARD_DESIGN_X.index(selection[1])
        except:
            return False

        for c in self.board:
            if c.position_y == selected_y and c.position_x == selected_x:
                # Ya player is free to select
                if c.player == None:
                    c.update_cell(self.player_turn)
                    return True
        return False

    def computer_move(self):
        i = random.randint(0, len(self.board)-1)
        while self.board[i].player != None:
            i = random.randint(0, len(self.board)-1)
        self.board[i].update_cell(self.player_turn)

    def next_turn(self):  
        self.player_turn = (self.player_turn + 1) % len(self.players)

    def get_current_player(self):
        return self.players[self.player_turn]
    
    def reset(self):
        self.reset_board()
        self.player_turn = 0

class Game:
    play = True
    state = 0    

    def __init__(self):
        random.seed()
        self.gameboard = Gameboard()
    
    def update_settings(self, settings):
        self.state = settings['state']
        self.gameboard.add_player(Player(settings['human_name'], settings['human_figure']))
        self.gameboard.add_player(Player(settings['computer_name'], settings['computer_figure'], True))
        self.gameboard.boardsize = settings['board_size']
        self.gameboard.reset_board()

    def play_game_main(self):
        while self.play: # State Machine
            if self.state == 0: # Menu Selector
                print("Welcome to Tic-Tack-Toe version 0.0.1")
                player_name = str(input("What is your name? "))
                player_figure = str(input("Select either norts or crosses? x, o "))
                self.gameboard.add_player(Player(player_name, player_figure))
                print("A computer player want to join!")
                computer_name = str(input("Computers name? "))
                self.gameboard.add_player(Player(computer_name, "0" if player_figure == "X" else "X", True))
                print()
                print()
                self.state = self.state + 1

            elif self.state == 1: # Game Loop
                print("{}s Turn\n".format(self.gameboard.get_current_player().name))

                # Render Gameboard
                print(self.gameboard.render_gameboard_string())

                # Check if game is over
                if not self.gameboard.check_gameover():

                    # Player gets to have a turn
                    if self.gameboard.players[self.gameboard.player_turn].human:
                        select_move = True
                        while select_move:
                            player_selection = input("Select your next move! (eg. A1) ")
                            print()
                            select_move = not self.gameboard.player_move(player_selection)

                    # Computer gets to have a turn
                    if self.gameboard.players[self.gameboard.player_turn].computer:
                        self.gameboard.computer_move()
                        print("{} Played\n".format(self.gameboard.get_current_player().name))

                    # Go to next player
                    if not self.gameboard.check_gameover():
                        self.gameboard.next_turn()

                else:
                    # go to the end game
                    self.state = self.state + 1

            elif(self.state == 2): # High Score & Reset
                print("{} Won!".format(self.gameboard.get_current_player().name))
                play_again = input("Play again? y/n ")
                if play_again == "y":
                    self.gameboard.reset()
                    self.state = 1
                else:
                    self.play = False