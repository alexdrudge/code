#initialisation of modules
import pygame
pygame.init()
import math
import random
import time
import os

#setup of display
display_window = pygame.display.set_mode((506,552))
pygame.display.set_caption("Mastermind")
display_clock = pygame.time.Clock()
cwd = os.getcwd()

def quit_game():

    print("Game Exited")

    #return game exit
    return True

def quit_play():

    #return game exit
    return True

def quit_reload():

    #return game exit
    return True

def quit_leaderboard():

    #return game exit
    return True

def quit_naming():

    #return game exit
    return True

def reset_code():

    #initialise variables
    code = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1]]
    num = 0

    #randomise colours
    for i in range(4):
        num = random.randint(1,6)
        code[0][i] = num

    #return new code
    return code

def title():

    #initialise variables
    title_background = pygame.image.load("projects/Mastermind/Code/Krita/title.png")
    code = []

    #main title loop
    exited_game = False
    while not exited_game:

        #display
        display_window.blit(title_background,(0,0))
        quitted = False

        for event in pygame.event.get():

            #buttons
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #quit or play
                if 205 < mouse[0] < 297:
                    if 242 < mouse[1] < 262:
                        code = reset_code()
                        game(code)
                        print("Title Mode")
                    if 362 < mouse[1] < 382:
                        exited_game = quit_game()
                #continue
                if 157 < mouse[0] < 345 and 282 < mouse[1] < 302:
                    code, quitted = reload()
                    if not quitted:
                        game(code)
                    print("Title Mode")
                #leaderboard
                if 123 < mouse[0] < 383 and 322 < mouse[1] < 342:
                    leaderboard()
                    print("Title Mode")

        #update display
        pygame.display.update()
        display_clock.tick(30)

def game(code):

    #initialise variables
    game_background = pygame.image.load("projects/Mastermind/Code/Krita/game.png")
    selected_colour = 0
    colour_box_y = 124
    box_x = 114
    box_y = 114
    box_x_2 = 0
    box_y_2 = 0

    #main game loop
    exited_game = False
    while not exited_game:

        #display
        display_window.blit(game_background,(0,0))
        display_smallbox(code)
        display_tinybox(code)
        display_position(code)

        for event in pygame.event.get():

            #buttons
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #quit or next or save
                if 410 <= mouse[0] <= 502:
                    if 492 <= mouse[1] <= 512:
                        exited_game = quit_play()
                    if 282 <= mouse[1] <= 302:
                        code = next_turn(code)
                        exited_game = check_finished(code)
                    if 422 <= mouse[1] <= 442:
                        save_game_code(code)
                        exited_game = quit_play()

                #select colour
                colour_box_y = 124
                for i in range(1,7):
                    if 336 <= mouse[0] <= 392 and colour_box_y <= mouse[1] <= colour_box_y + 56:
                        selected_colour = i
                    colour_box_y += 70

                #change colour
                box_x = 114
                box_y = 114
                for i in range(1,11):
                    for j in range(4):
                        if box_x <= mouse[0] <= box_x + 30 and box_y <= mouse[1] <= box_y + 30:
                            if i == code[11][0]:
                                code[i][j] = selected_colour
                        box_x += 44
                    box_x = 114
                    box_y += 44

        #update display
        pygame.display.update()
        display_clock.tick(30)

def check_finished(code):

    #initialise variables
    exited_game = False

    #check win conditions
    if code[0][4] == 4:
        #game won
        display_largebox(code)
        display_tinybox(code)
        exited_game = True
        pygame.display.update()
        pygame.time.delay(2000)
        add_leaderboard(code)
    elif code[11][0] == 11:
        #game lost
        display_largebox(code)
        display_tinybox(code)
        exited_game = True
        pygame.display.update()
        pygame.time.delay(2000)

    #return exit status
    return exited_game

def display_largebox(code):

    #initialise variables
    colours = {0:(155,155,155) , 1:(255,0,0) , 2:(0,255,0) , 3:(0,0,255) , 4:(255,255,0) , 5:(255,0,255) , 6:(0,255,255)}
    colour = (155,155,155)

    #display squares
    colour = colours[code[0][0]]
    pygame.draw.rect(display_window,colour,[116,22,56,56])
    colour = colours[code[0][1]]
    pygame.draw.rect(display_window,colour,[189,22,56,56])
    colour = colours[code[0][2]]
    pygame.draw.rect(display_window,colour,[261,22,56,56])
    colour = colours[code[0][3]]
    pygame.draw.rect(display_window,colour,[334,22,56,56])

