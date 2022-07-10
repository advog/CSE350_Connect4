import pygame
import random
import os
import json
import socket
import button
import gamelogic

#initiate pygame
pygame.init()

# Dimension globals
Xmax = 700
Ymax = 700
circle_size = (Xmax/700)*40
blockSize = Xmax/7

# color globals
empty_color = (1, 0, 60)
player1_color = (255, 0, 0)
player2_color = (255, 255, 0)
menu_color = (2,178,255)
button_color = (51,255,255)

# initialize display_surface
display_surface = pygame.display.set_mode((Xmax, Ymax))
pygame.display.set_caption('Ultimate Connect 4')

#initialize socket
host = socket.gethostname()
port = 42068
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#load assets
logo = pygame.image.load('logo.png')

#most recent game list, this is a placeholder for eventually storing and recalling games in files
rewatch_list = []


# initialize game_surface
game_surface = pygame.Surface((Xmax, Ymax))

#add buttons to game_surface
column_buttons = []
for i in range(7):
    tmp_button = button.invisible_button((blockSize * i, 100), (blockSize, 600))
    column_buttons.append(tmp_button)

#add textbox to game_surface (it is technically a click button but we just will never check if it is clicked)
game_textbox = button.click_button((0, 0), (700, 100), menu_color, "Textbox", game_surface)


#initialize menu surface
menu_surface = pygame.Surface((Xmax, Ymax))
menu_surface.fill(menu_color)
menu_surface.blit(logo, (0, 0))

#add buttons to menu_surface
menu_buttons = []
lpvp_button = button.click_button((Xmax/2-130,500),(120,50),button_color, "Local PvP", menu_surface)
menu_buttons.append(lpvp_button)
opvp_button = button.click_button((Xmax/2 +10, 500), (120, 50), button_color, "Online PvP", menu_surface)
menu_buttons.append(opvp_button)
aivp_button = button.click_button((Xmax/2-130, 560), (120, 50), button_color, "PvAI", menu_surface)
menu_buttons.append(aivp_button)
aivai_button = button.click_button((Xmax/2 +10, 560), (120, 50), button_color, "AIvAI", menu_surface)
menu_buttons.append(aivai_button)
rewatch_button = button.click_button((Xmax / 2 -60, 620), (120, 50), button_color, "Rewatch", menu_surface)
menu_buttons.append(rewatch_button)

#dict for readability (if this were c++ I could just #define these)
menu_button_dict = {"lpvp": 0, "opvp": 1, "aivp": 2, "aivai": 3, "rewatch": 4}


#draws all buttons in a list
#args: [] button_list
def draw_buttons(button_list):
    for b in button_list:
        b.draw()

#args: [] button_list, (x,y) pos
#return: index of first button clicked in list
def check_clicked_buttons(button_list, pos):
    for i in range(len(button_list)):
        if button_list[i].check_clicked(pos):
            return i
    return -1


#draws menu_surface buttons onto menu_surface
def draw_buttons_menu_surface():
    draw_buttons(menu_buttons)

#displays menu_surface on the display_surface
def display_menu_surface():
    display_surface.blit(menu_surface, (0, 0))
    pygame.display.flip()


#draws game_surface buttons onto game_surface
def draw_buttons_game_surface():
    game_textbox.draw()

#draws board onto game_surface
#args: [][] board
def draw_board_game_surface(board):
    blockSize = Xmax / 7  # Set the size of the grid block
    stepSize = (Xmax / 700) * 50
    for x in range(7):
        for y in range(6):
            rect = pygame.Rect(x * blockSize, y * blockSize + 100, blockSize, blockSize)
            pygame.draw.rect(game_surface, (255, 255, 255), rect, 1)
            xy_offset = (x * blockSize + stepSize, y * blockSize + stepSize + 100)
            color = empty_color
            if(board[x][y] == 1): color = player1_color
            elif(board[x][y] == 2): color = player2_color
            pygame.draw.circle(game_surface, color, xy_offset, circle_size)

