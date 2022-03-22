import pygame
import ctypes
import os

from grid import Grid
from pathfinders import *
from chasers import *

class Titles:
    def __init__(self, screen, grid):
        # screen and grid variables are objects
        # they are passed throughout the program where all other objects contain the memory address of these objects
        # that means that when they are edited elsewhere they are also edited here
        self._screen = screen
        self._grid = grid
        # when this is set to true the class run loop will end and fall back to the prevoius loop or close the program
        self._exited = False
        self._objects = []

    def run(self):
        # defines the basic outline of all needed operations in this program
        while not self._exited:
            self.display_background() # display two squares and border

            for event in pygame.event.get():
                self.check_exit(event) # if the default window close button is pressed it closes that menu / program
                self.check_objects(event) # checks interactions done with the menu screen
            
            self.check_grid() # checks interactions done with the grid screen
            self.display_grid()
            self.display_chasers() # display any players and chasers
            self.display_objects() # displays everything
            pygame.display.update()

    def display_background(self):
        # creates two sqaures with top left corners of (25,25) and (975,25)
        pygame.draw.rect(self._screen, (22, 22, 22), (0, 0, 1900, 950))
        pygame.draw.rect(self._screen, (32, 32, 32), (25, 25, 900, 900))
        pygame.draw.rect(self._screen, (32, 32, 32), (975, 25, 900, 900))
    
    def check_exit(self, event):
        if event.type == pygame.QUIT: # default window X button
            self._exited = True
    
    def check_objects(self, event):
        pass
    
    def check_grid(self):
        pass

    def display_chasers(self):
        pass
    
    def display_objects(self):
        for i in self._objects:
            i.display_object() # displays object in the object list list
    
    def display_grid(self):
        self._grid.display_grid()

