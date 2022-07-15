import pygame
import random
import os

import gui
import gamelogic

#initiate pygame
pygame.init()

# Dimension globals
Xmax = 700
Ymax = 700

# color globals
menu_color = (2,178,255)
button_color = (51,255,255)
empty_color = (1, 0, 60)
player1_color = (255, 0, 0)
player2_color = (255, 255, 0)
menu_color = (2,178,255)

# initialize display_surface
display_surface = pygame.display.set_mode((Xmax, Ymax))
pygame.display.set_caption('Ultimate Connect 4')

#initialize guis
menu_gui = gui.menu_gui(display_surface, Xmax, Ymax)
game_gui = gui.game_gui(display_surface, Xmax, Ymax)

#most recent game list
rewatch_list = []

###########
#main menu#
###########

# main loop, calls start menu to get an int indicating gamemode from the player then begins the chosen gamemode
def main():
    #draw start menu

    menu_gui.draw_buttons()
    menu_gui.update_display()

    while (True):
        menu_gui.update_display()
        choice = menu_gui.request_menu_choice()
        if (choice == 0):   localPvP()
        elif (choice == 1):   onlinePvP()
        elif (choice == 2):   PvAI()
        #TODO:
        #implement AI v AI gameloop
        elif (choice == 3):   AIvAI()
        elif (choice == 4):   rewatch()

###########
#Local PVP#
###########

def localPvP():
    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    #empty rewatch list
    rewatch_list.clear()

    #loop untill there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # update textbox
        player_string = "Player " + str((turn) % 2 + 1) + "'s Move"
        game_gui.draw_text(player_string)
        game_gui.draw_board(board)
        game_gui.update_display()

        #loop until a valid column is selected
        selected_column = -1
        while (selected_column == -1):

            #seed control to game_gui until player provides move
            selected_column = game_gui.request_move_player()

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
    if(winner == 0): winner_string = "TIE!"
    game_gui.draw_text(winner_string)
    game_gui.draw_board(board)
    game_gui.update_display()

    #keep open till user decides to close
    game_gui.request_move_player()

############
#online PvP#
############

#TODO:
#waits until response from server that indicates move, this will need to parse the raw byte data from the socket into a python int
#args: os.socket socket
#retun: int indicating column choice
def request_move_online(socket):
    return random.randrange(0,7,1)

#TODO:
#sends selected move to column, s
#args: os.socket socket, int column
def send_move_online(socket, column):
    pass

def onlinePvP():
    #TODO:
    #intiialize socket connection to server

    # player -1 if player is hosting, n if player is connecting

    #reset the network_config_menu then request info from it
    #connection_code = network_config_menu.online_config()
    connection_code = -1;

    player_turn = 0
    if(connection_code == -1):
        #request code from server
        #recieve code from server
        #display code to GUI
        #redraw GUI
        pass
    else:
        player_turn = 1
        #send connection code to server
        #display status to GUI
        #redraw GUI
        pass

    #wait until game is started by server

    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    # empty rewatch list
    rewatch_list.clear()

    # loop until there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # update textbox
        player_string = "Player " + str((turn) % 2 + 1) + "'s Move"
        game_gui.draw_text(player_string)
        game_gui.draw_board(board)
        game_gui.update_display()

        # loop until a valid column is selected
        selected_column = -1
        while (selected_column == -1):

            if turn % 2 == player_turn:
                # get move from player
                selected_column = game_gui.request_move_player()

                # if it is invalid then repeat, otherwise send move to server
                if (gamelogic.check_valid(board, selected_column) == False):
                    selected_column = -1
                else:
                    send_move_online(sock, selected_column)

            else:
                selected_column = request_move_online(sock)

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
    if (winner == 0): winner_string = "TIE!"
    game_gui.draw_text(winner_string)
    game_gui.draw_board(board)
    game_gui.update_display()

    # keep open till user decides to close
    game_gui.request_move_player()

##############
#AI gamemodes#
##############

#args: [][] board, int difficulty
#return: column of move chosen by AI
def request_move_AI(turn, board, difficulty):
    if(difficulty == 0):
        return random.randrange(0,7,1)

    # TODO:
    # implement search algorithm
    elif difficulty > 0:
        return 1

def PvAI():

    #player turn == 0 means player is going first
    player_turn, ai_difficulty = ai_config_menu.get_config()

    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    # empty rewatch list
    rewatch_list.clear()

    # loop untill there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # update gui
        player_string = "Player " + str((turn) % 2 + 1) + "'s Move"
        game_gui.draw_text(player_string)
        game_gui.draw_board(board)
        game_gui.update_display()

        # loop until a valid column is selected
        selected_column = -1
        while (selected_column == -1):

            if turn%2 == player_turn:
                # get move from player
                selected_column = game_gui.request_move_player()

                # if it is invalid then repeat
                if (gamelogic.check_valid(board, selected_column) == False):
                    selected_column = -1

            else:
                #sleep to give player time to unclick mouse
                pygame.time.wait(100)

                selected_column = request_move_AI(turn, board, ai_difficulty)

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
    if (winner == 0): winner_string = "TIE!"
    game_gui.draw_text(winner_string)
    game_gui.draw_board(board)
    game_gui.update_display()

    # keep open till user decides to close
    game_gui.request_move_player()


def AIvAI():
    print('aivai')

##################
#rewatch gamemode#
##################

def rewatch():
    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    # loop untill there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # update gui
        player_string = "Player " + str((turn) % 2 + 1) + "'s Move"
        game_gui.draw_text(player_string)
        game_gui.draw_board(board)
        game_gui.update_display()

        #get move then wait for player input
        selected_column = rewatch_list[turn]
        game_gui.request_move_player()

        # add move to gameboard
        gamelogic.add_piece(board, selected_column, turn)

        # increment turn
        turn = turn + 1

        # check for winner
        winner = gamelogic.check_win(board, turn)

    # display who won
    winner_string = "Player " + str(winner) + " Wins!"
    if (winner == 0): winner_string = "TIE!"
    game_gui.draw_text(winner_string)
    game_gui.draw_board(board)
    game_gui.update_display()

    # keep open till user decides to close
    game_gui.request_move_player()

if __name__ == '__main__':
    main()