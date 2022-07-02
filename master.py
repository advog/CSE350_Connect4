import pygame
import c4tools
import gamelogic
pygame.init()

# Globals
Xmax = 700
Ymax= 700
circleSize = (Xmax/700)*40

emptyColor = (1,0,60)
Red = (255,0,0)
Yellow = (255,255,0)
currColor = Red
turn = 1

board = [[None]*6 for i in range(7)]

#initialize display_surface
display_surface = pygame.display.set_mode((Xmax, Ymax))
pygame.display.set_caption('Ultimate Connect 4')

#initialize additional surfaces
game_surface = pygame.Surface((Xmax, Ymax))
menu_surface = pygame.Surface((Xmax, Ymax))
text_box = c4tools.Label((0, 0), "Welcome", game_surface)
game_surface.fill((2, 0, 115))
menu_surface.fill((2, 0, 115))

#Menu Buttons
PvP = c4tools.Button((Xmax/2-250, Ymax - 200), "Player vs Player", menu_surface)
OPvP = c4tools.Button((Xmax/2-250, Ymax - 100), "Online PvP", menu_surface)
PvAI = c4tools.Button((Xmax/2+100, Ymax - 200), "Player vs AI", menu_surface)
AIvAI = c4tools.Button((Xmax/2+100, Ymax - 100), "AI vs AI", menu_surface)
logo = pygame.image.load('logo2.png')

# returns int representing gamemode chosen by player
def start_menu():

    PvP.show()
    OPvP.show()
    PvAI.show()
    AIvAI.show()
    menu_surface.blit(logo, (20, 20))
    display_surface.blit(menu_surface, (0,0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            PvP.process()
            OPvP.process()
            PvAI.process()
            AIvAI.process()
        if PvP.triggered:
            return 0
        elif OPvP.triggered:
            return 1
        elif PvAI.triggered:
            return 2
        elif AIvAI.triggered:
            return 3



# main loop
def main():
    drawGrid()
    while (True):
        gamemode_choice = start_menu()
        # clear or delete the screen
        if (gamemode_choice == 0):
            pvp_mode()
        elif (gamemode_choice == 1):
            online_mode()
        elif (gamemode_choice == 2):
            cvp_mode()
        elif (gamemode_choice == 3):
            cvc_mode()

#inititalizes board array and draws grid
def drawGrid():
    text_box.show()
    blockSize = Xmax/7 #Set the size of the grid block
    stepSize = (Xmax/700)*50
    for x in range(7):
        for y in range(6):
            rect = pygame.Rect(x*blockSize, y*blockSize+100,
                               blockSize, blockSize)
            pygame.draw.rect(game_surface, (255,255,255), rect, 1)
            board[x][y]=[(x*blockSize+stepSize,y*blockSize+stepSize+100), 0]
            pygame.draw.circle(game_surface,emptyColor,board[x][y][0], circleSize)

#draws and adds a piece
def addPiece(col, turn):
    row = gamelogic.get_open_row(board, col)

    board[col][row]
    if turn%2 == 0:
        color = Yellow
        board[col][row][1] = 2
    else:
        color = Red
        board[col][row][1] = 1

    print(board[col][row][0])
    pygame.draw.circle(game_surface, color, board[col][row][0], circleSize)
    display_surface.blit(game_surface, (0,0))
    pygame.display.flip()


# waits until the player inputs move
def request_move_player():
    text_box.change("Checking for move")
    column = -1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == 49:
                    column = 0
                if event.key == pygame.K_2 or event.key == 50:
                    column = 1
                if event.key == pygame.K_3 or event.key == 51:
                    column = 2
                if event.key == pygame.K_4 or event.key == 52:
                    column = 3
                if event.key == pygame.K_5 or event.key == 53:
                    column = 4
                if event.key == pygame.K_6 or event.key == 54:
                    column = 5
                if event.key == pygame.K_7 or event.key == 55:
                    column = 6
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if (column != -1):
            break
    return column


# begins pvp mode gameloop
def pvp_mode():
    # stuff to display gameboard goes here
    display_surface.blit(game_surface, (0,0))
    pygame.display.flip()

    turn = 1
    winner = -1

    while (winner == -1):
        selected_column = -1
        while (gamelogic.check_valid(board, selected_column) != True):
            selected_column = request_move_player()

            if(selected_column == -1):
                text_box.change("INVALID MOVE")
            print(gamelogic.get_open_row(board, selected_column))
        addPiece(selected_column, turn)

        if(gamelogic.check_win(board, turn, selected_column)):
            winner = 1
        turn += 1
    text_box.change("YAY YOU WIN")



    # update_board(board, column)

    # display_board(board)

    # winner = check_win()


# winner display stuff here


# TODO for later
def onlinePvP():
    print('online pvp')


def localPvAI():
    print('pvai')


def localAIvAI():
    print('aivai')


main()
