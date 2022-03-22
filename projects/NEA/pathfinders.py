from priority import Priority
from queue import Queue
from stack import Stack

class Dijkstra:
    def __init__(self, grid):
        self.__grid = grid
        self.__start = self.__grid.get_start()
        self.__end = self.__grid.get_end()
        self.__queue = Priority()
    
    def run(self, changes = False):
        path = []
        steps = [] # list containing all state changes that are made
        self.__grid.reset() # resets the grid back to a pre solved state
        self.__start.set_distance(0) # sets the starting distance to 0
        self.__queue.push(self.__start, 0) # adds the starting node to the queue

        found = False
        # main loop that runs untill the end is found or cannot be found
        while not found and not self.__queue.empty():
            current = self.__queue.pull()[0] # take the node with the shortest distance
            # set the node to closed if its is not the start or end node
            if current.get_state() != (255, 255, 0) and current.get_state() != (0, 0, 255):
                current.set_state((255, 0, 0))
                steps.append([current, (255, 0, 0)])

            # for every neighbour that the current node has
            for i in current.get_neighbours():
                if i != None:
                    if i.get_state() != (255, 255, 0) and i.get_state() != (255, 0, 0):
                        distance = current.get_distance() + 1 # calcualte its new distance
                        if distance < i.get_distance():
                            i.set_distance(distance) # update node to shortest distance
                            # if the node is first time visited then change it to an open state
                            if i.get_state() != (0, 0, 255):
                                if i.get_state() != (0, 255, 0):
                                    i.set_state((0, 255, 0)) # set the state to open
                                    steps.append([i, (0, 255, 0)])
                                    self.__queue.push(i, distance) # add to the priority queue
                                else:
                                    self.__queue.reweigh(i, distance) # change its place in the queue
                            else:
                                # if it is the end mode then dont change its state
                                if self.__queue.search(i):
                                    self.__queue.reweigh(i, distance)
                                else:
                                    self.__queue.push(i, distance)
                            # create and assign its new path
                            path = current.get_path()[:]
                            path.append(current)
                            i.set_path(path)
            
            # end the while loop once the end has been found
            if current.get_state() == (0, 0, 255):
                found = True
        
        # obtain the final path taken
        path = self.__end.get_path()
        path.append(self.__end)
        self.__grid.reset()
        # return the values that were requested
        if changes:
            return path, steps
        else:
            return path

class Astar:
    def __init__(self, grid):
        self.__grid = grid
        self.__start = self.__grid.get_start()
        self.__end = self.__grid.get_end()
        self.__queue = Priority()

    def run(self, changes = False):
        path = []
        steps = [] # list containing all state changes that are made
        self.__grid.reset() # resets the grid back to a pre solved state
        self.__start.set_distance(0) # sets the starting distance to 0
        self.__queue.push(self.__start, 0) # adds the starting node to the queue
        x1, y1 = self.__grid.get_pos(self.__end)

        found = False
        # main loop that runs untill the end is found or cannot be found
        while not found and not self.__queue.empty():
            current = self.__queue.pull()[0] # take the node with the shortest distance
            # set the node to closed if its is not the start or end node
            if current.get_state() != (255, 255, 0) and current.get_state() != (0, 0, 255):
                current.set_state((255, 0, 0))
                steps.append([current, (255, 0, 0)])

            # for every neighbour that the current node has
            for i in current.get_neighbours():
                if i != None:
                    if i.get_state() != (255, 255, 0) and i.get_state() != (255, 0, 0):
                        distance = current.get_distance() + 1 # calcualte its new distance
                        # calculate the heuristic distance
                        x2, y2 = self.__grid.get_pos(i)
                        heuristic = abs(x2 - x1) + abs(y2 - y1)
                        weight = self.__queue.get_weight(i)
                        if weight == None:
                            weight = 1000
                        # weight is the addition of the distance from the start and the heuristic value
                        # the node stores the distance and the queue stores the weight
                        if distance + heuristic < weight:
                            i.set_distance(distance) # update node to shortest distance
                            # if the node is first time visited then change it to an open state
                            if i.get_state() != (0, 0, 255):
                                if i.get_state() != (0, 255, 0):
                                    i.set_state((0, 255, 0)) # set state to open
                                    steps.append([i, (0, 255, 0)])
                                    self.__queue.push(i, distance + heuristic) # add to the priority queue
                                else:
                                    self.__queue.reweigh(i, distance + heuristic) # change its place in the queue
                            else:
                                # if it is the end node then dont change the state
                                if self.__queue.search(i):
                                    self.__queue.reweigh(i, distance + heuristic)
                                else:
                                    self.__queue.push(i, distance + heuristic)
                            # create and assign its new path
                            path = current.get_path()[:]
                            path.append(current)
                            i.set_path(path)
            
            # end the while loop once the end has been found
            if current.get_state() == (0, 0, 255):
                found = True
        
        # obtain the final path taken
        path = self.__end.get_path()
        path.append(self.__end)
        self.__grid.reset()
        # return the values that were requested
        if changes:
            return path, steps
        else:
            return path