def next_turn(code):

    #initialise variables
    turn = code[11][0]
    correct = 0
    place = 0
    correct_colour = [code[0][0] , code[0][1] , code[0][2] , code[0][3]]
    guess_colour = [code[turn][0] , code[turn][1] , code[turn][2] , code[turn][3]]

    #calculate correct colours
    if correct_colour[0] == guess_colour[0]:
        correct += 1
        correct_colour[0] = -1
        guess_colour[0] = -1
    if correct_colour[1] == guess_colour[1]:
        correct += 1
        correct_colour[1] = -1
        guess_colour[1] = -1
    if correct_colour[2] == guess_colour[2]:
        correct += 1
        correct_colour[2] = -1
        guess_colour[2] = -1
    if correct_colour[3] == guess_colour[3]:
        correct += 1
        correct_colour[3] = -1
        guess_colour[3] = -1
    for i in range(4):
        for j in range(4):
            if correct_colour[i] == guess_colour[j] and guess_colour[j] != -1 and correct_colour[i] != -1:
                place += 1
                correct_colour[i] = -1
                guess_colour[j] = -1

    #reset code
    code[0][4] = correct
    code[0][5] = place
    code[turn][4] = correct
    code[turn][5] = place
    code[11][0] = turn + 1
    return code

def display_smallbox(code):

    #initialise variables
    colours = {0:(155,155,155) , 1:(255,0,0) , 2:(0,255,0) , 3:(0,0,255) , 4:(255,255,0) , 5:(255,0,255) , 6:(0,255,255)}
    colour = (0,0,0)
    box_x = 114
    box_y = 114

    #display the boxes
    for i in range(1,11):
        for j in range(4):
            colour = colours[code[i][j]]
            pygame.draw.rect(display_window,colour,[box_x,box_y,30,30])
            box_x += 44
        box_x = 114
        box_y += 44

def display_tinybox(code):

    #initialise variables
    colour = (155,155,155)
    box_x = 290
    box_y = 114
    box_1 = 0
    box_2 = 0

    #display the boxes
    for i in range(1,11):
        box_1 = code[i][4]
        box_2 = code[i][5]
        for j in range(2):
            for k in range(2):
                if box_1 > 0:
                    colour = (255,0,0)
                    box_1 -= 1
                elif box_2 > 0:
                    colour = (255,255,255)
                    box_2 -= 1
                else:
                    colour = (155,155,155)
                pygame.draw.rect(display_window,colour,[box_x,box_y,12,12])
                box_x += 20
            box_x = 290
            if j == 0:
                box_y += 18
        box_x = 290
        box_y += 26

def display_position(code):

    #initialise variables
    number_0 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/0.png")
    number_1 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/1.png")
    number_2 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/2.png")
    number_3 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/3.png")
    number_4 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/4.png")
    number_5 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/5.png")
    number_6 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/6.png")
    number_7 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/7.png")
    number_8 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/8.png")
    number_9 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/9.png")
    positions = {1:number_1,2:number_2,3:number_3,4:number_4,5:number_5,6:number_6,7:number_7,8:number_8,9:number_9,0:number_0}
    number_y = 75
    position = code[11][0]

    #display the positions
    if position < 10:
        display_window.blit(positions[position],(40,number_y + (position * 44)))
    elif position == 10:
        display_window.blit(positions[1],(28,number_y + (position * 44)))
        display_window.blit(positions[0],(52,number_y + (position * 44)))

def reload():

    #initialise variables
    reload_background = pygame.image.load("projects/Mastermind/Code/Krita/reload.png")
    quitted = False
    games = []
    games = reload_game_code()
    position = 0
    length = 0
    length = len(games)
    code = []
    if length == 0:
        exited_game = quit_reload()
        quitted = True
    else:
        exited_game = False
        code = games[position]

    #main game loop
    while not exited_game:

        #display
        display_window.blit(reload_background,(0,0))
        display_smallbox(code)
        display_tinybox(code)

        for event in pygame.event.get():

            #buttons
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #quit or play
                if 410 <= mouse[0] <= 502:
                    if 492 <= mouse[1] <= 512:
                        exited_game = quit_reload()
                        quitted = True
                    if 282 <= mouse[1] <= 302:
                        games = remove_code(games, position)
                        exited_game = quit_reload()
                #move left or right
                if 212 <= mouse[1] <= 232:
                    if 40 <= mouse[0] <= 60:
                        if position != 0:
                            position -= 1
                            code = games[position]
                    if 446 <= mouse[0] <= 466:
                        if position != length - 1:
                            position += 1
                            code = games[position]
                #delete a code
                if 410 <= mouse[0] <= 478 and 422 <= mouse[1] <= 442:
                    games = remove_code(games, position)
                    position = 0
                    length = len(games)
                    if length == 0:
                        exited_game = quit_reload()
                        quitted = True
                    else:
                        code = games[position]

        #update display
        pygame.display.update()
        display_clock.tick(30)

    #return code and play the game
    return code, quitted