#displays game_surface on the display_surface
def display_game_surface():
    display_surface.blit(game_surface, (0,0))
    pygame.display.flip()


#loops until the player chooses a gamemode by clicking on a button
#returns: int indicating which button was clicked
def start_menu():
    draw_buttons_menu_surface()
    display_menu_surface()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                clicked_index = check_clicked_buttons(menu_buttons, pos)
                if clicked_index != -1:
                    return clicked_index

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# main loop, calls start menu to get an int indicating gamemode from the player then begins the chosen gamemode
def main():
    while (True):
        gamemode_choice = start_menu()
        if (gamemode_choice == menu_button_dict["lpvp"]):
            localPvP()
        elif (gamemode_choice == menu_button_dict["opvp"]):
            onlinePvP()
        elif (gamemode_choice == menu_button_dict["aivp"]):
            PvAI()
        elif (gamemode_choice == menu_button_dict["aivai"]):
            AIvAI()
        elif (gamemode_choice == menu_button_dict["rewatch"]):
            rewatch()


#loops until player returns move
#returns: int indicating column chosen by player
def request_move_player():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                ret = check_clicked_buttons(column_buttons, pos)
                if ret != -1:
                    return ret

            #event.key 49-55 map to the number keys 1-7
            if event.type == pygame.KEYDOWN:
                if 49 <= event.key <= 55:
                    return event.key - 49

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# begins local pvp mode gameloop
def localPvP():
    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    #empty rewatch list
    rewatch_list.clear()

    #loop untill there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # change text box to indicate who's turn it is
        player_string = "Player " + str((turn) % 2 + 1) + "'s Move"
        game_textbox.text = player_string
        game_textbox.draw()

        # draw board and buttons to game_surface
        draw_board_game_surface(board)
        draw_buttons_game_surface()

        # display game_surface
        display_game_surface()

        #loop until a valid column is selected
        selected_column = -1
        while (selected_column == -1):

            #get move from player
            selected_column = request_move_player()

            #if it is invalid then repeat
            if(gamelogic.check_valid(board, selected_column) == False):
                selected_column = -1

        #add move to gameboard
        gamelogic.add_piece(board, selected_column, turn)

        #add move to rewatch list
        rewatch_list.append(selected_column)

        # increment turn
        turn = turn + 1

        #check for winner
        winner = gamelogic.check_win(board, turn)

    #display who won
    winner_string = "Player " + str(winner) + " Wins!"
    if(winner == 0):
        winner_string = "TIE!"
    game_textbox.text = winner_string

    # draw board and buttons to game_surface
    draw_board_game_surface(board)
    draw_buttons_game_surface()

    # display game_surface
    display_game_surface()

    #keep open till user decides to close
    request_move_player()


#TODO:
#waits until response from server that indicates move, this will need to parse the raw byte data from the socket into a python int
#args: os.socket socket
#retun: int indicating column choice
def request_move_online():
    #try:
    col = client.recv(1024)
    return int.from_bytes(col)
    #except:
    #    print('didnt work')
    #    return random.randrange(0,7,1)

#TODO:
#sends selected move to column, int needs to be parsed to byte[] before being sent over socket
#args: os.socket socket, int column
def send_move_online(column):
    #try:
    client.sendall(int.to_bytes(column))
    #except:
    #    print('didnt work')
    #    pass

