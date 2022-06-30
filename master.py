import pygame
import c4tools
pygame.init()

# Globals
Xmax = 1400
Ymax= 1200

emptyColor = (1,0,60)
Red = (255,0,0)
Yellow = (255,255,0)
currColor = Red
turn = 1

board = [[0]*6 for i in range(7)]
pieces = [[None]*6 for i in range(7)]

#initialize display_surface
display_surface = pygame.display.set_mode((Xmax, Ymax))
pygame.display.set_caption('Ultimate Connect 4')

#initialize additional surfaces
game_surface = pygame.Surface((Xmax, Ymax))
menu_surface = pygame.Surface((Xmax, Ymax))
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

def drawGrid():
    blockSize = Xmax/7 #Set the size of the grid block
    circleSize = (Xmax/700)*40
    stepSize = (Xmax/700)*50
    for x in range(7):
        for y in range(6):
            rect = pygame.Rect(x*blockSize, y*blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(game_surface, (255,255,255), rect, 1)
            pieces[x][y]=((x*blockSize+stepSize,y*blockSize+stepSize), circleSize,0)
            pygame.draw.circle(game_surface,emptyColor,pieces[x][y][0], pieces[x][y][1],pieces[x][y][2])

# waits until the player inputs move
def request_move_player():
    column = -1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    column = 0
                if event.key == pygame.K_2:
                    column = 1
                if event.key == pygame.K_3:
                    column = 2
                if event.key == pygame.K_4:
                    column = 3
                if event.key == pygame.K_5:
                    column = 4
                if event.key == pygame.K_6:
                    column = 5
                if event.key == pygame.K_7:
                    column = 6
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if (column is not -1):
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
        while (True):
            selected_column = request_move_player()
            # if(check_valid(column, board, turn%2)):
            break;

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
