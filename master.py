import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
screen.fill((2, 0, 115))


class Button:
    def __init__(self, pos, text, event):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Calibri", 20)
        self.text = self.font.render(text, 1, (0, 0, 0))
        self.size = self.text.get_size()
        self.surface = pygame.Surface((150, 40))
        self.surface.fill(pygame.Color('grey27'))
        self.surface.blit(self.text, ((150 - self.size[0]) / 2, (40 - self.size[1]) / 2))
        self.rect = pygame.Rect(self.x, self.y, 150, 40)
        self.event = event

    def show(self):
        screen.blit(self.surface, (self.x, self.y))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.event()


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
    turn = 0
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
