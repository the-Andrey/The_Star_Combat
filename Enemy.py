import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,image):#método construtor
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed_x, self.speed_y = 3 , 3
        self.multiplicate_value = 1
        self.health = 300
        self.hit_by_bullet = False #determina se o inimigo ja foi acertado por uma bala ou não
    
    def draw(self, win): #método que exibe na tela
        win.blit(self.image,(self.rect.x, self.rect.y))


    def movimentation(self, starship_x, starship_y): #método que define a movimentação do objeto
        multiplier_value = 1

        #utiliza combinação linear para movimentar o objeto
        if self.rect.x < (starship_x - 30): 
            direction_x = multiplier_value * self.speed_x
            self.rect.x += direction_x
        
        if self.rect.x > (starship_x + 30):
            direction_x = multiplier_value * self.speed_x
            self.rect.x -= direction_x
       
        if self.rect.y < (starship_y - 30):
            direction_y = multiplier_value * self.speed_y
            self.rect.y += direction_y
        if self.rect.y > (starship_y + 30):
            direction_y = multiplier_value * self.speed_y
            self.rect.y -= direction_y

    def starship_collision(self, starship): #método que detecta colisão entre o inimigo e a nave principal
        if self.rect.colliderect(starship.rect):#pode ser que esse 'starship' precise de alteração
            return True
                 
            
    def other_enemy_collision(self, other_enemies):
        for enemy in other_enemies:
            if enemy != self:
                if self.rect.colliderect(enemy.rect):
                    # Se houver colisão com outro inimigo, ajuste as posições
                    if self.rect.x < enemy.rect.x:
                        self.rect.x -= 1
                    elif self.rect.x > enemy.rect.x:
                        self.rect.x += 1

                    if self.rect.y < enemy.rect.y:
                        self.rect.y -= 1
                    elif self.rect.y > enemy.rect.y:
                        self.rect.y += 1

    def health_bar(self, surface):
            bar_x = self.rect.centerx - 130 / 2
            bar_y = self.rect.bottom + 15
            current_health = self.health

            ratio = current_health/ 300
            pygame.draw.rect(surface, "white", (bar_x, bar_y, 130, 15))
            pygame.draw.rect(surface, "red", (bar_x, bar_y, 130 * ratio, 15))


    def lost_health(self, damage, win, image):
        if damage:
           self.health -= 100

        if self.health <= 0:
            explosion_time = 500
            current_time = pygame.time.get_ticks()
            explosion_start = getattr(self, 'explosion_start', current_time)

            if current_time - explosion_start < explosion_time:
                win.blit(image, (self.rect.x, self.rect.y))
                return True
        return False
        
    

    def enemy_killed(self):
        self.kill()
        return True