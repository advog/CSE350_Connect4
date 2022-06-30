import pygame

pygame.init()
screen = pygame.display.set_mode((600, 700))
screen.fill((2, 0, 115))

class Button:
    def __init__(self, pos, text):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Calibri", 20)
        self.text = self.font.render(text, 1, (0, 0, 0))
        self.size = self.text.get_size()
        self.surface = pygame.Surface((150, 40))
        self.surface.fill(pygame.Color('grey27'))
        self.surface.blit(self.text, ((150-self.size[0])/2, (40-self.size[1])/2))
        self.rect = pygame.Rect(self.x, self.y, 150, 40)
        self.triggered = 0

    def show(self):
        screen.blit(self.surface, (self.x, self.y))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.triggered = 1


def menu():
    PvP = Button((125, 500), "Player vs Player")
    OPvP = Button((125, 600), "Online PvP")
    PvAI = Button((325, 500), "Player vs AI")
    AIvAI = Button((325, 600), "AI vs AI")
    logo = pygame.image.load('logo2.png')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            PvP.process()
            OPvP.process()
            PvAI.process()
            AIvAI.process()
        PvP.show()
        OPvP.show()
        PvAI.show()
        AIvAI.show()

        if PvP.triggered:
            return 1
        elif OPvP.triggered:
            return 2
        elif PvAI.triggered:
            return 3
        elif AIvAI.triggered:
            return 4
        #screen.blit(logo, (0, 200))

        pygame.display.update()


def localPvP():
    print('pvp')
def onlinePvP():
    print('online pvp')
def localPvAI():
    print('pvai')
def localAIvAI():
    print('aivai')


mainloop()
