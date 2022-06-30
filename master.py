import pygame

pygame.init()
# assigning values to width and height variable
X = 700
Y = 600

emptyColor = (1,0,60)
Red = (255,0,0)
Yellow = (255,255,0)
currColor = Red
turn = 1


display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Ultimate Connect 4')
board = [[0]*6 for i in range(7)]
pieces = [[None]*6 for i in range(7)]

# returns int representing gamemode chosen by player
def start_menu():
    return 0


# main loop
def main():
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
    blockSize = 100 #Set the size of the grid block
    circleSize = 40
    for x in range(7):
        for y in range(6):
            rect = pygame.Rect(x*blockSize, y*blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(display_surface, (255,255,255), rect, 1)
            pieces[x][y]=((x*blockSize+50,y*blockSize+50), circleSize,0)
            pygame.draw.circle(display_surface,emptyColor,pieces[x][y][0], pieces[x][y][1],pieces[x][y][2])

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

    # initialize board here
    display_surface.fill((2, 0, 115))
    drawGrid()
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
