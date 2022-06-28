import pygame

pygame.init()

# assigning values to width and height variable
X = 700
Y = 600

emptyColor = (1,0,60)
Red = (255,0,0)
Yellow = (255,255,0)
currColor = Red

board = [[0]*6 for i in range(7)]

display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Ultimate Connect 4')

pieces = [[None]*6 for i in range(7)]

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

# infinite loop
display_surface.fill((2,0,115))
drawGrid()


def addPiece(col, color):
    row = -1
    for i in range(6):
        if(board[col][i]==0):
            row = i
    if(row==-1):
        return
    board[col][row]=1
    pygame.draw.circle(display_surface, color, pieces[col][row][0], pieces[col][row][1], pieces[col][row][2])

def switchColor(color):
    if color == Red:
        return Yellow
    else:
        return Red

##MAIN LOOP
while True:

    for event in pygame.event.get():
        #key listener
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                addPiece(0,currColor)
                currColor = switchColor(currColor)
            if event.key == pygame.K_2:
                addPiece(1,currColor)
                currColor = switchColor(currColor)
            if event.key == pygame.K_3:
                addPiece(2,currColor)
                currColor = switchColor(currColor)
            if event.key == pygame.K_4:
                addPiece(3,currColor)
                currColor = switchColor(currColor)
            if event.key == pygame.K_5:
                addPiece(4,currColor)
                currColor = switchColor(currColor)
            if event.key == pygame.K_6:
                addPiece(5,currColor)
                currColor = switchColor(currColor)
            if event.key == pygame.K_7:
                addPiece(6,currColor)
                currColor = switchColor(currColor)
        #quit
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        pygame.display.update()

