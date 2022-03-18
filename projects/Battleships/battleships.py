# import modules
from abc import ABC, abstractmethod
from random import randint

# abstract class that defines the methods for the player and computer
class Player(ABC):
    
    @abstractmethod
    def __init__(self, width, height):
        pass
    
    # returns the board object
    def getBoard(self):
        return self.board

    @abstractmethod
    def takeShot(self, target):
        pass

# subclass that defines the players controls
class HumanPlayer(Player):

    def __init__(self, width, height):
        self.board = HumanBoard(width, height)
    
    def takeShot(self, target):
        print("taking a shot:")
        # player choses location to shoot
        shotPlaced = False
        while not shotPlaced:

            xSet = False
            xPos = 0
            while not xSet:
                try:
                    xPos = int(input("enter the column number, from 1-%d: " % (target.getWidth()))) - 1
                    if 0 <= xPos <= target.getWidth()-1:
                        xSet = True
                    else:
                        print("ERROR integer out of range")
                except:
                    print("ERROR enter an integer")
            
            ySet = False
            yPos = 0
            while not ySet:
                try:
                    yPos = int(input("enter the row number, from 1-%d: " % (target.getHeight()))) - 1
                    if 0 <= yPos <= target.getHeight()-1:
                        ySet = True
                    else:
                        print("ERROR integer out of range")
                except:
                    print("ERROR enter an integer")
            
            # check that the location is a new shot
            location = ""
            location = target.getBoardPos(xPos, yPos)
            if location == " " or location == "B":
                shotPlaced = True
            else:
                print("ERROR you have already taken that shot")
        
        # set the new state of the hit position
        target.setPos(xPos, yPos)

# subclass that defines the computers logic  
class ComputerPlayer(Player):

    def __init__(self, width, height):
        self.board = ComputerBoard(width, height)
    
    def takeShot(self, target):
        print("computer shooting:")
        # check if their is already a hit cell to shoot around
        shotTaken = False
        for i in range(target.getHeight()):
            for j in range(target.getWidth()):
                if target.getBoardPos(j,i) == "H":
                    # attempt to hit a cell surrounding the boat
                    if i != 0 and shotTaken == False:
                        if target.getBoardPos(j,i-1) == " " or target.getBoardPos(j,i-1) == "B":
                            shotTaken = True
                            target.setPos(j,i-1)
                            print("shot taken at column %d, row %d" % (j, i-1))
                    if i != target.getHeight()-1 and shotTaken == False:
                        if target.getBoardPos(j,i+1) == " " or target.getBoardPos(j,i+1) == "B":
                            shotTaken = True
                            target.setPos(j,i+1)
                            print("shot taken at column %d, row %d" % (j, i+1))
                    if j!= 0 and shotTaken == False:
                        if target.getBoardPos(j-1,i) == " " or target.getBoardPos(j-1,i) == "B":
                            shotTaken = True
                            target.setPos(j-1,i)
                            print("shot taken at column %d, row %d" % (j-1, i))
                    if j!= target.getWidth()-1 and shotTaken == False:
                        if target.getBoardPos(j+1,i) == " " or target.getBoardPos(j+1,i) == "B":
                            shotTaken = True
                            target.setPos(j+1,i)
                            print("shot taken at column %d, row %d" % (j+1, i))
        
        # shoot at a random position
        while not shotTaken:
            xPos = randint(0,target.getWidth()-1)
            yPos = randint(0,target.getHeight()-1)
            if target.getBoardPos(xPos,yPos) == " " or target.getBoardPos(xPos,yPos) == "B":
                shotTaken = True
                target.setPos(xPos,yPos)
                print("shot taken at column %d, row %d" % (xPos, yPos))


# abstract class that defined the boards
class Board(ABC):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        self.ships = []

        # creates the nested list that is the board
        row = []
        for i in range(self.width):
            row.append(" ")
        for i in range(self.height):
            self.board.append(list(row))
    
    def checkWinner(self):
        # check if all ships have been sunk
        gameWon = True
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == "B":
                    gameWon = False
        return gameWon
    
    @abstractmethod
    def display(self):
        pass

        # return the state of a location
    def getBoardPos(self, xPos, yPos):
        return self.board[yPos][xPos]
    
    def setPos(self, xPos, yPos):
        # update the hit cell
        if self.board[yPos][xPos] == " ":
            self.board[yPos][xPos] = "x"
        if self.board[yPos][xPos] == "B":
            self.board[yPos][xPos] = "H"
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height

