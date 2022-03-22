import pygame
from pathfinders import *
from queue import Queue
from stack import Stack

class Player:
    def __init__(self, screen, grid):
        self.__screen = screen
        self.__grid = grid
        # null values for its position
        self.__pos = [None, None]
        self.__x = None
        self.__y = None
        self.__colour = (0, 255, 255) # predefined colour
        self.__length = grid.get_length() # how long to make the square

    def display_player(self):
        if self.__x != None and self.__y != None: # only display if it has been placed
            pygame.draw.rect(self.__screen, self.__colour, (self.__x, self.__y, self.__length, self.__length))
    
    def update_pos(self, x, y):
        pos = self.__grid.xy_to_ij(x, y) # change to grid position
        if pos != [None, None]:
            self.__pos = pos
            if self.__grid.get_state(pos[0], pos[1]) != "wall":
                self.__x, self.__y = self.__grid.ij_to_xy(pos[0], pos[1]) # change back to screen position
    
    def get_pos(self):
        return self.__pos
    
    def move(self, direction):
        # attempt to update the piece to a new location
        if direction == "up":
            self.update_pos(self.__x, self.__y - self.__length)
        elif direction  == "down":
            self.update_pos(self.__x, self.__y + self.__length + 1)
        elif direction == "left":
            self.update_pos(self.__x - self.__length, self.__y)
        elif direction == "right":
            self.update_pos(self.__x + self.__length + 1, self.__y)
    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def set_colour(self, colour):
        self.__colour = colour
    
    def get_colour(self):
        return self.__colour

class Chaser:
    def __init__(self, screen, grid, player, colour = (255, 127, 255)):
        self.__screen = screen
        self.__grid = grid
        self.__player = player
        # null values for its position
        self.__pos = [None, None]
        self.__x = None
        self.__y = None
        self.__colour = colour
        self.__length = grid.get_length() # how long to make the square
        # settings that define how the chaser moves
        self.__algorithm = "a*"
        self.__order = ["up", "right", "down", "left"]
        self.__speed = 1
        self.__target = "player"

    def display_chaser(self):
        if self.__x != None and self.__y != None: # only display if it has been placed
            pygame.draw.rect(self.__screen, self.__colour, (self.__x, self.__y, self.__length, self.__length))
    
    def update_pos(self, x, y):
        pos = self.__grid.xy_to_ij(x, y) # change to grid position
        if pos != [None, None]:
            self.__pos = pos
            if self.__grid.get_state(pos[0], pos[1]) != "wall":
                self.__x, self.__y = self.__grid.ij_to_xy(pos[0], pos[1]) # change back to screen position
    
    def run(self):
        if self.__pos != [None, None]:
            self.__grid.set_start(self.__x, self.__y) # set the start to the chaser
            self.set_end() # set the goal it is working towards

            num_order = [None, None, None, None]
            # convert the order from a list of string to a list of numbers
            for i in range(len(self.__order)):
                if self.__order[i] == "up":
                    num_order[0] = i
                elif self.__order[i] == "right":
                    num_order[1] = i
                elif self.__order[i] == "down":
                    num_order[2] = i
                elif self.__order[i] == "left":
                    num_order[3] = i
            self.__grid.update_neighbours(up = num_order[0], right = num_order[1], down = num_order[2], left = num_order[3]) # change the ordering of the neighbours
            
            # create the pathfinding object
            if self.__algorithm == "a*":
                pathfind = Astar(self.__grid)
            elif self.__algorithm == "dijkstra":
                pathfind = Dijkstra(self.__grid)
            elif self.__algorithm == "breadth":
                pathfind = Breadth(self.__grid)
            elif self.__algorithm == "depth":
                pathfind = Depth(self.__grid)

            path = []
            if self.__grid.get_start() != None and self.__grid.get_end() != None:
                path = pathfind.run() # run the pathfinding algorithm
            if len(path) > 1:
                # move the chaser
                x, y = path[1].get_pos()
                self.update_pos(x, y)
    
    def set_end(self):
        self.__grid.set_end(self.__player.get_x(), self.__player.get_y())
        if self.__target == "ahead" or self.__target == "behind":
            node = self.__grid.get_end()
            stack = Stack() # create a stack

            for i in range(3): # move three tiles away from the player
                neighbours = node.get_neighbours()
                if self.__target == "ahead":
                    neighbours = neighbours[::-1] # reverse the neighbour list to go backwards
                
                #add the neighbours to a stack
                for i in neighbours:
                    if i != None:
                        stack.push(i)
                if not stack.empty():
                    node = stack.pull() # move to the next neighbour
            # change the location of the end
            x, y = node.get_pos()
            self.__grid.set_end(x, y)
        
        elif self.__target == "corner" or self.__target == "straight":
            node = self.__grid.get_end()
            queue = Queue() # create a queue
            queue.push(node) # add the position of the player to the queue
            
            found = False
            while not found and not queue.empty():
                node = queue.pull()
                neighbours = node.get_neighbours()
                # only take the objects from the neighbour list
                filtered = []
                for i in neighbours:
                    if i != None:
                        filtered.append(i)
                
                # corners or open spaces have three or four neighbours
                if self.__target == "corner":
                    if len(filtered) > 2:
                        found = True
                # strights or enclosed spaces has one or two neighbours
                elif self.__target == "straight":
                    if len(filtered) < 3:
                        found = True
                for i in filtered:
                    queue.push(i) # add the neighbours to a queue
            # change the location of the end
            x, y = node.get_pos()
            self.__grid.set_end(x, y)
    
    def file_export(self, path):
        settings = []
        # add all the settings to a list
        settings.append(self.__pos)
        settings.append(self.__colour)
        settings.append(self.__algorithm)
        settings.append(self.__order)
        settings.append(self.__speed)
        settings.append(self.__target)
        chaser_file = open(path, "w") # open the file
        # add each setting on a new line
        for i in settings:
            i = str(i) + "\n"
            chaser_file.write(i)
        chaser_file.close() # close the file

    def set_algorithm(self, algorithm):
        self.__algorithm = algorithm
    
    def get_algorithm(self):
        return self.__algorithm
    
    def set_order(self, order):
        self.__order = order
    
    def get_order(self):
        return self.__order
    
    def set_speed(self, speed):
        self.__speed = speed
    
    def get_speed(self):
        return self.__speed
    
    def set_target(self, target):
        self.__target = target
    
    def get_target(self):
        return self.__target
    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def set_colour(self, colour):
        self.__colour = colour
    
    def get_colour(self):
        return self.__colour