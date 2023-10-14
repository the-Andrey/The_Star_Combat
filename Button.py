import pygame

class Button():
    def __init__(self, button_image, x,y): #método construtor
        self.image = button_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked = False
    
    def draw(self, win): #método que exibe o botão na tela
        action = False
        pos_mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_mouse):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
        
                action = True

        win.blit(self.image,(self.rect.x,self.rect.y))
        
        return action