import math
import pygame

class Shot(pygame.sprite.Sprite):
    def __init__(self, surface, x, y, dx, dy, speed_bullet): #método construtor
        super().__init__()
        self.image = surface
        angle = math.atan2(dy - y, dx - x) #calcula a distancia entre a nave e a clicada pelo mouse
        self.dx = math.cos(angle) * speed_bullet #tira a angulaçao 
        self.dy = math.sin(angle) * speed_bullet 
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)#posição em que a nave se encontra
    
    def move(self):#move a bala na direção do angulo tirado do calculo feito acima
        self.rect.x += int(self.dx) 
        self.rect.y += int(self.dy)

    def enemy_collision(self, enemy):
        if self.rect.colliderect(enemy.rect):
            return True
    
    def shot_excluded(self):
        self.kill()