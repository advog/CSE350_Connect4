import pygame

#button class for displaying text and also checking for clicks
class click_button:

    #args: (x,y) pos, (w,h) dim, (r,g,b) color, "" text, pygam.surface surface
    def __init__(self, pos, dim, color, text, external_surface):
        self.width, self. height = dim
        self.x, self.y = pos
        self.internal_surface = pygame.Surface((self.width, self.height))
        self.text = text
        self.color = color
        self.external_surface = external_surface

        #rectangle for click detection
        self.rect = pygame.Rect(self.x, self.y,self.width, self.height)

    #redraws self to the external_gamesurface
    def draw(self):
        self.internal_surface.fill(self.color)

        font = pygame.font.SysFont("Calibri", 20)
        rendered_text = font.render(self.text, 1, (0, 0, 0))
        self.internal_surface.blit(rendered_text, (self.width / 2 - rendered_text.get_width() / 2, self.height / 2))

        self.external_surface.blit(self.internal_surface, (self.x,self.y))

    def check_clicked(self, pos):
        return self.rect.collidepoint(pos)


#easier for click detection, only method is to check if click pos is within button
class invisible_button:
    def __init__(self, pos, dim):
        self.width, self. height = dim
        self.x, self.y = pos

        self.rect = pygame.Rect(self.x, self.y,self.width, self.height)

    def check_clicked(self, pos):
        return self.rect.collidepoint(pos)
