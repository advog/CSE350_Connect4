import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
screen.fill(pygame.Color("white"))

class Button:
    def __init__(self, pos, text, event):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", 20)
        self.text = self.font.render(text, 1, pygame.Color("black"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface((75, 35))
        self.surface.fill(pygame.Color("grey45"))
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, 75, 35)

    def show(self):
        screen.blit(self.surface, (self.x, self.y))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                event

def mainloop():
    PvP = Button((350, 800), "Local Player vs Player", localPvP)
    OPvP = Button((350, 900), "Online Player vs Player", onlinePvP)
    PvAI = Button((650, 800), "Local Player vs AI", localPvAI)
    AIvAI = Button((650, 900), "Local AI vs AI", localAIvAI)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            PvP.process()
            OPvP.process()
            PvAI.process()
            AIvAI.process()


def localPvP():
    print('pvp')
def onlinePvP():
    print('online pvp')
def localPvAI():
    print('pvai')
def localAIvAI():
    print('aivai')


mainloop()