def onlinePvP():

    #TODO:
    #display menu for configuring connection
    #user will either enter or request a pairing code
    #if requesting pairing code they will also indicate if they are going first or not

    # player turn == 0 means player is going first
    player_turn = 0

    # connect to socket for network communications
    client.connect((host, port))
    client.setblocking(0)

    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    # empty rewatch list
    rewatch_list.clear()

    # loop untill there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # change text box to indicate who's turn it is
        player_string = "Player " + str((turn) % 2 + 1) + "'s Move"
        game_textbox.text = player_string
        game_textbox.draw()

        # draw board and buttons to game_surface
        draw_board_game_surface(board)
        draw_buttons_game_surface()

        # display game_surface
        display_game_surface()

        # loop until a valid column is selected
        selected_column = -1
        while (selected_column == -1):

            if turn % 2 == player_turn:
                # get move from player
                selected_column = request_move_player()

                # if it is invalid then repeat, otherwise send move to server
                if (gamelogic.check_valid(board, selected_column) == False):
                    selected_column = -1
                else:
                    send_move_online(selected_column)

            else:
                selected_column = request_move_online()

        # add move to gameboard
        gamelogic.add_piece(board, selected_column, turn)

        # add move to rewatch list
        rewatch_list.append(selected_column)

        # increment turn
        turn = turn + 1

        # check for winner
        winner = gamelogic.check_win(board, turn)

    # display who won
    winner_string = "Player " + str(winner) + " Wins!"
    if (winner == 0):
        winner_string = "TIE!"
    game_textbox.text = winner_string

    # draw board and buttons to game_surface
    draw_board_game_surface(board)
    draw_buttons_game_surface()

    # display game_surface
    display_game_surface()

    # keep open till user decides to close
    request_move_player()


#args: [][] board, int difficulty
#return: column of move chosen by AI
def request_move_AI(board, difficulty):
    if(difficulty == 0):
        return random.randrange(0,7,1)

    # TODO implement search algorithm
    elif difficulty > 0:
        return 1

def PvAI():

    #TODO:
    #call fuction that displays menu asking for parameters
    #parameters are AI difficulty and whether player is going first or second

    #player turn == 0 means player is going first
    player_turn = 0

    #ai_difficulty == 0 means random, 0> are progressivly difficult
    ai_difficulty = 0

    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    # empty rewatch list
    rewatch_list.clear()

    # loop untill there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # change text box to indicate who's turn it is
        player_string = "Player " + str((turn) % 2 + 1) + "'s Move"
        game_textbox.text = player_string
        game_textbox.draw()

        # draw board and buttons to game_surface
        draw_board_game_surface(board)
        draw_buttons_game_surface()

        # display game_surface
        display_game_surface()

        # loop until a valid column is selected
        selected_column = -1
        while (selected_column == -1):

            if turn%2 == player_turn:
                # get move from player
                selected_column = request_move_player()

                # if it is invalid then repeat
                if (gamelogic.check_valid(board, selected_column) == False):
                    selected_column = -1

            else:
                #sleep to give player time to unclick mouse
                pygame.time.wait(100)

                selected_column = request_move_AI(board, ai_difficulty)

        # add move to gameboard
        gamelogic.add_piece(board, selected_column, turn)

        # add move to rewatch list
        rewatch_list.append(selected_column)

        # increment turn
        turn = turn + 1

        # check for winner
        winner = gamelogic.check_win(board, turn)

    # display who won
    winner_string = "Player " + str(winner) + " Wins!"
    if (winner == 0):
        winner_string = "TIE!"
    game_textbox.text = winner_string

    # draw board and buttons to game_surface
    draw_board_game_surface(board)
    draw_buttons_game_surface()

    # display game_surface
    display_game_surface()

    # keep open till user decides to close
    request_move_player()


def AIvAI():
    print('aivai')

def rewatch():
    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    # update textbox
    game_textbox.text = "Click anywhere to progress replay"
    game_textbox.draw()

    # loop untill there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # draw board and buttons to game_surface
        draw_board_game_surface(board)
        draw_buttons_game_surface()

        # display game_surface
        display_game_surface()

        #block until player input
        request_move_player()

        # get saved move
        selected_column = rewatch_list[turn]

        # add move to gameboard
        gamelogic.add_piece(board, selected_column, turn)

        # increment turn
        turn = turn + 1

        #check for winner
        winner = gamelogic.check_win(board, turn)

    # display who won
    winner_string = "Player " + str(winner) + " Wins!"
    if (winner == 0):
        winner_string = "TIE!"
    game_textbox.text = winner_string

    # draw board and buttons to game_surface
    draw_board_game_surface(board)
    draw_buttons_game_surface()

    # display game_surface
    display_game_surface()

    # keep open till input
    request_move_player()


if __name__ == '__main__':
    main()
