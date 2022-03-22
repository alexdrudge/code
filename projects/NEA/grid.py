import pygame

# classes generalised for other peoples use
# classes work with any other program given it uses pygame

class Grid:
    def __init__(self, screen, width, height, length = 900, depth = 900, x = 975, y = 25):
        self.__screen = screen
        # save the window config incase grid is resized 
        self.__length = length
        self.__depth = depth
        self.__x = x
        self.__y = y
        self.create_grid(width, height) # make the grid
    
    def create_grid(self, width, height, states = []):
        # save the width and length of the grid
        self.__width = width
        self.__height = height
        # calculate the length of each of the tiles
        node_length = (self.__length - self.__width - 1) // self.__width
        node_depth = (self.__depth - self.__height - 1) // self.__height
        # every tile is square
        if node_length > node_depth:
            node_length = node_depth
        self.__node_length = node_length
        #calculate the extra space needed to centre the grid
        extra_length = (self.__length - (((node_length + 1) * self.__width) + 1)) // 2
        extra_depth = (self.__depth - (((node_length + 1) * self.__height) + 1)) // 2

        # i defines the row, j defines the column
        # [ [a, b, c],
        #   [e, f, g],
        #   [h, i, j] ]
        # grid[1][2] = g
        # read down then across
        self.__grid = []
        # add one to each x and y to create first spacer
        x = self.__x + extra_length + 1
        y = self.__y + extra_depth + 1
        # z stores the value that y needs to reset to
        z = x
        for i in range(self.__height):
            self.__grid.append([])
            for j in range(self.__width):
                if states == []:
                    self.__grid[i].append(Node(self.__screen, x, y, node_length))
                else:
                    self.__grid[i].append(Node(self.__screen, x, y, node_length, states[i][j]))
                x = x + node_length + 1
            y = y + node_length + 1
            x = z

    def display_grid(self):
        # display each node
        for i in range(self.__height):
            for j in range(self.__width):
                self.__grid[i][j].display_node()

    def update_state(self, x, y, state):
        state = self.string_to_colour(state) # convert string states into corresponding colours
        # check each node to see if it was clicked on
        if state == (255, 255, 0):
            self.set_start(x, y)
        elif state == (0, 0, 255):
            self.set_end(x, y)
        else:
            for i in range(self.__height):
                for j in range(self.__width):
                    self.__grid[i][j].update_state(x, y, state)
    
    def set_state(self, i, j, state):
        state = self.string_to_colour(state)
        self.__grid[i][j].set_state(state) # change the state of the node
    
    def get_state(self, i, j):
        state = self.__grid[i][j].get_state()
        return self.colour_to_string(state) # change the colour of the state to the corrosponding string name

    def xy_to_ij(self, x, y):
        for i in range(self.__height):
            for j in range(self.__width):
                # check if the player clicked on the grid
                if self.__grid[i][j].check_press(x, y):
                    return [i, j]
        return [None, None] # return a null value

    def ij_to_xy(self, i, j):
        return self.__grid[i][j].get_pos()

    def string_to_colour(self, state):
        if state == "space":
            return (255, 255, 255)
        elif state == "wall":
            return (0, 0, 0)
        elif state == "start":
            return (255, 255, 0)
        elif state == "end":
            return (0, 0, 255)
        elif state == "open":
            return (0, 255, 0)
        elif state == "closed":
            return (255, 0, 0)
        elif state == "path":
            return (255, 0, 255)
        else: return (255, 255, 255) # prevent import crashes
    
    def colour_to_string(self, state):
        if state == (255, 255, 255):
            return "space"
        elif state == (0, 0, 0):
            return "wall"
        elif state == (255, 255, 0):
            return "start"
        elif state == (0, 0, 255):
            return "end"
        elif state == (0, 255, 0):
            return "open"
        elif state == (255, 0, 0):
            return "closed"
        elif state == (255, 0, 255):
            return "path"

    def update_neighbours(self, up = 0, right = 1, down = 2, left = 3):
        # add neighbours to a node if the are a space on one of the four sides
        for i in range(self.__height):
            for j in range(self.__width):
                neighbours = [None, None, None, None]
                # only check neighbours if its not a wall
                if self.__grid[i][j].get_state() != (0, 0, 0):
                    # check above tile
                    if i != 0:
                        if self.__grid[i-1][j].get_state() != (0, 0, 0):
                            neighbours[up] = self.__grid[i-1][j]
                    # check left tile
                    if j != 0:
                        if self.__grid[i][j-1].get_state() != (0, 0, 0):
                            neighbours[left] = self.__grid[i][j-1]
                    # check below tile
                    if i != self.__height - 1:
                        if self.__grid[i+1][j].get_state() != (0, 0, 0):
                            neighbours[down] = self.__grid[i+1][j]
                    # check right tile
                    if j != self.__width - 1:
                        if self.__grid[i][j+1].get_state() != (0, 0, 0):
                            neighbours[right] = self.__grid[i][j+1]
                self.__grid[i][j].set_neighbours(neighbours) # set the neighbour list

    def set_neighbours(self, i, j, neighbours):
        self.__grid[i][j].set_neighbours(neighbours)

    def get_neighbours(self, i, j):
        return self.__grid[i][j].get_neighbours()

    def set_start(self, x, y):
        start = self.get_start() # save the original start node
        if start != None:
            start.set_state((255, 255, 255)) # reset its state
        for i in range(self.__height):
            for j in range(self.__width):
                self.__grid[i][j].update_state(x, y, (255, 255, 0)) # attempt to set a new start
        # if a new start wasnt placed then replace the new one
        if self.get_start() == None and start != None:
            start.set_state((255, 255, 0))

    def get_start(self):
        for i in range(self.__height):
            for j in range(self.__width):
                # checks if the start node is present
                if self.__grid[i][j].get_state() == (255, 255, 0):
                    return self.__grid[i][j]
        return None
    
    def set_end(self, x, y):
        end = self.get_end() # save the original end node
        if end != None:
            end.set_state((255, 255, 255)) # reset its state
        for i in range(self.__height):
            for j in range(self.__width):
                self.__grid[i][j].update_state(x, y, (0, 0, 255)) # attempt to set a new end
        # if a new end wasnt set then replace the old one
        if self.get_end() == None and end != None:
            end.set_state((0, 0, 255))

    def get_end(self):
        for i in range(self.__height):
            for j in range(self.__width):
                # checks if the end node is present
                if self.__grid[i][j].get_state() == (0, 0, 255):
                    return self.__grid[i][j]
        return None

    def get_pos(self, node):
        for i in range(self.__height):
            for j in range(self.__width):
                if self.__grid[i][j] == node:
                    return i, j # return the two values

    def set_distance(self, i, j, distance):
        self.__grid[i][j].set_distance(distance)

    def get_distance(self, i, j):
        return self.__grid[i][j].get_distance()

    def set_path(self, i, j, path):
        self.__grid[i][j].set_path(path)
    
    def get_path(self, i, j):
        return self.__grid[i][j].get_path()

    def file_export(self, path):
        states = []
        # takes the state of each node and saves it to a nested list
        for i in range(self.__height):
            states.append([])
            for j in range(self.__width):
                states[i].append(self.colour_to_string(self.__grid[i][j].get_state()))
        # opens the file of the given path then writes each state separated by commas and lines
        grid_file = open(path, "w")
        for i in states:
            for j in i:
                j = j + ","
                grid_file.write(j)
            grid_file.write("\n")
        grid_file.close()
    
    def file_import(self, path):
        # opens the specified file and creates a nested list of node states
        grid_file = open(path, "r")
        temp1 = grid_file.readlines()
        grid_file.close()
        temp2 = []
        for i in temp1:
            temp2.append(i.split(","))
        # calculates the size of the imported grid
        height = len(temp2)
        width = len(temp2[0]) - 1 # -1 to remove the \n
        states = []
        # converts the grid from string states to colours
        for i in range(height):
            states.append([])
            for j in range(width):
                states[i].append(self.string_to_colour(temp2[i][j]))
        self.create_grid(width, height, states) # remakes the grid with the new states

    def set_height(self, height):
        self.__height = height

    def get_height(self):
        return self.__height

    def set_width(self, width):
        self.__width = width

    def get_width(self):
        return self.__width

    def get_length(self):
        return self.__node_length

    def reset(self):
        # resets all variables that would have been changed by the pathfidning algorithm
        self.reset_states()
        self.reset_distances()
        self.reset_path()
    
    def reset_states(self):
        # if a nodes state is path, closed or open set it back to space
        for i in self.__grid:
            for j in i:
                if j.get_state() == (255, 0, 0) or j.get_state() == (0, 255, 0) or j.get_state() == (255, 0, 255):
                    j.set_state((255, 255, 255))

    def reset_distances(self):
        # set the distance for every node to 1000 (greater than any possible distance)
        for i in self.__grid:
            for j in i:
                j.set_distance(1000)
    
    def reset_path(self):
        # set the path list for every node to an empty list
        for i in self.__grid:
            for j in i:
                j.set_path([])


        
