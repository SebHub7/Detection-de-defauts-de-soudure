import pygame

class Button1:

    def __init__(self, x, y, w, h, text):
        self.pos = (x, y)
        self.w = w
        self.h = h

        self.font = pygame.font.SysFont('Corbel', 20, bold=True) 
        self.text = self.font.render(text, True, (0, 0, 0))

    

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), [self.pos[0], self.pos[1], self.w+5, self.h], border_radius=5) 
        window.blit(self.text, (self.pos[0] + 3, self.pos[1] + 5)) 


    def isClicked(self):
        mouse = pygame.mouse.get_pos()
        return self.pos[0] <= mouse[0] <= self.pos[0]+self.w and self.pos[1] <= mouse[1] <= self.pos[1]+self.h