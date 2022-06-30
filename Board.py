import pygame
import gamelogic

pygame.init()

# assigning values to width and height variable
X = 700
Y = 600

emptyColor = (1,0,60)
Red = (255,0,0)
Yellow = (255,255,0)
currColor = Red
turn = 1

board = [[0]*6 for i in range(7)]

display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Ultimate Connect 4')

pieces = [[None]*6 for i in range(7)]

#Switched row and col
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


def addPiece(col, color):
    row = -1
    for i in range(6):
        if(board[col][i]==0):
            row = i
    if(row==-1):
        return
    board[col][row]= turn
    print(board)
    tempPiece=pieces[col][row]
    pygame.draw.circle(display_surface, color, tempPiece[0], tempPiece[1], tempPiece[2])

def switchColor(color):
    if color == Red:
        return Yellow
    else:
        return Red

def switchTurn(curr_turn):
    return curr_turn+1


def request_move_player():
    #print("in")
    column = -1
    while True:
        for event in pygame.event.get():
            # key listener


            if event.type == pygame.KEYDOWN:
                #print("farther in")

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
        if(column is not -1):
            break
    return column

##MAIN LOOP

display_surface.fill((2,0,115))
drawGrid()
while True:
    pygame.display.update()
    col = request_move_player()
    #print("past")
    addPiece(col, currColor)
    currColor = switchColor(currColor)
    print("turn {}", turn)
    print("win {}", gamelogic.check_win(board, turn, col))
    turn = switchTurn(turn)

    for event in pygame.event.get():
        #key listener
        """
        if event.type == pygame.KEYDOWN:
            column = -1
            if event.key == pygame.K_1:
                column = 1
            if event.key == pygame.K_2:
                addPiece(1,currColor)
                currColor = switchColor(currColor)
                turn = switchTurn(turn)
                print(gamelogic.check_win(board, 1, 1))
            if event.key == pygame.K_3:
                addPiece(2,currColor)
                currColor = switchColor(currColor)
                turn = switchTurn(turn)
                print(gamelogic.check_win(board, 1, 1))
            if event.key == pygame.K_4:
                addPiece(3,currColor)
                currColor = switchColor(currColor)
                turn = switchTurn(turn)
                print(gamelogic.check_win(board, 1, 1))
            if event.key == pygame.K_5:
                addPiece(4,currColor)
                currColor = switchColor(currColor)
                turn = switchTurn(turn)
                print(gamelogic.check_win(board, 1, 1))
            if event.key == pygame.K_6:
                addPiece(5,currColor)
                currColor = switchColor(currColor)
                turn = switchTurn(turn)
                print(gamelogic.check_win(board, 1, 1))
            if event.key == pygame.K_7:
                addPiece(6,currColor)
                currColor = switchColor(currColor)
                turn = switchTurn(turn)
                print(gamelogic.check_win(board, 1, 1))
            addPiece(0, currColor)
            currColor = switchColor(currColor)
            turn = switchTurn(turn)
            print(gamelogic.check_win(board, 1, 1))
        #quit
        """
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()


        pygame.display.update()

