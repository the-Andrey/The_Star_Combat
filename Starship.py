import pygame
import math

class Starship(pygame.sprite.Sprite):
    def __init__(self, x, y, image, win_width, win_height): #método construtor
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed_x, self.speed_y = 3 , 3
        self.active = True
        self.angle = 0
        self.health = 15000
        self.win_width = win_width
        self.win_height = win_height
        
        
       
    def draw(self, win): #método que desenha a nave na tela
        win.blit(self.image,(self.rect.x, self.rect.y))
    
    def movimentation(self): #método de movimentação da nave principal
        keys = pygame.key.get_pressed()
        key_input = 1
    
        #utiliza combinação linear para movimentar a nave
        if keys[pygame.K_d]:
            direction_x = key_input * self.speed_x 
            self.rect.x += direction_x
           
        if keys[pygame.K_w]:#ir para cima
            direction_y = key_input * self.speed_y 
            self.rect.y -= direction_y

        if keys[pygame.K_a]:#ir para esquerda
            direction_x = key_input * self.speed_x
            self.rect.x -= direction_x

        if keys[pygame.K_s]:#ir para baixo
            direction_y = key_input * self.speed_y
            self.rect.y += direction_y
        
    
    def starship_aim(self, image): #método que rotaciona a nave de acordo com a direção do mouse
        pos_mouse = pygame.mouse.get_pos()
        mouse_y = -(pos_mouse[1] - self.rect.centery)
        mouse_x = pos_mouse[0] - self.rect.centerx
        self.angle = math.degrees(math.atan2(mouse_y, mouse_x)) #calcula a distancia entre a nave e a coordenada do mouse e transforma em angulo em graus
        image_rotated = pygame.transform.rotate(image, self.angle -90)  # inverte o ângulo para corresponder à rotação desejada e rotaciona
        self.rect = image_rotated.get_rect(center = self.rect.center)
        self.image = image_rotated

    def edge_collision(self): #método que detecta colisão com a borda da janela para que a nave não saia da janela o jogo
        if self.rect.right >= self.win_width :
            self.rect.right = self.win_width 

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.bottom >= self.win_height:
            self.rect.bottom = self.win_height 
        
        if self.rect.top <= 0:
            self.rect.top = 0
    
    def health_bar(self, surface):
        bar_x = self.rect.centerx - 150 // 2
        bar_y = self.rect.bottom + 15
        current_health = self.health

        ratio = current_health/ 15000
        pygame.draw.rect(surface, "white", (bar_x, bar_y, 150, 15))
        pygame.draw.rect(surface, "cyan", (bar_x, bar_y, 150 * ratio, 15))
        
    
    def starship_lost_health(self, damage, win, image):
        if damage:
            self.health -= 100
        if self.health <= 0:
            win.blit(image, (self.rect.x,self.rect.y))
            return True
        

    def starship_killed(self):
        self.kill()
        return True