def leaderboard():

    #initialise variables
    leaderboard_background = pygame.image.load("projects/Mastermind/Code/Krita/leaderboard.png")
    scores = []
    scores = open_leaderboard(scores)
    scores = sort_leaderboard(scores)

    #main game loop
    exited_game = False
    while not exited_game:

        #display
        display_window.blit(leaderboard_background,(0,0))
        display_letters(scores)
        display_numbers(scores)

        for event in pygame.event.get():

            #buttons
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #quit
                if 410 <= mouse[0] <= 502 and 492 <= mouse[1] <= 512:
                    exited_game = quit_leaderboard()

        #update display
        pygame.display.update()
        display_clock.tick(30)

def display_numbers(scores):

    #initialise variables
    number_0 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/0.png")
    number_1 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/1.png")
    number_2 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/2.png")
    number_3 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/3.png")
    number_4 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/4.png")
    number_5 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/5.png")
    number_6 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/6.png")
    number_7 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/7.png")
    number_8 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/8.png")
    number_9 = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/9.png")
    numbers = {1:number_1,2:number_2,3:number_3,4:number_4,5:number_5,6:number_6,7:number_7,8:number_8,9:number_9,0:number_0}
    number = ""
    number_x = 315
    number_y = 119

    #display the numbers
    for i in range(10):
        for j in range(3):
            number = int(scores[i][1][j])
            display_window.blit(numbers[number],(number_x,number_y))
            number_x += 24
        number_x = 315
        number_y += 44

def display_letters(scores):

    #initialise varaibles
    letter_a = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/a.png")
    letter_b = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/b.png")
    letter_c = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/c.png")
    letter_d = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/d.png")
    letter_e = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/e.png")
    letter_f = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/f.png")
    letter_g = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/g.png")
    letter_h = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/h.png")
    letter_i = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/i.png")
    letter_j = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/j.png")
    letter_k = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/k.png")
    letter_l = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/l.png")
    letter_m = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/m.png")
    letter_n = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/n.png")
    letter_o = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/o.png")
    letter_p = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/p.png")
    letter_q = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/q.png")
    letter_r = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/r.png")
    letter_s = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/s.png")
    letter_t = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/t.png")
    letter_u = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/u.png")
    letter_v = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/v.png")
    letter_w = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/w.png")
    letter_x = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/x.png")
    letter_y = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/y.png")
    letter_z = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/z.png")
    letters = {"a":letter_a,"b":letter_b,"c":letter_c,"d":letter_d,"e":letter_e,"f":letter_f,"g":letter_g,"h":letter_h,"i":letter_i,"j":letter_j,"k":letter_k,"l":letter_l,"m":letter_m,"n":letter_n,"o":letter_o,"p":letter_p,"q":letter_q,"r":letter_r,"s":letter_s,"t":letter_t,"u":letter_u,"v":letter_v,"w":letter_w,"x":letter_x,"y":letter_y,"z":letter_z}
    letter = ""
    letter_x = 123
    letter_y = 119

    #display the letters
    for i in range(10):
        for j in range(5):
            letter = scores[i][0][j]
            display_window.blit(letters[letter],(letter_x,letter_y))
            letter_x += 24
        letter_x = 123
        letter_y += 44

def sort_leaderboard(scores):

    #bubble sort the scores
    temp = []
    for i in range(len(scores) - 1):
        for j in range(len(scores) - 1):
            if int(scores[j][1]) < int(scores[j+1][1]):
                temp = scores[j]
                scores[j] = scores[j+1]
                scores[j+1] = temp

    #return the leaderboard
    return scores

def add_leaderboard(code):

    #initialise variables
    scores = []
    scores = open_leaderboard(scores)
    name = ""
    score = 0

    #get the users name
    name, scores = naming(name,scores)

    #add the score to the name
    for i in range(len(scores)):
        if name == scores[i][0]:
            score = int(scores[i][1]) + ((11 - code[11][0]) * 2)
            if score >= 999:
                scores[i][1] = "999"
            if 9 < score < 100:
                scores[i][1] = "0" + str(score)
            if score < 9:
                scores[i][1] = "00" + str(score)

    #update the text file
    save_leaderboard(scores)

