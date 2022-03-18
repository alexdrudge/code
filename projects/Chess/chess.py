# initialise the libraries used
import pygame
from abc import ABC, abstractmethod
import time

# initialise the pygame varibles
pygame.init()
game_display = pygame.display.set_mode((550,550))
game_clock = pygame.time.Clock()

# main class used to controll the logic of the game
class Board():
    def __init__(self):
        # initialise the grid and images used
        # two dimentional list, i is each row and j is each column
        self.grid = [["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]
        self.image = pygame.image.load("projects/Chess/chess_board.png")
        self.selected_image = pygame.image.load("projects/Chess/selected.png")
        self.selected = ""
        self.white = pygame.image.load("projects/Chess/white/tile.png")
        self.black = pygame.image.load("projects/Chess/black/tile.png")

        # create the chess layout for both teams and initialise the objects
        for i in range(8):
            for j in range(8):
                if i == 0:
                    if j == 0 or j == 7:
                        self.grid[i][j] = Rook("black",i,j)
                    if j == 1 or j == 6:
                        self.grid[i][j] = Knight("black",i,j)
                    if j == 2 or j == 5:
                        self.grid[i][j] = Bishop("black",i,j)
                    if j == 3:
                        self.grid[i][j] = Queen("black",i,j)
                    if j == 4:
                        self.grid[i][j] = King("black",i,j)

                if i == 1:
                    self.grid[i][j] = Pawn("black",i,j)

                if i == 6:
                    self.grid[i][j] = Pawn("white",i,j)

                if i == 7:
                    if j == 0 or j == 7:
                        self.grid[i][j] = Rook("white",i,j)
                    if j == 1 or j == 6:
                        self.grid[i][j] = Knight("white",i,j)
                    if j == 2 or j == 5:
                        self.grid[i][j] = Bishop("white",i,j)
                    if j == 3:
                        self.grid[i][j] = Queen("white",i,j)
                    if j == 4:
                        self.grid[i][j] = King("white",i,j)
    
    def display(self,team):
        # display the background a turn tile
        game_display.blit(self.image,(0,0))
        if team == "white":
            game_display.blit(self.white,(10,10))
        if team == "black":
            game_display.blit(self.black,(10,10))

        # add a green background to highlighted pieces
        if self.selected != "":
            ypos = 60*(self.selected.get_i() + 1) + 10
            xpos = 60*(self.selected.get_j() + 1) + 10
            game_display.blit(self.selected_image, (xpos,ypos))

        # iotterate through the grid and display all objects
        ypos = 10
        xpos = 10
        for i in self.grid:
            ypos += 60
            for j in i:
                xpos += 60
                if j != "":
                    # each object displays its own image
                    j.display(xpos,ypos)
            xpos = 10
        
    def select(self,i,j,team):
        # if the clicked on piece is on the current turns team, select it
        piece = self.grid[i][j]
        if piece != "":
            if piece.get_team() == team:
                self.selected = piece

    def move(self,i,j,team):
        # check if the clicking on piece is on the opposite team
        move_pieces = False
        if self.selected != "":
            if self.grid[i][j] == "" or self.grid[i][j].get_team() != team:
                # get the current positiom of the selected item
                ipos = self.selected.get_i()
                jpos = self.selected.get_j()
                # validate the move
                move_pieces = self.selected.move(i,j,self)
                if move_pieces:
                    # move the piece to its new position
                    self.grid[i][j] = self.selected
                    # reset the position that it was in
                    self.grid[ipos][jpos] = ""
                    self.selected = ""
                    # swap the turn over
                    if team == "white":
                        return "black"
                    if team == "black":
                        return "white"
                else:
                    # deselect the tile if a move was invalid to show it failed
                    self.selected = ""
        return team
    
    def get_position(self,i,j):
        return self.grid[i][j]
    
    def check_win(self,team):
        # itterate through the grid and check for the existance of an enemy king
        won = True
        for i in self.grid:
            for j in i:
                if j != "":
                    if j.get_type() == "king" and j.get_team() == "black" and team == "white":
                        won = False
                    if j.get_type() == "king" and j.get_team() == "white" and team == "black":
                        won = False
        # if won display the winners coloured tile over the grid
        if won:
            ypos = 10
            xpos = 10
            for i in range(8):
                ypos += 60
                for j in range(8):
                    xpos += 60
                    if team == "white":
                        game_display.blit(self.white,(xpos,ypos))
                    if team == "black":
                        game_display.blit(self.black,(xpos,ypos))
                xpos = 10
            
            # pause the game to show the victory screen before closing the game
            pygame.display.update()
            time.sleep(2)
            return True

# an abstract class that defines how all of the piece classes should function
# all classes inherit the getters and setters from this class   
class Piece(ABC):
    def __init__(self,team,i,j):
        self.team = team
        self.i = i
        self.j = j
    
    def display(self,xpos,ypos):
        # display the pieces image at the given position
        game_display.blit(self.image,(xpos,ypos))
    
    def get_team(self):
        return self.team
    
    def get_i(self):
        return self.i

    def get_j(self):
        return self.j
    
    def get_type(self):
        return self.type

    # defines the name and parameters of the move method
    @abstractmethod
    def move(self,i,j,board):
        pass

class Pawn(Piece):
    def __init__(self,team,i,j):
        super().__init__(team,i,j)
        # load in the pawns image
        file_name = "projects/Chess/" + team + "/pawn.png"
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image,(50,50))
        self.type = "pawn"
        self.moved = False
    
    def move(self,i,j,board):
        piece = ""
        # seperate the teams as pawns only move in one direction
        if self.team == "white":
            if j - self.j == 0:
                # if they havent moved they can go two positons
                if not self.moved:
                    if i - self.i == -2:
                        # check if their is a piece in the way of movement
                        if board.get_position(self.i - 1,j) == "" and board.get_position(self.i - 2,j) == "":
                            self.i = i
                            self.j = j
                            self.moved = True
                            return True
                # check that the piece is only moving one tile
                if i - self.i == -1:
                    if board.get_position(self.i - 1, j) == "":
                        self.i = i
                        self.j = j
                        self.moved = True
                        return True
            else:
                # check if its is sidestepping to take a piece
                if i - self.i == -1:
                    if j - self.j == -1:
                        piece = board.get_position(self.i - 1, self.j - 1)
                    if j - self.j == 1:
                        piece = board.get_position(self.i - 1, self.j + 1)
                    # check if their was a piece to take
                    if piece != "":
                        if piece.get_team() == "black":
                            self.i = i
                            self.j = j
                            self.moved = True
                            return True
            return False
        # same logic as before but going in the opposite direction
        if self.team == "black":
            if j - self.j == 0:
                if not self.moved:
                    if i - self.i == 2:
                        if board.get_position(self.i + 1,j) == "" and board.get_position(self.i + 2,j) == "":
                            self.i = i
                            self.j = j
                            self.moved = True
                            return True
                if i - self.i == 1:
                    if board.get_position(self.i + 1, j) == "":
                        self.i = i
                        self.j = j
                        self.moved = True
                        return True
            else:
                if i - self.i == 1:
                    if j - self.j == -1:
                        piece = board.get_position(self.i + 1, self.j - 1)
                    if j - self.j == 1:
                        piece = board.get_position(self.i + 1, self.j + 1)
                    if piece != "":
                        if piece.get_team() == "white":
                            self.i = i
                            self.j = j
                            self.moved = True
                            return True
        return False

class Rook(Piece):
    def __init__(self,team,i,j):
        super().__init__(team,i,j)
        # load in the rooks image
        file_name = "projects/Chess/" + team + "/rook.png"
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image,(50,50))
        self.type = "rook"
    
    def move(self,i,j,board):
        distance = 0
        blocked = False
        # check if it is moving horizontaly or veritcally
        if self.i == i:
            distance = j - self.j
            # if it moves one tile then it will always work
            if abs(distance) == 1:
                self.i = i
                self.j = j
                return True
            else:
                # check if their is piece in the way of movement
                if distance > 1:
                    for k in range(1,distance):
                        if board.get_position(i,self.j+k) != "":
                            blocked = True
                if distance < -1:
                    for k in range(-1,distance,-1):
                        if board.get_position(i,self.j+k) != "":
                            blocked = True
                if blocked:
                    return False
                else:
                    self.i = i
                    self.j = j
                    return True

        # same logic as before but in the other dimention
        if self.j == j:
            distance = i - self.i
            if abs(distance) == 1:
                self.i = i
                self.j = j
                return True
            else:
                if distance > 1:
                    for k in range(1,distance):
                        if board.get_position(self.i+k,j) != "":
                            blocked = True
                if distance < -1:
                    for k in range(-1,distance,-1):
                        if board.get_position(self.i+k,j) != "":
                            blocked = True
                if blocked:
                    return False
                else:
                    self.i = i
                    self.j = j
                    return True
        return False

