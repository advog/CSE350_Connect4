import pygame

import button
import gamelogic

pygame.init()

# Dimension globals
Xmax = 700
Ymax = 700
circle_size = (Xmax/700)*40

# color globals
empty_color = (1, 0, 60)
player1_color = (255, 0, 0)
player2_color = (255, 255, 0)
menu_color = (2,178,255)
button_color = (51,255,255)

# initialize display_surface
display_surface = pygame.display.set_mode((Xmax, Ymax))
pygame.display.set_caption('Ultimate Connect 4')

#load assets
logo = pygame.image.load('logo.png')

#most recent game list, this is a placeholder
rewatch_list = []



# initialize game_surface surfaces
game_surface = pygame.Surface((Xmax, Ymax))
def update_game_surface():
    display_surface.blit(game_surface, (0, 0))
    pygame.display.flip()

# initialize menu_surface
menu_surface = pygame.Surface((Xmax, Ymax))
def update_menu_surface():
    display_surface.blit(menu_surface, (0, 0))
    pygame.display.flip()


# loops until the player chooses a gamemode by clicking on a button, returns an int indicating the button clicked
def start_menu():
    menu_surface.fill(menu_color)
    menu_surface.blit(logo, (0, 0))

    lpvp_button = button.click_button((Xmax/2-130,500),(120,50),button_color, "Local PvP")
    lpvp_button.draw(menu_surface)

    opvp_button = button.click_button((Xmax/2 +10, 500), (120, 50), button_color, "Online PvP")
    opvp_button.draw(menu_surface)

    aivp_button = button.click_button((Xmax/2-130, 560), (120, 50), button_color, "PvAI")
    aivp_button.draw(menu_surface)

    aivai_button = button.click_button((Xmax/2 +10, 560), (120, 50), button_color, "AIvAI")
    aivai_button.draw(menu_surface)

    rewatch_button = button.click_button((Xmax / 2 -60, 620), (120, 50), button_color, "Rewatch")
    rewatch_button.draw(menu_surface)

    update_menu_surface()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if lpvp_button.check_clicked(pos):
                    return 0
                if opvp_button.check_clicked(pos):
                    return 1
                if aivp_button.check_clicked(pos):
                    return 2
                if aivai_button.check_clicked(pos):
                    return 3
                if rewatch_button.check_clicked(pos):
                    return 4
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


# main loop, calls start menu to get a gamemode from the player then begins the chosen gamemode
def main():
    while (True):
        gamemode_choice = start_menu()
        if (gamemode_choice == 0):
            localPvP()
        elif (gamemode_choice == 1):
            onlinePvP()
        elif (gamemode_choice == 2):
            localPvAI()
        elif (gamemode_choice == 3):
            localAIvAI()
        elif (gamemode_choice == 4):
            rewatch()


#loops until player returns move
def request_move_player(button_list):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for i in range(7):
                    if( button_list[i].check_clicked(pos)):
                        return i

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == 49:
                    return 0
                if event.key == pygame.K_2 or event.key == 50:
                    return 1
                if event.key == pygame.K_3 or event.key == 51:
                    return 2
                if event.key == pygame.K_4 or event.key == 52:
                    return 3
                if event.key == pygame.K_5 or event.key == 53:
                    return 4
                if event.key == pygame.K_6 or event.key == 54:
                    return 5
                if event.key == pygame.K_7 or event.key == 55:
                    return 6
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


#board is [][], draws board onto game_surface
def draw_board(board):
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


#mutates the button_list to contain a list of inivisible buttons whose index maps to columns
def create_column_buttons(button_list):
    blockSize = Xmax / 7
    for i in range(7):
        tmp_button = button.invisible_button((blockSize*i, 100), (blockSize, 600))
        button_list.append(tmp_button)

# begins local pvp mode gameloop
def localPvP():
    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    #empty rewatch list
    rewatch_list.clear()

    #create button_list
    button_list = []
    create_column_buttons(button_list)

    # create textbox
    textbox = button.click_button((0, 0), (700, 100), menu_color, "")
    textbox.text = "Player 1's Move"
    textbox.draw(game_surface)

    # draw board
    draw_board(board)

    #update surface
    update_game_surface()

    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        selected_column = -1
        while (selected_column == -1):

            #get move from player
            selected_column = request_move_player(button_list)

            #if it is invalid then repeat
            if(gamelogic.check_valid(board, selected_column) == False):
                selected_column = -1

        #add move to gameboard
        gamelogic.add_piece(board, selected_column, turn)

        rewatch_list.append(selected_column)

        # increment turn
        turn = turn + 1

        # change text box
        player_string = "Player " + str((turn)%2+1) + "'s Move"
        textbox.text = player_string
        textbox.draw(game_surface)

        #redraw board
        draw_board(board)

        #update surface
        update_game_surface()

        winner = gamelogic.check_win(board, turn)

    #display who won
    winner_string = "Player " + str(winner) + " Wins!"
    if(winner == 0):
        winner_string = "TIE!"
    textbox.text = winner_string
    textbox.draw(game_surface)

    #update surface
    update_game_surface()

    #keep open till input
    request_move_player(button_list)


# TODO for later
def onlinePvP():
    print('online pvp')


def localPvAI():
    print('pvai')


def localAIvAI():
    print('aivai')

def request_move_rewatch(turn):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return rewatch_list[turn]
            if event.type == pygame.KEYDOWN:
                return rewatch_list[turn]
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def rewatch():
    # initialize game logic vars
    board = [[0] * 6 for i in range(7)]
    turn = 0

    print(rewatch_list)

    # create button_list
    button_list = []
    create_column_buttons(button_list)

    # create textbox
    textbox = button.click_button((0, 0), (700, 100), menu_color, "")
    textbox.text = "Cllick board to advance"
    textbox.draw(game_surface)

    # draw board
    draw_board(board)

    # update surface
    update_game_surface()

    winner = -1  # 0 = tie, 1 = player 1, 2 = player 2
    while (winner == -1):

        selected_column = -1
        while (selected_column == -1):

            # get move from player
            selected_column = request_move_rewatch(turn)

            # if it is invalid then repeat
            if (gamelogic.check_valid(board, selected_column) == False):
                selected_column = -1

        # add move to gameboard
        gamelogic.add_piece(board, selected_column, turn)

        # increment turn
        turn = turn + 1

        # redraw board
        draw_board(board)

        # update surface
        update_game_surface()

        winner = gamelogic.check_win(board, turn)

    # display who won
    winner_string = "Player " + str(winner) + " Wins!"
    if (winner == 0):
        winner_string = "TIE!"
    textbox.text = winner_string
    textbox.draw(game_surface)

    # update surface
    update_game_surface()

    # keep open till input
    request_move_rewatch(0)


if __name__ == '__main__':
    main()
