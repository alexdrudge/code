# import needed modules
import pygame
import time

# initialise display and clock
display_window = pygame.display.set_mode((340,340))
pygame.display.set_caption("Tic Tac Toe")
display_clock = pygame.time.Clock()

class Board():

    # open the image for the grid
    game_background = pygame.image.load("projects/TicTacToe/grid.png")

    def __init__(self):
        # open the images for the cells
        no_symbol = pygame.image.load("projects/TicTacToe/_.png")
        x_symbol = pygame.image.load("projects/TicTacToe/x.png")
        o_symbol = pygame.image.load("projects/TicTacToe/o.png")

        # create both players with their respecive symbols
        # add the players to a list for easy handling
        player1 = Player(x_symbol)
        player2 = Player(o_symbol)
        self.players = [player1, player2]
        # create a fake player that is a stand in for empty cells
        player0 = Player(no_symbol)
        self.player0 = player0

        # initialise the grid, turn count
        self.grid = [[player0, player0, player0],[player0, player0, player0],[player0, player0, player0]]
        self.turn = 0
    
    def place(self, mouse):
        # loop through the rows and the columns
        exited_game = False
        for i in range(3):
            for j in range(3):
                # check what cell the mouse is hovering over
                if 110 * i + 10 < mouse[0] < 110 * i + 110:
                    if 110 * j + 10 < mouse[1] < 110 * j + 110:
                        # check that the cell is empty
                        if self.grid[i][j] == self.player0:
                            # replace the cell with the player
                            self.grid[i][j] = self.players[self.turn]
                            # itterate the turn forward
                            self.turn = (self.turn + 1) % 2
                            # check to see if the game is won or drawn
                            exited_game = self.checkGrid()
        return exited_game
    
    def showGrid(self):
        # display the grid to the screen behind all other objects
        display_window.blit(Board.game_background,(0,0))
        # loop through the cels in the grid
        for i in range(3):
            for j in range(3):
                # define the coord that the symbol will be displayed at
                coord = (110 * i + 10, 110 * j + 10)
                self.grid[i][j].showSymbol(coord)
    
    def checkGrid(self):
        # loop though the grid checking for filled cells
        count = 0
        for i in range(3):
            for j in range(3):
                # if the cell is not empty itterate the counter
                if self.grid[i][j] != self.player0:
                    count += 1

        # both players check if they have won
        exited_game = False
        for i in self.players:
            exited_game = i.checkWin(self.grid)
            if exited_game:
                return True

        # if all cells are used then its a draw
        if count == 9:
            # display the final state of the game
            self.showGrid()
            pygame.display.update()
            # freeze the screen for a second
            time.sleep(1)
            return True

        # if the game is not won or drawn then keep playing
        return False

class Player():

    # open the image for the victory screen
    game_victory = pygame.image.load("projects/TicTacToe/victory.png")

    def __init__(self, symbol):
        # define the symbol that the player is using
        self.symbol = symbol
    
    def showSymbol(self, coord):
        # display the players symbol at the given coords
        display_window.blit(self.symbol, coord)
    
    def checkWin(self, grid):
        # check if the player has three in a row
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] == self:
                self.victory()
                return True
        for j in range(3):
            if grid[0][j] == grid[1][j] == grid[2][j] == self:
                self.victory()
                return True
        if grid[0][0] == grid[1][1] == grid[2][2] == self:
            self.victory()
            return True
        if grid[0][2] == grid[1][1] == grid[2][0] == self:
            self.victory()
            return True
        return False
    
    def victory(self):
        # display the victory background with the players symbol
        display_window.blit(Player.game_victory,(0,0))
        display_window.blit(self.symbol,(120,10))
        pygame.display.update()
        # freeze the game for a second
        time.sleep(1)

def title():

    # open the image for the title page
    title_background = pygame.image.load("projects/TicTacToe/home.png")

    # loop through the logic while the user hasnt quitted
    exited_display = False
    while not exited_display:
        
        # display the background
        display_window.blit(title_background,(0,0))

        # run the event loop
        for event in pygame.event.get():

            # check if the user has tried to close the game
            if event.type == pygame.QUIT:
                exited_display = True
            
            # get the mouse position and detect if its being pressed
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # check if either of the buttons are being pressed
                if 120 < mouse[0] < 220:
                    if 120 < mouse[1] < 220:
                        game()
                    if 230 < mouse[1] < 330:
                        exited_display = True

        # update the display (not needed)
        pygame.display.update()
        display_clock.tick(30)

def game():

    # define the playing board and the players
    board = Board()

    # loop though the game logic untill a win, draw or exit
    exited_game = False
    while not exited_game:

        # run the event loop
        for event in pygame.event.get():

            # check if the user has pressed the quit button
            if event.type == pygame.QUIT:
                exited_game = True
            
            # checks if the user clicks the mouse
            # runs through inputting the users selection of a cell
            # runs through if the game is won or drawn
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                exited_game = board.place(mouse)

        # displays the grid and the symbols on the grid
        # doesnt run if the game is won (prevents flickering)
        if not exited_game:
            board.showGrid()
        
        # updates the display
        pygame.display.update()
        display_clock.tick(30)

# runs the title loop
title()
pygame.quit()