def naming(name,scores):

    #inititalise variables
    victory_background = pygame.image.load("projects/Mastermind/Code/Krita/victory.png")
    position = 0
    username = ["-","-","-","-","-"]
    letter_x = 171
    letter_y = 207
    count = 0
    letters = "abcdefghijklmnopqrstu-vwxyz-"
    existing = False

    #main naming loop
    exited_game = False
    while not exited_game:

        #display
        display_window.blit(victory_background,(0,0))
        display_username(username)

        for event in pygame.event.get():

            #buttons
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #backspace
                if 410 <= mouse[0] <= 502 and 422 <= mouse[1] <= 442:
                    if position != 0:
                        position -= 1
                        username[position] = "-"
                #add
                if 410 <= mouse[0] <= 478 and 282 <= mouse[1] <= 302:
                    if position == 5:
                        exited_game = quit_naming()
                        #add new names to the list
                        for i in username:
                            name += i
                        for i in scores:
                            if i[0] == name:
                                existing = True
                        if existing == False:
                            scores.append([name,"000"])

                #select letter
                letter_x = 171
                letter_y = 207
                count = 0
                for i in range(4):
                    for j in range(7):
                        if letter_x <= mouse[0] <= letter_x + 20 and letter_y <= mouse[1] <= letter_y + 20:
                            if position < 5 and letters[count] != "-":
                                username[position] = letters[count]
                                position += 1
                        count += 1
                        letter_x += 24
                    letter_x = 171
                    letter_y += 44

            #update display
            pygame.display.update()
            display_clock.tick(30)

    #return the name and leaderboard
    return name, scores

def display_username(username):

    #initialise varaibles
    letter_a = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/a.png")
    letter_b = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/b.png")
    letter_c = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/c.png")
    letter_d = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/d.png")
    letter_e = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/e.png")
    letter_f = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/f.png")
    letter_g = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/g.png")
    letter_h = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/h.png")
    letter_i = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/i.png")
    letter_j = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/j.png")
    letter_k = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/k.png")
    letter_l = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/l.png")
    letter_m = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/m.png")
    letter_n = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/n.png")
    letter_o = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/o.png")
    letter_p = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/p.png")
    letter_q = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/q.png")
    letter_r = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/r.png")
    letter_s = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/s.png")
    letter_t = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/t.png")
    letter_u = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/u.png")
    letter_v = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/v.png")
    letter_w = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/w.png")
    letter_x = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/x.png")
    letter_y = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/y.png")
    letter_z = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/z.png")
    letter_none = pygame.image.load("projects/Mastermind/Code/Krita/Alphabet/-.png")
    letters = {"-":letter_none,"a":letter_a,"b":letter_b,"c":letter_c,"d":letter_d,"e":letter_e,"f":letter_f,"g":letter_g,"h":letter_h,"i":letter_i,"j":letter_j,"k":letter_k,"l":letter_l,"m":letter_m,"n":letter_n,"o":letter_o,"p":letter_p,"q":letter_q,"r":letter_r,"s":letter_s,"t":letter_t,"u":letter_u,"v":letter_v,"w":letter_w,"x":letter_x,"y":letter_y,"z":letter_z}
    letter = ""
    letter_x = 195

    #display the letters
    for i in range(5):
        letter = username[i]
        display_window.blit(letters[letter],(letter_x,163))
        letter_x += 24

def save_leaderboard(scores):

    #write to the text file
    leaderboard_file = open("projects/Mastermind/Code/leaderboard.txt","w")
    for i in scores:
        leaderboard_file.write(i[0] + "," + i[1] + "\n")
    leaderboard_file.close()

def open_leaderboard(scores):

    #initialise variables
    leaderboard_file = open("projects/Mastermind/Code/leaderboard.txt","r")
    leaders = []
    leaders = leaderboard_file.readlines()

    #format the data
    for i in leaders:
        scores.append(i.strip("\n").split(","))
    leaderboard_file.close()

    #return the leaderboard
    return scores

def save_game_code(code):

    #append to the text file
    saved_games = open("projects/Mastermind/Code/saved_games.txt","a")
    saved_games.write(str(code) + "\n")
    saved_games.close()

def reload_game_code():

    #initialise variables
    saved_games = open("projects/Mastermind/Code/saved_games.txt","r")
    saved = []
    saved = saved_games.readlines()
    games = []
    game = []

    #format the data
    for i in saved:
        game = eval(i.strip("\n"))
        games.append(game)
    saved_games.close()

    #return the games
    return games

def remove_code(saved,position):

    #remove the current code from the games
    games = []
    for i in range(len(saved)):
        if i != position:
            games.append(saved[i])

    #write to the text file
    saved_games = open("projects/Mastermind/Code/saved_games.txt","w")
    for i in games:
        saved_games.write(str(i) + "\n")
    saved_games.close()

    #return the games
    return games

#run game
print("Game Started")
title()

#ininitialisation of modules
pygame.quit()