class Knight(Piece):
    def __init__(self,team,i,j):
        super().__init__(team,i,j)
        # load in the knights image
        file_name = "projects/Chess/" + team + "/knight.png"
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image,(50,50))
        self.type = "knight"
    
    # check if the piece is moving the correct number of tiles
    def move(self,i,j,board):
        if abs(i - self.i) == 2:
            if abs(j - self.j) == 1:
                self.i = i
                self.j = j
                return True
        if abs(j - self.j) == 2:
            if abs(i - self.i) == 1:
                self.i = i
                self.j = j
                return True
        return False

class Bishop(Piece):
    def __init__(self,team,i,j):
        super().__init__(team,i,j)
        # load in the bishops image
        file_name = "projects/Chess/" + team + "/bishop.png"
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image,(50,50))
        self.type = "bishop"
    
    def move(self,i,j,board):
        distance1 = i - self.i
        distance2 = j - self.j
        blocked = False
        # check if it is moving diagonally
        if abs(distance1) == abs(distance2):
            if abs(distance1) == 1:
                self.i = i
                self.j = j
                return True
            else:
                # check what direction it is moving diagonaly
                # check if their is a piece in the way of movement
                if distance1 < 0 and distance2 < 0:
                    for k in range(-1,distance1,-1):
                        if board.get_position(self.i+k,self.j+k) != "":
                            blocked = True
                if distance1 < 0 and distance2 > 0:
                    for k in range(-1,distance1,-1):
                        if board.get_position(self.i+k,self.j-k) != "":
                            blocked = True
                if distance1 > 0 and distance2 < 0:
                    for k in range(1,distance1):
                        if board.get_position(self.i+k,self.j-k) != "":
                            blocked = True
                if distance1 > 0 and distance2 > 0:
                    for k in range(1,distance1):
                        if board.get_position(self.i+k,self.j+k) != "":
                            blocked = True
                if blocked:
                    return False
                else:
                    self.i = i
                    self.j = j
                    return True
        return False