class Node:
    def __init__(self, screen, x, y, length, state = (255, 255, 255)):
        self.__screen = screen
        # unchangeable variables that define how the node should be displayed
        self.__x = x
        self.__y = y
        self.__length = length
        # initial state of space, colour white
        self.__state = state
        # creates an adjacency list that connects all nodes that are not seperated by walls
        self.__neighbours = []
        # variables needed for pathfinding
        self.__distance = 1000
        self.__path = []
    
    def display_node(self):
        pygame.draw.rect(self.__screen, self.__state, (self.__x, self.__y, self.__length, self.__length))
    
    def set_state(self, state):
        self.__state = state
    
    def get_state(self):
        return self.__state

    def update_state(self, x, y, state):
        # if the mouse click was within the nodes space it changes the state
        if self.__x <= x <= self.__x + self.__length:
            if self.__y <= y <= self.__y + self.__length:
                self.__state = state # changes state if node is clicked on

    def check_press(self, x, y):
        # check if the press was within the range of a tile
        if self.__x <= x <= self.__x + self.__length:
            if self.__y <= y <= self.__y + self.__length:
                return True
        return False
    
    def get_pos(self):
        return self.__x, self.__y

    def set_neighbours(self, neighbours):
        self.__neighbours = neighbours

    def get_neighbours(self):
        return self.__neighbours
    
    def set_distance(self, num):
        self.__distance = num
    
    def get_distance(self):
        return self.__distance
    
    def set_path(self, path):
        self.__path = path
    
    def get_path(self):
        return self.__path