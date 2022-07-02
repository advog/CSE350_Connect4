import pygame

class click_button:
    def __init__(self, pos, dim, color, text):
        self.width, self. height = dim
        self.x, self.y = pos
        self.surface = pygame.Surface((self.width, self.height))
        self.text = text
        self.color = color

        #fill with color
        self.surface.fill(color)

        #render text
        font = pygame.font.SysFont("Calibri", 20)
        rendered_text = font.render(self.text, 1, (0, 0, 0))
        self.surface.blit(rendered_text, (self.width / 2 - rendered_text.get_width() / 2, self.height / 2))

        #rectangle for click detection
        self.rect = pygame.Rect(self.x, self.y,self.width, self.height)

    def draw(self, external_surface):
        self.surface.fill(self.color)

        font = pygame.font.SysFont("Calibri", 20)
        rendered_text = font.render(self.text, 1, (0, 0, 0))
        self.surface.blit(rendered_text, (self.width / 2 - rendered_text.get_width() / 2, self.height / 2))

        external_surface.blit(self.surface, (self.x,self.y))

    def check_clicked(self, pos):
        return self.rect.collidepoint(pos)


#easier for click detection
class invisible_button:
    def __init__(self, pos, dim):
        self.width, self. height = dim
        self.x, self.y = pos

        self.rect = pygame.Rect(self.x, self.y,self.width, self.height)

    def check_clicked(self, pos):
        return self.rect.collidepoint(pos)
