import pygame

class Button:
    def __init__(self, pos, text, dispSurf):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Calibri", 20)
        self.text = self.font.render(text, 1, (0, 0, 0))
        self.size = self.text.get_size()
        self.surface = pygame.Surface((150, 40))
        self.surface.fill(pygame.Color('grey27'))
        self.surface.blit(self.text, ((150-self.size[0])/2, (40-self.size[1])/2))
        self.rect = pygame.Rect(self.x, self.y, 150, 40)
        self.triggered = 0
        self.dispSurf = dispSurf

    def show(self):
        self.dispSurf.blit(self.surface, (self.x, self.y))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.triggered = 1