class Queen(Piece):
    def __init__(self,team,i,j):
        super().__init__(team,i,j)
        # load in the queens image
        file_name = "projects/Chess/" + team + "/queen.png"
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image,(50,50))
        self.type = "queen"

    def move(self,i,j,board):
        # used the same logic as the rook and bishop
        distance = 0
        blocked = False
        if self.i == i:
            distance = j - self.j
            if abs(distance) == 1:
                self.i = i
                self.j = j
                return True
            else:
                if distance > 1:
                    for k in range(1,distance):
                        if board.get_position(i,self.j+k) != "":
                            blocked = True
                if distance < -1:
                    for k in range(-1,distance,-1):
                        if board.get_position(i,self.j+k) != "":
                            blocked = True
                if blocked:
                    return False
                else:
                    self.i = i
                    self.j = j
                    return True

        if self.j == j:
            distance = i - self.i
            if abs(distance) == 1:
                self.i = i
                self.j = j
                return True
            else:
                if distance > 1:
                    for k in range(1,distance):
                        if board.get_position(self.i+k,j) != "":
                            blocked = True
                if distance < -1:
                    for k in range(-1,distance,-1):
                        if board.get_position(self.i+k,j) != "":
                            blocked = True
                if blocked:
                    return False
                else:
                    self.i = i
                    self.j = j
                    return True

        distance1 = i - self.i
        distance2 = j - self.j
        blocked = False
        if abs(distance1) == abs(distance2):
            if abs(distance1) == 1:
                self.i = i
                self.j = j
                return True
            else:
                if distance1 < 0 and distance2 < 0:
                    for k in range(-1,distance1,-1):
                        if board.get_position(self.i+k,self.j+k) != "":
                            blocked = True
                if distance1 < 0 and distance2 > 0:
                    for k in range(-1,distance1,-1):
                        if board.get_position(self.i+k,self.j-k) != "":
                            blocked = True
                if distance1 > 0 and distance2 < 0:
                    for k in range(1,distance1):
                        if board.get_position(self.i+k,self.j-k) != "":
                            blocked = True
                if distance1 > 0 and distance2 > 0:
                    for k in range(1,distance1):
                        if board.get_position(self.i+k,self.j+k) != "":
                            blocked = True
                if blocked:
                    return False
                else:
                    self.i = i
                    self.j = j
                    return True
        return False

class King(Piece):
    def __init__(self,team,i,j):
        super().__init__(team,i,j)
        # load in the kings image
        file_name = "projects/Chess/" + team + "/king.png"
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image,(50,50))
        self.type = "king"
    
    def move(self,i,j,board):
        # check if it is moving only 1 tile
        if abs(i - self.i) == 1 or abs(i - self.i) == 0:
            if abs(j - self.j) == 1 or abs(j - self.j) == 0:
                self.i = i
                self.j = j
                return True
        return False

def main():
    board = Board()
    turn = "white"

    game_exited = False
    while not game_exited:
        
        # check if the player presses the exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exited = True
            
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(8):
                    for j in range(8):
                        if 60*(i+1) + 10 < mouse[1] < 60*(i+2) and 60*(j+1) + 10 < mouse[0] < 60*(j+2):
                            # check for selection and moves with the given tile position
                            board.select(i,j,turn)
                            turn = board.move(i,j,turn)

        # show the display and tick the game forwards
        board.display(turn)
        pygame.display.update()
        game_clock.tick(30)

        # if the game was won activate the victory screen and exit the while loop
        won = False
        if turn == "white":
            won = board.check_win("black")
        if turn == "black":
            won = board.check_win("white")
        if won:
            game_exited = True

# run the game
main()