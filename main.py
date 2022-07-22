import pygame
import ai
import gui
import gamelogic
import network
import ai_2

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
ai_config_gui = gui.ai_config_gui(display_surface, Xmax, Ymax)
network_config_gui = gui.network_config_gui(display_surface, Xmax, Ymax)

#most recent game list
rewatch_list = []

###########
#main menu#
###########

# main loop, calls start menu to get an int indicating gamemode from the player then begins the chosen gamemode
def main():
    #draw start menu
    while (True):
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
    gui.click_anywhere()

############
#online PvP#
############

def network_failure():
    network_config_gui.draw_text_feedback("network failure, click anywhere to return to main menu")
    network_config_gui.update_display()
    gui.click_anywhere()
    return

def onlinePvP():
    #get config info from the config gui
    player_turn, connection_code = network_config_gui.get_config()

    #update gui
    network_config_gui.draw_text_feedback("connecting to server...")
    network_config_gui.update_display()

    #conect to server
    status, sock = network.connect_server()

    #connection failed, inform user and prompt to return to menu
    if status == -1: network_failure(); return

    #if we are hosting, host always goes first, request code from server
    if(player_turn == 0):
        network_config_gui.draw_text_feedback("requesting code...")
        network_config_gui.update_display()

        code = network.request_code(sock)
        if code == -1: network_failure(); return

        network_config_gui.draw_text_feedback("recieved code")
        network_config_gui.update_display()

        network_config_gui.draw_text_host(str(code))
        network_config_gui.update_display()
    #if we are connecting, send code to server
    else:
        ret = network.send_code(sock, connection_code)
        if ret == -1: network_failure(); return

        network_config_gui.draw_text_feedback("sent code, waiting for return...")
        network_config_gui.update_display()

    ret = network.wait_start()
    if ret == -1: network_failure(); return

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
                    ret = network.send_move(sock, selected_column)
                    if ret == -1: network_failure(); return

            else:
                selected_column = network.request_move(sock)
                if selected_column == -1: network_failure(); return

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
    gui.click_anywhere()

##############
#AI gamemodes#
##############

def PvAI():

    #player turn == 0 means player is going first
    player_turn, ai_difficulty = ai_config_gui.get_config()

    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    #empty rewatch list
    rewatch_list.clear()

    #loop untill there is a winner/tie
    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        # update textbox
        is_human = turn % 2 #whose turn is it 1 = player/human, 1 = AI
        player_string = "Player's Move"
        ai_string = "AI's Move"
        if(is_human == 0):
            game_gui.draw_text(player_string)
        elif(is_human == 1):
            game_gui.draw_text(ai_string)
        game_gui.draw_board(board)
        game_gui.update_display()

        #loop until a valid column is selected
        selected_column = -1

        if (is_human == 0):  #if its a humna/player
            while (selected_column == -1):

                #seed control to game_gui until player provides move
                selected_column = game_gui.request_move_player()

                #if it is invalid then repeat
                if(gamelogic.check_valid(board, selected_column) == False):
                    selected_column = -1

        elif (is_human == 1):
            while (selected_column == -1):
                selected_column = ai_2.request_move_AI(board, ai_difficulty, is_human)  # adjust difficulty #-=============================================================================
                #print(selected_column)
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
    gui.click_anywhere()


def AIvAI():
    print('aivai')

##################
#rewatch gamemode#
##################

def rewatch():
    if len(rewatch_list) == 0:
        game_gui.draw_text("no game to rewatch, click anywhere to return to menu")
        game_gui.update_display()
        gui.click_anywhere()
        return

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
    gui.click_anywhere()

if __name__ == '__main__':
    main()