# subclass that defines the players board
class HumanBoard(Board):

    def __init__(self, width, height):
        super().__init__(width, height)

        self.display()
        # gets the player to chose where their ships go
        for length in [5,4,3,3,2,2]:
            print("palcing a ship of length %d:" % (length))

            shipPlaced = False
            while not shipPlaced:

                # set the orinentation of the ship
                directionSet = False
                direction = ""
                while not directionSet:
                    direction = input("""type 1 for a vertical ship
type 2 for a horizontal ship: """)
                    if direction == "1":
                        directionSet = True
                    elif direction == "2":
                        directionSet = True
                    else:
                        print("ERROR enter a specified number")
                
                # set the starting point of the ship
                xSet = False
                xPos = 0
                while not xSet:
                    try:
                        if direction == "1":
                            xPos = int(input("enter the column number, from 1-%d: " % (self.width))) - 1
                            if 0 <= xPos <= self.width-1:
                                xSet = True
                            else:
                                print("ERROR integer out of range")
                        if direction == "2":
                            xPos = int(input("enter the column number, from 1-%d: " % (self.width-length+1))) - 1
                            if 0 <= xPos <= self.width-length:
                                xSet = True
                            else:
                                print("ERROR integer out of range")
                    except:
                        print("ERROR enter an integer")

                ySet = False
                yPos = 0
                while not ySet:
                    try:
                        if direction == "1":
                            yPos = int(input("enter the row number, from 1-%d: " % (self.height-length+1))) - 1
                            if 0 <= yPos <= self.height-length:
                                ySet = True
                            else:
                                print("ERROR integer out of range")
                        if direction == "2":
                            yPos = int(input("enter the row number, from 1-%d: " % (self.height))) - 1
                            if 0 <= yPos <= self.height-1:
                                ySet = True
                            else:
                                print("ERROR integer out of range")
                    except:
                        print("ERROR enter an integer")
                
                # check if their is already a ship
                emptySpace = True
                for i in range(length):
                    if direction == "1":
                        if self.board[yPos+i][xPos] != " ":
                            emptySpace = False
                    if direction == "2":
                        if self.board[yPos][xPos+i] != " ":
                            emptySpace = False
                # determine if the player needs to reenter their ship
                if emptySpace == True:
                    shipPlaced = True
                    self.ships.append([length,xPos,yPos,int(direction)])
                else:
                    print("ERROR your ships collided")
        
            # palce the ship onto the grid
            for i in range(length):
                if direction == "1":
                    self.board[yPos+i][xPos] = "B"
                if direction == "2":
                    self.board[yPos][xPos+i] = "B"
            self.display()

    def display(self):
        print("player board: ")
        # print the table using unicode box drawing
        print("┌─", end="")
        for i in range(self.width-1):
            print("──┬─", end="")
        print("──┐")

        for i in range(self.height):
            for j in range(self.width):
                print("│ %s " % (self.board[i][j]), end="")
            print("│")
            if i != self.height-1:
                print("├─", end="")
                for j in range(self.width-1):
                    print("──┼─", end="")
                print("──┤")
        
        print("└─", end="")
        for i in range(self.width-1):
            print("──┴─", end="")
        print("──┘")

# subclass that defines the computers board
class ComputerBoard(Board):

    def __init__(self, width, height):
        super().__init__(width, height)

        # computer randomly choses the locations of the ships
        for length in [5,4,3,3,2,2]:

            shipPlaced = False
            while not shipPlaced:

                direction = randint(1,2)
                if direction == 1:
                    xPos = randint(0,self.width-1)
                    yPos = randint(0,self.height-length)
                if direction == 2:
                    xPos = randint(0,self.width-length)
                    yPos = randint(0,self.height-1)
                
                emptySpace = True
                for i in range(length):
                    if direction == 1:
                        if self.board[yPos+i][xPos] != " ":
                            emptySpace = False
                    if direction == 2:
                        if self.board[yPos][xPos+i] != " ":
                            emptySpace = False
                
                if emptySpace == True:
                    shipPlaced = True
                    self.ships.append([length,xPos,yPos,direction])
            
            for i in range(length):
                if direction == 1:
                    self.board[yPos+i][xPos] = "B"
                if direction == 2:
                    self.board[yPos][xPos+i] = "B"
                
    def display(self):
        print("computer board:")
        # print the table using unicode box drawing
        print("┌─", end="")
        for i in range(self.width-1):
            print("──┬─", end="")
        print("──┐")

        symbol = " "
        for i in range(self.height):
            for j in range(self.width):
                symbol = self.board[i][j]
                if symbol == "B":
                    symbol = " "
                print("│ %s " % (symbol), end="")
                symbol = " "
            print("│")
            if i != self.height-1:
                print("├─", end="")
                for j in range(self.width-1):
                    print("──┼─", end="")
                print("──┤")
        
        print("└─", end="")
        for i in range(self.width-1):
            print("──┴─", end="")
        print("──┘")

def main():

    widthSet = False
    heightSet = False
    width = 0
    height = 0
    # set the width of the game board
    while not widthSet:
        try:
            width = int(input("enter the width, from 10-26: "))
            if 10 <= width <= 26:
                widthSet = True
            else:
                print("ERROR integer out of range")
        except:
            print("ERROR enter an integer")
    # set the height of the game board
    while not heightSet:
        try:
            height = int(input("enter the height, from 10-26: "))
            if 10 <= height <= 26:
                heightSet = True
            else:
                print("ERROR integer out of range")
        except:
            print("ERROR enter an integer")
    
    # initialise all objects that are used in the game
    player1 = HumanPlayer(width, height)
    player2 = ComputerPlayer(width, height)
    board1 = player1.getBoard()
    board2 = player2.getBoard()
	
    exited = False
    # run the main game loop
    while not exited:

        # start the players turn
        print("players turn:")
        
        makeShot = False
        result = ""
        # give the options for the players actions
        while not makeShot:
            result = input("""type 1 to take a shot
type 2 to display your board
type 3 to display the computers board
type 4 to see the key: """)
            if result == "1":
                makeShot = True
            elif result == "2":
                board1.display()
            elif result == "3":
                board2.display()
            elif result == "4":
                print("""B means boat 
H means hit
x means miss""")
            else:
                print("ERROR enter a specified number")

        # display the board to shoot at then take the shot 
        board2.display()
        player1.takeShot(board2)
        # check if the player just won
        playerWon = False
        playerWon = board2.checkWinner()
        if playerWon:
            board2.display()
            print("player has won!")
            exited = True
        
        # start the computers turn
        print("computers turn: ")

        # take the random shot then show if it hit
        player2.takeShot(board1)
        board1.display()
        # check if the computer just won
        computerWon = False
        computerWon = board1.checkWinner()
        if computerWon:
            board1.display()
            print("computer has won!")
            exited = True

# run the program
main()