class Menu(Titles):
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware() # ensures that the pygame screen opens corretly
        self._screen = pygame.display.set_mode((1900,950))
        self._exited = False
        self._grid = Grid(self._screen, 20, 20) # creates the grid

        self._objects = [ # defines all objects on the menu screen
            Button(self._screen, None, 0, 0, 900, 100, background = (28, 28, 28), text = "Menu"),
            Button(self._screen, "exit", 0, 800, 900, 100, background = (28, 28, 28), text = "Quit"),
            Button(self._screen, "visual", 0, 300, 900, 200, text = "Visualisation Mode"),
            Button(self._screen, "folder", 0, 700, 900, 100, text = "Open Folder"),
            Button(self._screen, "editor", 0, 500, 900, 200, text = "Maze Editor"),
            Button(self._screen, "gamemode", 0, 100, 900, 200, text = "Chaser Development")
        ]
    
    def check_objects(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self._objects:
                if (cmd := i.pressed(pygame.mouse.get_pos())) != None:
                    if cmd == "visual":
                        # run visualisation screen
                        visualise = Visualise(self._screen, self._grid)
                        visualise.run()
                    elif cmd == "exit":
                        self._exited = True
                    elif cmd == "gamemode":
                        # run gamemode settings
                        gamemode = Gamemode(self._screen, self._grid)
                        gamemode.run()
                    elif cmd == "folder":
                        os.startfile(os.getcwd()) # open the directory of the python file
                    elif cmd == "editor":
                        # run the maze editor
                        editor = Editor(self._screen, self._grid)
                        editor.run()

class Visualise(Titles):
    def __init__(self, screen, grid):
        super().__init__(screen, grid)
        self.__algorithm = "a*" # stores the pathfinding algorithm that will be run
        self.__changes = True # stores if the steps are to be shown
        self.__order = ["up", "right", "down", "left"] # the order that the neighbours should be in

        self._objects = [
            Button(self._screen, None, 0, 0, 900, 100, background = (28, 28, 28), text = "Visualisation"),
            Button(self._screen, "exit", 0, 800, 900, 100, background = (28, 28, 28), text = "Quit"),
            Button(self._screen, "editor", 0, 700, 900, 100, text = "Maze Editor"),
            Button(self._screen, None, 0, 100, 900, 100, background = (65, 65, 65), text = "Algorithms"),
            Button(self._screen, None, 0, 400, 900, 100, background = (65, 65, 65), text = "Controls"),
            Button(self._screen, "reset", 225, 500, 225, 100, text = "Reset"),
            Button(self._screen, "run", 0, 500, 225, 100, text = "Run"),
            Button(self._screen, None, 450, 500, 225, 100, text = "Steps"),
            Button(self._screen, "position1", 0, 600, 225, 100, text = self.__order[0].title()),
            Button(self._screen, "position2", 225, 600, 225, 100, text = self.__order[1].title()),
            Button(self._screen, "position3", 450, 600, 225, 100, text = self.__order[2].title()),
            Button(self._screen, "position4", 675, 600, 225, 100, text = self.__order[3].title()),
            Button(self._screen, "changes", 675, 500, 225, 100, text = str(self.__changes)),
            Button(self._screen, "astar", 0, 200, 300, 100, text = "A*"),
            Button(self._screen, "dijkstra", 300, 200, 300, 100, text = "Dijkstra"),
            Button(self._screen, "breadth", 0, 300, 300, 100, text = "Breadth"),
            Button(self._screen, "depth", 300, 300, 300, 100, text = "Depth"),
            Button(self._screen, "algorithm", 600, 200, 300, 200, background = (29, 28, 28), text = self.__algorithm.title())
        ]
  
    def check_objects(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self._objects:
                if (cmd := i.pressed(pygame.mouse.get_pos())) != None:
                    if cmd == "exit":
                        # reset the grid so that there arent any coloured tiles
                        self._grid.reset()
                        self._exited = True
                    elif cmd == "editor":
                        # run the maze editor
                        editor = Editor(self._screen, self._grid)
                        editor.run()
                    # set the algorithm being used
                    elif cmd == "astar":
                        self.__algorithm = "a*"
                    elif cmd == "dijkstra":
                        self.__algorithm = "dijkstra"
                    elif cmd == "breadth":
                        self.__algorithm = "breadth"
                    elif cmd == "depth":
                        self.__algorithm = "depth"
                    elif cmd == "reset":
                        self._grid.reset() # reset the grid
                    elif cmd == "changes":
                        self.__changes = not self.__changes # change the steps from true to false or false to true
                    # switching the positions around
                    elif cmd == "position1":
                        if event.button == 3:
                            self.__order[0], self.__order[1] = self.__order[1], self.__order[0]
                    elif cmd == "position2":
                        if event.button == 1: # left click
                            self.__order[0], self.__order[1] = self.__order[1], self.__order[0]
                        elif event.button == 3: # right click
                            self.__order[1], self.__order[2] = self.__order[2], self.__order[1]
                    elif cmd == "position3":
                        if event.button == 1:
                            self.__order[1], self.__order[2] = self.__order[2], self.__order[1]
                        elif event.button == 3:
                            self.__order[2], self.__order[3] = self.__order[3], self.__order[2]
                    elif cmd == "position4":
                        if event.button == 1:
                            self.__order[2], self.__order[3] = self.__order[3], self.__order[2]
                    elif cmd == "run":
                        # change the order list from strings to numbers
                        num_order = [None, None, None, None]
                        for i in range(len(self.__order)):
                            if self.__order[i] == "up":
                                num_order[0] = i
                            elif self.__order[i] == "right":
                                num_order[1] = i
                            elif self.__order[i] == "down":
                                num_order[2] = i
                            elif self.__order[i] == "left":
                                num_order[3] = i
                        self._grid.update_neighbours(up = num_order[0], right = num_order[1], down = num_order[2], left = num_order[3])

                        # initialise variables used to store the pathfinders output
                        path = []
                        steps = []
                        # only run if their is a start and end
                        if self._grid.get_start() != None and self._grid.get_end() != None:
                            # create the pathfinding object and run the algorithm
                            if self.__algorithm == "dijkstra":
                                pathfind = Dijkstra(self._grid)
                            elif self.__algorithm == "breadth":
                                pathfind = Breadth(self._grid)
                            elif self.__algorithm == "depth":
                                pathfind = Depth(self._grid)
                            elif self.__algorithm == "a*":
                                pathfind = Astar(self._grid)

                            # if steps were set to on then recieve those
                            if self.__changes:
                                path, steps = pathfind.run(changes = True)
                            else:
                                path = pathfind.run()
                            
                            # display all the steps taken
                            if steps != []:
                                for i in steps:
                                    i[0].set_state(i[1])
                            # display the path taken
                            for i in path:
                                if i.get_state() != (255, 255, 0) and i.get_state() != (0, 0, 255):
                                    i.set_state((255, 0, 255)) # set the nodes state to path

            for i in self._objects:
                cmd = i.get_cmd()
                if cmd == "algorithm":
                    i.set_text(self.__algorithm.title()) # set the algorithm indicator to the correct state
                elif cmd == "changes":
                    i.set_text(str(self.__changes)) # show if changes are being made or not
                # show the order of the postitions
                elif cmd == "position1":
                    i.set_text(self.__order[0].title())
                elif cmd == "position2":
                    i.set_text(self.__order[1].title())
                elif cmd == "position3":
                    i.set_text(self.__order[2].title())
                elif cmd == "position4":
                    i.set_text(self.__order[3].title())

class Editor(Titles):
    def __init__(self, screen, grid):
        super().__init__(screen, grid)
        self.__brush = "wall" # the currently selected state
        self.__height = self._grid.get_height()
        self.__width = self._grid.get_width()

        self._objects = [
            Button(self._screen, None, 0, 0, 900, 100, background = (28, 28, 28), text = "Maze Editor"),
            Button(self._screen, None, 0, 100, 900, 100, background = (65, 65, 65), text = "Maze Tiles"),
            Button(self._screen, "wall", 0, 200, 225, 100, text = "Wall"),
            Button(self._screen, "space", 225, 200, 225, 100, text = "Space"),
            Button(self._screen, "start", 450, 200, 225, 100, text = "Start"),
            Button(self._screen, "end", 675, 200, 225, 100, text = "End"),
            Button(self._screen, None, 0, 300, 675, 100, background = (65, 65, 65), text = "Colour Tiles"),
            Button(self._screen, "open", 0, 400, 225, 100, text = "Open"),
            Button(self._screen, "save", 0, 800, 900, 100, background = (28, 28, 28), text = "Quit"),
            Button(self._screen, "closed", 225, 400, 225, 100, text = "Closed"),
            Button(self._screen, "path", 450, 400, 225, 100, text = "Path"),
            Button(self._screen, "brush", 675, 300, 225, 200, background = (28, 28, 28), text = "Wall"),
            Button(self._screen, None, 0, 500, 900, 100, background = (65, 65, 65), text = "Grid Settings"),
            Button(self._screen, None, 0, 600, 225, 100, text = "Height"),
            Button(self._screen, "height", 225, 600, 225, 100, text = str(self.__height)),
            Button(self._screen, None, 0, 700, 225, 100, text = "Width"),
            Button(self._screen, "width", 225, 700, 225, 100, text = str(self.__width)),
            Button(self._screen, "importer", 450, 700, 450, 100, text = "Importer"),
            Button(self._screen, "recreate", 450, 600, 450, 100, text = "Recreate")
        ]
   
    def check_objects(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self._objects:
                if (cmd := i.pressed(pygame.mouse.get_pos())) != None:
                    # selecting the different states
                    if cmd == "exit":
                        self._exited = True
                    elif cmd == "space":
                        self.__brush = "space"
                    elif cmd == "wall":
                        self.__brush = "wall"
                    elif cmd == "start":
                        self.__brush = "start"
                    elif cmd == "end":
                        self.__brush = "end"
                    elif cmd == "open":
                        self.__brush = "open"
                    elif cmd == "closed":
                        self.__brush = "closed"
                    elif cmd == "path":
                        self.__brush = "path"
                    elif cmd == "save":
                        self._grid.reset() # remove any path, closed or open states from the grid
                        self._grid.update_neighbours() # set the neighbours for each node
                        self._exited = True
                    elif cmd == "height":
                        # if left click and not too high add to the height
                        if event.button == 1:
                            if self.__height < 40:
                                self.__height += 1
                        # if right click and not too low take from the height
                        elif event.button == 3:
                            if self.__height > 5:
                                self.__height -= 1
                    elif cmd == "width":
                        # if left click and not too high add to the width
                        if event.button == 1:
                            if self.__width < 40:
                                self.__width += 1
                        # if right click and not too low take from the width
                        elif event.button == 3:
                            if self.__width > 5:
                                self.__width -= 1
                    elif cmd == "importer":
                        # open the importer menu
                        importer = Importer(self._screen, self._grid)
                        importer.run()
                    elif cmd == "recreate":
                        # recreate the grid with the new width and height
                        self._grid.create_grid(self.__width, self.__height)

            for i in self._objects:
                cmd = i.get_cmd()
                if cmd == "brush":
                    i.set_text(self.__brush.title()) # set the brush indicator to the correct state
                # show the height and width of the grid
                if cmd == "height":
                    i.set_text(str(self.__height))
                if cmd == "width":
                    i.set_text(str(self.__width))
    
    def check_grid(self):
        # change the state of the clicked on node
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            self._grid.update_state(pos[0], pos[1], self.__brush)

            # update the brush indicator again
            for i in self._objects:
                if i.get_cmd() == "brush":
                    i.set_text(self.__brush.title())
                    
        # right click always sets a tile to space
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            self._grid.update_state(pos[0], pos[1], "space")

class Importer(Titles):
    def __init__(self, screen, grid):
        super().__init__(screen, grid)

        self._objects = [
            Button(self._screen, None, 0, 0, 900, 100, background = (28, 28, 28), text = "Importer"),
            Button(self._screen, None, 0, 100, 300, 100, background = (65, 65, 65), text = "Primary"),
            Button(self._screen, "import1", 300, 100, 300, 100, text = "Import"),
            Button(self._screen, "export1", 600, 100, 300, 100, text = "Export"),
            Button(self._screen, None, 0, 200, 300, 100, background = (65, 65, 65), text = "Secondary"),
            Button(self._screen, "import2", 300, 200, 300, 100, text = "Import"),
            Button(self._screen, "export2", 600, 200, 300, 100, text = "Export"),
            Button(self._screen, None, 0, 300, 300, 100, background = (65, 65, 65), text = "Tertiary"),
            Button(self._screen, "import3", 300, 300, 300, 100, text = "Import"),
            Button(self._screen, "export3", 600, 300, 300, 100, text = "Export"),
            Button(self._screen, None, 0, 400, 300, 100, background = (65, 65, 65), text = "Quaternary"),
            Button(self._screen, "import4", 300, 400, 300, 100, text = "Import"),
            Button(self._screen, "export4", 600, 400, 300, 100, text = "Export"),
            Button(self._screen, None, 0, 500, 300, 100, background = (65, 65, 65), text = "Quinary"),
            Button(self._screen, "import5", 300, 500, 300, 100, text = "Import"),
            Button(self._screen, "export5", 600, 500, 300, 100, text = "Export"),
            Button(self._screen, None, 0, 600, 300, 100, background = (65, 65, 65), text = "Senary"),
            Button(self._screen, "import6", 300, 600, 300, 100, text = "Import"),
            Button(self._screen, "export6", 600, 600, 300, 100, text = "Export"),
            Button(self._screen, None, 0, 700, 300, 100, background = (65, 65, 65), text = "Septenary"),
            Button(self._screen, "import7", 300, 700, 300, 100, text = "Import"),
            Button(self._screen, "export7", 600, 700, 300, 100, text = "Export"),
            Button(self._screen, "exit", 0, 800, 900, 100, background = (28, 28, 28), text = "Quit")
        ]
    
    def check_objects(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self._objects:
                if (cmd := i.pressed(pygame.mouse.get_pos())) != None:
                    if cmd == "exit":
                        self._exited = True
                    # activation of the import and export buttons
                    elif cmd == "import1":
                        self._grid.file_import("grids/primary.txt")
                    elif cmd == "export1":
                        self._grid.file_export("grids/primary.txt")
                    elif cmd == "import2":
                        self._grid.file_import("grids/secondary.txt")
                    elif cmd == "export2":
                        self._grid.file_export("grids/secondary.txt")
                    elif cmd == "import3":
                        self._grid.file_import("grids/tertiary.txt")
                    elif cmd == "export3":
                        self._grid.file_export("grids/tertiary.txt")
                    elif cmd == "import4":
                        self._grid.file_import("grids/quarternary.txt")
                    elif cmd == "export4":
                        self._grid.file_export("grids/quarternary.txt")
                    elif cmd == "import5":
                        self._grid.file_import("grids/quinary.txt")
                    elif cmd == "export5":
                        self._grid.file_export("grids/quinary.txt")
                    elif cmd == "import6":
                        self._grid.file_import("grids/senary.txt")
                    elif cmd == "export6":
                        self._grid.file_export("grids/senary.txt")
                    elif cmd == "import7":
                        self._grid.file_import("grids/septenary.txt")
                    elif cmd == "export7":
                        self._grid.file_export("grids/septenary.txt")

class Gamemode(Titles):
    def __init__(self, screen, grid):
        super().__init__(screen, grid)
        self.__player = Player(self._screen, self._grid) # create the player objects
        self.__chasers = [None, None, None, None, None, None, None] # list containing null values to be replaced by chasers
        self.__mode = "turned" # the mode that is selected
        self.__time = 1800 # time is defined as 30 per second
        self.__turns = 20 # how many turns the player will have

        self._objects = [
            Button(self._screen, "exit", 0, 800, 900, 100, background = (28, 28, 28), text = "Quit"),
            Button(self._screen, None, 0, 0, 900, 100, background = (28, 28, 28), text = "Chaser Development"),
            Button(self._screen, "editor", 0, 700, 900, 100, text = "Maze Editor"),
            Button(self._screen, "selection", 0, 500, 900, 100, text = "Chaser Editor"),
            Button(self._screen, "reset", 0, 600, 450, 100, text = "Reset"),
            Button(self._screen, "export", 450, 600, 450, 100, text = "Export"),
            Button(self._screen, "run", 600, 300, 300, 100, text = "Run"),
            Button(self._screen, None, 0, 400, 900, 100, background = (65, 65, 65), text = "Editors"),
            Button(self._screen, None, 0, 100, 900, 100, background = (65, 65, 65), text = "Controls"),
            Button(self._screen, "turned", 0, 200, 300, 100, text = "Turned"),
            Button(self._screen, "timed", 300, 200, 300, 100, text = "Timed"),
            Button(self._screen, "mode", 600, 200, 300, 100, background = (28, 28, 28), text = self.__mode.title()),
            Button(self._screen, "turns", 0, 300, 300, 100, text = str(self.__turns)),
            Button(self._screen, "time", 300, 300, 300, 100, text = "01:00")
        ]
    
    def check_objects(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self._objects:
                if (cmd := i.pressed(pygame.mouse.get_pos())) != None:
                    if cmd == "exit":
                        self._exited = True
                    elif cmd == "editor":
                        # run the maze editor
                        editor = Editor(self._screen, self._grid)
                        editor.run()
                        self.reset()
                    elif cmd == "selection":
                        # run the selection screen
                        selection = Selection(self._screen, self._grid, self.__player, self.__chasers)
                        selection.run()
                    elif cmd == "reset":
                        self.reset() # reset the player and chasers
                    elif cmd == "run":
                        # only run if there is a player and an end goal
                        if self.__player.get_pos()[0] != None and self.__player.get_pos()[1] != None:
                            if self._grid.get_end() != None:
                                # open the chaser gamemode
                                if self.__mode == "timed":
                                    chase = Chase(self._screen, self._grid, self.__player, self.__chasers, self.__mode, self.__time)
                                    chase.run()
                                elif self.__mode == "turned":
                                    chase = Chase(self._screen, self._grid, self.__player, self.__chasers, self.__mode, self.__turns)
                                    chase.run()
                    # selecting a gamemode
                    elif cmd == "turned":
                        self.__mode = "turned"
                    elif cmd == "timed":
                        self.__mode = "timed"
                    elif cmd == "time":
                        # change the time up or down by a minute
                        if event.button == 1: # left click
                            if self.__time < 18000:
                                self.__time += 1800
                        if event.button == 3: # right click
                            if self.__time > 1800:
                                self.__time -= 1800
                    elif cmd == "turns":
                        # change the turns up or down by 10
                        if event.button == 1:
                            if self.__turns < 400:
                                self.__turns += 10
                        elif event.button == 3:
                            if self.__turns > 10:
                                self.__turns -= 10
                    elif cmd == "export":
                        # export the settings for each chaser
                        for i in range(len(self.__chasers)):
                            if self.__chasers[i] != None:
                                path = "chasers/chaser" + str(i) + ".txt"
                                self.__chasers[i].file_export(path)
            
            for i in self._objects:
                cmd = i.get_cmd()
                # show the mode, turns and time that the player will have
                if cmd == "mode":
                    i.set_text(self.__mode.title())
                elif cmd == "turns":
                    i.set_text(str(self.__turns))
                elif cmd == "time":
                    time = self.__time
                    time1 = time // 18000
                    time -= time1 * 18000
                    time2 = time // 1800
                    time -= time2 * 1800
                    time3 = time // 300
                    time -= time3 * 300
                    time4 = time // 30
                    i.set_text(str(time1)[0] + str(time2)[0] + ":" + str(time3)[0] + str(time4)[0])

    def check_grid(self):
        # left click places the player
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            self.__player.update_pos(pos[0], pos[1])

    def display_chasers(self):
        self.__player.display_player() # display the player
        # display all the chasers
        for i in self.__chasers:
            if i != None:
                i.display_chaser()
    
    def reset(self):
        # recreate the player and delete all of the chasers
        self.__player = Player(self._screen, self._grid)
        self.__chasers = [None, None, None, None, None, None, None]

class Selection(Titles):
    def __init__(self, screen, grid, player, chasers):
        super().__init__(screen, grid)
        self.__player = player
        self.__chasers = chasers
        
        self._objects = [
            Button(self._screen, "exit", 0, 800, 900, 100, background = (28, 28, 28), text = "Quit"),
            Button(self._screen, None, 0, 0, 900, 100, background = (28, 28, 28), text = "Select Chaser"),
            Button(self._screen, None, 0, 100, 300, 100, background = (65, 65, 65), text = "Chaser 1"),
            Button(self._screen, "create1", 300, 100, 300, 100, text = "Create"),
            Button(self._screen, "edit1", 600, 100, 300, 100, text = "Edit"),
            Button(self._screen, None, 0, 200, 300, 100, background = (65, 65, 65), text = "Chaser 2"),
            Button(self._screen, "create2", 300, 200, 300, 100, text = "Create"),
            Button(self._screen, "edit2", 600, 200, 300, 100, text = "Edit"),
            Button(self._screen, None, 0, 300, 300, 100, background = (65, 65, 65), text = "Chaser 3"),
            Button(self._screen, "create3", 300, 300, 300, 100, text = "Create"),
            Button(self._screen, "edit3", 600, 300, 300, 100, text = "Edit"),
            Button(self._screen, None, 0, 400, 300, 100, background = (65, 65, 65), text = "Chaser 4"),
            Button(self._screen, "create4", 300, 400, 300, 100, text = "Create"),
            Button(self._screen, "edit4", 600, 400, 300, 100, text = "Edit"),
            Button(self._screen, None, 0, 500, 300, 100, background = (65, 65, 65), text = "Chaser 5"),
            Button(self._screen, "create5", 300, 500, 300, 100, text = "Create"),
            Button(self._screen, "edit5", 600, 500, 300, 100, text = "Edit"),
            Button(self._screen, None, 0, 600, 300, 100, background = (65, 65, 65), text = "Chaser 6"),
            Button(self._screen, "create6", 300, 600, 300, 100, text = "Create"),
            Button(self._screen, "edit6", 600, 600, 300, 100, text = "Edit"),
            Button(self._screen, None, 0, 700, 300, 100, background = (65, 65, 65), text = "Chaser 7"),
            Button(self._screen, "create7", 300, 700, 300, 100, text = "Create"),
            Button(self._screen, "edit7", 600, 700, 300, 100, text = "Edit")
        ]
    
    def check_objects(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self._objects:
                # check if the user clicked on create or edit
                create = False
                edit = False
                num = None # the number the user clicked on
                colour = () # colour of the chaser
                if (cmd := i.pressed(pygame.mouse.get_pos())) != None:
                    if cmd == "exit":
                        self._exited = True
                    elif cmd == "create1":
                        num = 0
                        create = True
                        colour = (127, 255, 255)
                    elif cmd == "create2":
                        num = 1
                        create = True
                        colour = (255, 127, 255)
                    elif cmd == "create3":
                        num = 2
                        create = True
                        colour = (255, 255, 127)
                    elif cmd == "create4":
                        num = 3
                        create = True
                        colour = (255, 127, 127)
                    elif cmd == "create5":
                        num = 4
                        create = True
                        colour = (127, 255, 127)
                    elif cmd == "create6":
                        num = 5
                        create = True
                        colour = (127, 127, 255)
                    elif cmd == "create7":
                        num = 6
                        create = True
                        colour = (127, 127, 127)
                    elif cmd == "edit1":
                        num = 0
                        edit = True
                    elif cmd == "edit2":
                        num = 1
                        edit = True
                    elif cmd == "edit3":
                        num = 2
                        edit = True
                    elif cmd == "edit4":
                        num = 3
                        edit = True
                    elif cmd == "edit5":
                        num = 4
                        edit = True
                    elif cmd == "edit6":
                        num = 5
                        edit = True
                    elif cmd == "edit7":
                        num = 6
                        edit = True
                
                if create:
                    # create a new chaser and open up its settings menu
                    self.__chasers[num] = Chaser(self._screen, self._grid, self.__player, colour = colour)
                    settings = Settings(self._screen, self._grid, self.__player, self.__chasers, num)
                    settings.run()
                if edit:
                    if self.__chasers[num] != None:
                        # open the settings menu for the chaser
                        settings = Settings(self._screen, self._grid, self.__player, self.__chasers, num)
                        settings.run()
    
    def display_chasers(self):
        self.__player.display_player()
        for i in self.__chasers:
            if i != None:
                i.display_chaser()

class Settings(Titles):
    def __init__(self, screen, grid, player, chasers, num):
        super().__init__(screen, grid)
        self.__player = player
        self.__chasers = chasers
        self.__chaser = chasers[num] # the currently selected chaser
        # all the settings that define how the chaser moves
        self.__algorithm = self.__chaser.get_algorithm()
        self.__order = self.__chaser.get_order()
        self.__speed = self.__chaser.get_speed()
        self.__target = self.__chaser.get_target()
        
        self._objects = [
            Button(self._screen, "exit", 0, 800, 900, 100, background = (28, 28, 28), text = "Quit"),
            Button(self._screen, None, 0, 0, 900, 100, background = (28, 28, 28), text = "Chaser Settings"),
            Button(self._screen, "astar", 0, 200, 300, 100, text = "A*"),
            Button(self._screen, "dijkstra", 300, 200, 300, 100, text = "Dijkstra"),
            Button(self._screen, "breadth", 0, 300, 300, 100, text = "Breadth"),
            Button(self._screen, "depth", 300, 300, 300, 100, text = "Depth"),
            Button(self._screen, "algorithm", 600, 200, 300, 200, background = (29, 28, 28), text = self.__algorithm.title()),
            Button(self._screen, None, 0, 100, 900, 100, background = (65, 65, 65), text = "Algorithms"),
            Button(self._screen, "position1", 0, 700, 225, 100, text = self.__order[0].title()),
            Button(self._screen, "position2", 225, 700, 225, 100, text = self.__order[1].title()),
            Button(self._screen, "position3", 450, 700, 225, 100, text = self.__order[2].title()),
            Button(self._screen, "position4", 675, 700, 225, 100, text = self.__order[3].title()),
            Button(self._screen, None, 0, 400, 675, 100, background = (65, 65, 65), text = "Movement"),
            Button(self._screen, None, 450, 600, 225, 100, text = "Speed"),
            Button(self._screen, "speed", 675, 600, 225, 100, text = str(self.__speed)),
            Button(self._screen, "target", 675, 400, 225, 200, background = (28, 28, 28), text = self.__target.title()),
            Button(self._screen, "player", 0, 500, 225, 100, text = "Player"),
            Button(self._screen, "ahead", 225, 500, 225, 100, text = "Ahead"),
            Button(self._screen, "behind", 450, 500, 225, 100, text = "Behind"),
            Button(self._screen, "corner", 0, 600, 225, 100, text = "Corner"),
            Button(self._screen, "straight", 225, 600, 225, 100, text = "Straight")
        ]
    
    def check_objects(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self._objects:
                if (cmd := i.pressed(pygame.mouse.get_pos())) != None:
                    if cmd == "exit":
                        self._exited = True
                    # select the algorithm to be used
                    elif cmd == "astar":
                        self.__algorithm = "a*"
                    elif cmd == "dijkstra":
                        self.__algorithm = "dijkstra"
                    elif cmd == "breadth":
                        self.__algorithm = "breadth"
                    elif cmd == "depth":
                        self.__algorithm = "depth"
                    # change the order of the directions
                    elif cmd == "position1":
                        if event.button == 3:
                            self.__order[0], self.__order[1] = self.__order[1], self.__order[0]
                    elif cmd == "position2":
                        if event.button == 1: # left click
                            self.__order[0], self.__order[1] = self.__order[1], self.__order[0]
                        elif event.button == 3: # right click
                            self.__order[1], self.__order[2] = self.__order[2], self.__order[1]
                    elif cmd == "position3":
                        if event.button == 1:
                            self.__order[1], self.__order[2] = self.__order[2], self.__order[1]
                        elif event.button == 3:
                            self.__order[2], self.__order[3] = self.__order[3], self.__order[2]
                    elif cmd == "position4":
                        if event.button == 1:
                            self.__order[2], self.__order[3] = self.__order[3], self.__order[2]
                    elif cmd == "speed":
                        # change the speed up or down by 1 skipping 0
                        if event.button == 1:
                            if 0 < self.__speed < 3:
                                self.__speed += 1
                            elif self.__speed == -1:
                                self.__speed = 1
                            elif self.__speed == -2:
                                self.__speed = -1
                        elif event.button == 3:
                            if 1 < self.__speed < 4:
                                self.__speed -= 1
                            elif self.__speed == 1:
                                self.__speed = -1
                            elif self.__speed == -1:
                                self.__speed = -2
                    # select the target mode of the chaser
                    elif cmd == "player":
                        self.__target = "player"
                    elif cmd == "ahead":
                        self.__target = "ahead"
                    elif cmd == "behind":
                        self.__target = "behind"
                    elif cmd == "corner":
                        self.__target = "corner"
                    elif cmd == "straight":
                        self.__target = "straight"

            # assign the chaser its settings
            self.__chaser.set_algorithm(self.__algorithm)
            self.__chaser.set_order(self.__order)
            self.__chaser.set_speed(self.__speed)
            self.__chaser.set_target(self.__target)
            for i in self._objects:
                cmd = i.get_cmd()
                # show the settings on the menu
                if cmd == "algorithm":
                    i.set_text(self.__chaser.get_algorithm().title())
                elif cmd == "position1":
                    i.set_text(self.__chaser.get_order()[0].title())
                elif cmd == "position2":
                    i.set_text(self.__chaser.get_order()[1].title())
                elif cmd == "position3":
                    i.set_text(self.__chaser.get_order()[2].title())
                elif cmd == "position4":
                    i.set_text(self.__chaser.get_order()[3].title())
                elif cmd == "speed":
                    i.set_text(str(self.__chaser.get_speed()))
                elif cmd == "target":
                    i.set_text(self.__chaser.get_target().title())

    def check_grid(self):
        if pygame.mouse.get_pressed()[0]:
            # place the chaser if the user clicks on the grid
            pos = pygame.mouse.get_pos()
            self.__chaser.update_pos(pos[0], pos[1])
    
    def display_chasers(self):
        self.__player.display_player()
        for i in self.__chasers:
            if i != None:
                i.display_chaser()

class Chase(Titles):
    def __init__(self, screen, grid, player, chasers, mode, num):
        super().__init__(screen, grid)
        self.__player = player
        self.__chasers = chasers
        self.__mode = mode # the mode being used
        self.__past_pos = self.__player.get_pos() # the previous position of the player to check for movement
        # how long the player has to win
        self.__turns = 0
        self.__time = 0
        if self.__mode == "timed":
            self.__time = num
        elif self.__mode == "turned":
            self.__turns = num
        self.__clock = pygame.time.Clock() # clock to keep the game at 30fps in timed mode
        self.__x, self.__y = self._grid.get_end().get_pos() # position of the end goal

        self._objects = [
            Button(self._screen, "exit", 0, 800, 900, 100, background = (28, 28, 28), text = "Quit"),
            Button(self._screen, None, 0, 0, 900, 100, background = (28, 28, 28), text = "Chase"),
            Button(self._screen, "up", 0, 300, 900, 200, text = "Up"),
            Button(self._screen, "down", 0, 600, 900, 200, text = "Down"),
            Button(self._screen, "left", 0, 500, 450, 100, text = "Left"),
            Button(self._screen, "right", 450, 500, 450, 100, text = "Right"),
            Button(self._screen, "timer", 225, 100, 225, 100, text = "00:00"),
            Button(self._screen, None, 0, 100, 225, 100, text = "Timer"),
            Button(self._screen, None, 450, 100, 225, 100, text = "Turns"),
            Button(self._screen, "turns", 675, 100, 225, 100, text = str(self.__turns)),
            Button(self._screen, None, 0, 200, 900, 100, background = (65, 65, 65), text = "Controls")
        ]
    
    def check_objects(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self._objects:
                if (cmd := i.pressed(pygame.mouse.get_pos())) != None:
                    if cmd == "exit":
                        self._exited = True
                    # check if the player clicked a movement button
                    elif cmd == "up":
                        self.__player.move("up")
                    elif cmd == "down":
                        self.__player.move("down")
                    elif cmd == "left":
                        self.__player.move("left")
                    elif cmd == "right":
                        self.__player.move("right")

        for i in self._objects:
            cmd = i.get_cmd()
            if cmd == "timer":
                if self.__mode == "timed":
                    # convet the time into a clock
                    time = self.__time
                    time1 = time // 18000
                    time -= time1 * 18000
                    time2 = time // 1800
                    time -= time2 * 1800
                    time3 = time // 300
                    time -= time3 * 300
                    time4 = time // 30
                    i.set_text(str(time1)[0] + str(time2)[0] + ":" + str(time3)[0] + str(time4)[0])
            if cmd == "turns":
                if self.__mode == "turned":
                    i.set_text(str(self.__turns)) # show how many turns left
    
    def display_chasers(self):
        self.__player.display_player()
        for i in self.__chasers:
            if i != None:
                i.display_chaser()
    
    def run(self):
        while not self._exited:
            self.display_background()

            for event in pygame.event.get():
                self.check_exit(event)
                self.check_objects(event)
            
            if self.__mode == "turned":
                # check for player movement
                if self.__player.get_pos() != self.__past_pos:
                    self.__past_pos = self.__player.get_pos() # update the position
                    self.__turns -= 1 # remove a turn
                    for i in self.__chasers:
                        if i != None:
                            # move the chasers depending on their speed
                            speed = i.get_speed()
                            if speed > 0:
                                for j in range(speed):
                                    i.run()
                            elif speed < 0:
                                if self.__turns % (abs(speed) + 1) == 0:
                                    i.run()
            
            elif self.__mode == "timed":
                self.__time -= 1
                for i in self.__chasers:
                    if i != None:
                        # move the chasers depending on their speed
                        speed = i.get_speed()
                        if speed > 0:
                            if self.__time % (60 * speed) == 0:
                                i.run()
                        elif speed < 0:
                            if self.__time % ((1 / (abs(speed) + 1)) * 30) == 0:
                                i.run()

            self.check_grid()
            # show the end goal
            self._grid.set_start(self.__x + 1, self.__y + 1)
            self._grid.set_end(self.__x + 1, self.__y + 1)
            self.display_grid()
            self.display_chasers()
            self.display_objects()
            pygame.display.update()
            # check if the game has been lost or won
            if self.__mode == "timed":
                self.__clock.tick(30)
                if self.__time < 10:
                    self.lost() # time ran out
            elif self.__mode == "turned":
                if self.__turns == 0:
                    self.lost() # out of turns
            if self.__player.get_x() == self.__x and self.__player.get_y() == self.__y:
                self.won() # player reached the end goal
            for i in self.__chasers:
                if i != None:
                    if i.get_x() == self.__player.get_x() and i.get_y() == self.__player.get_y():
                        self.lost() # player got caught up to and lost
    
    def won(self):
        self._exited = True
    
    def lost(self):
        self._exited = True

class Button:
    def __init__(self, screen, cmd, x, y, width, height, background = (50, 50, 50), text = "", colour = (222, 222, 222), style = "Arial", size = 50):
        self.__screen = screen
        self.__cmd = cmd
        # position variables
        self.__x = x + 25
        self.__y = y + 25
        self.__width = width
        self.__height = height
        self.__background = background # colour of the button
        # text related variables
        self.__colour = colour
        self.__style = pygame.font.SysFont(style, size)
        self.__text = self.__style.render(text, False, colour)
        self.__rect = self.__text.get_rect(center = (self.__x + self.__width // 2, self.__y + self.__height // 2))
    
    def display_object(self):
        # draw the button and its text
        pygame.draw.rect(self.__screen, self.__background, (self.__x, self.__y, self.__width, self.__height))
        self.__screen.blit(self.__text, self.__rect)

    def pressed(self, pos):
        # check if the button was pressed
        if self.__x <= pos[0] <= self.__x + self.__width:
            if self.__y <= pos[1] <= self.__y + self.__height:
                return self.__cmd
        return None
    
    def get_cmd(self):
        return self.__cmd
    
    def set_text(self, text):
        # update the text on the buttom
        self.__text = self.__style.render(text, False, self.__colour)
        self.__rect = self.__text.get_rect(center = (self.__x + self.__width // 2, self.__y + self.__height // 2))

if __name__ == "__main__":
    # required init commands
    pygame.display.init()
    pygame.font.init()
    # create and run the menu system
    menu = Menu()
    menu.run()