class Breadth:
    def __init__(self, grid):
        self.__grid = grid
        self.__start = self.__grid.get_start()
        self.__end = self.__grid.get_end()
        self.__queue = Queue()

    def run(self, changes = False):
        path = []
        steps = [] # list containing all state changes that are made
        self.__grid.reset() # resets the grid back to a pre solved stat
        self.__queue.push(self.__start) # adds the starting node to the queue

        found = False
        # main loop that runs untill the end is found or cannot be found
        while not found and not self.__queue.empty():
            current = self.__queue.pull() # take the first node in the list
            # set the node to closed if its is not the start or end node
            if current.get_state() != (255, 255, 0) and current.get_state() != (0, 0, 255):
                current.set_state((255, 0, 0))
                steps.append([current, (255, 0, 0)])

            # for every neighbour that the current node has
            for i in current.get_neighbours():
                if i != None:
                    if i.get_state() != (255, 255, 0) and i.get_state() != (255, 0, 0):
                        # if the node is first time visited then change it to an open state
                        if i.get_state() != (0, 0, 255):
                            i.set_state((0, 255, 0)) # set the state to open
                            steps.append([i, (0, 255, 0)])
                            if not self.__queue.search(i):
                                self.__queue.push(i) # add to the queue
                        else:
                            # dont change the state of the end node
                            if not self.__queue.search(i):
                                self.__queue.push(i)
                        # create and assign its new path
                        path = current.get_path()[:]
                        path.append(current)
                        i.set_path(path)
            
            # end the while loop once the end has been found
            if current.get_state() == (0, 0, 255):
                found = True
        
        # obtain the final path taken
        path = self.__end.get_path()
        path.append(self.__end)
        self.__grid.reset()
        # return the values that were requested
        if changes:
            return path, steps
        else:
            return path

class Depth:
    def __init__(self, grid):
        self.__grid = grid
        self.__start = self.__grid.get_start()
        self.__end = self.__grid.get_end()
        self.__stack = Stack()

    def run(self, changes = False):
        path = []
        steps = [] # list containing all state changes that are made
        self.__grid.reset() # resets the grid back to a pre solved stat
        self.__stack.push(self.__start) # adds the starting node to the stack

        found = False
        # main loop that runs untill the end is found or cannot be found
        while not found and not self.__stack.empty():
            current = self.__stack.pull() # take the first node in the stack
            # set the node to closed if its is not the start or end node
            if current.get_state() != (255, 255, 0) and current.get_state() != (0, 0, 255):
                current.set_state((255, 0, 0))
                steps.append([current, (255, 0, 0)])

            # for every neighbour that the current node has
            for i in current.get_neighbours():
                if i != None:
                    if i.get_state() != (255, 255, 0) and i.get_state() != (255, 0, 0):
                        # if the node is first time visited then change it to an open state
                        if i.get_state() != (0, 0, 255):
                            i.set_state((0, 255, 0)) # set the state to open
                            steps.append([i, (0, 255, 0)])
                            if not self.__stack.search(i):
                                self.__stack.push(i) # add to the stack
                        else:
                            # dont change the state of the end node
                            if not self.__stack.search(i):
                                self.__stack.push(i)
                        # create and assign its new path
                        path = current.get_path()[:]
                        path.append(current)
                        i.set_path(path)
            
            # end the while loop once the end has been found
            if current.get_state() == (0, 0, 255):
                found = True
        
        # obtain the final path taken
        path = self.__end.get_path()
        path.append(self.__end)
        self.__grid.reset()
        # return the values that were requested
        if changes:
            return path, steps
        else:
            return path