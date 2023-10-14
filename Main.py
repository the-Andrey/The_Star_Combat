import pygame
import pygame.time
from Starship import Starship
from Shot import Shot
from Enemy import Enemy
from Button import Button

pygame.init()

#criação da janela e suas propriedades
WIN_WIDTH = 1280 #largura da janela principal
WIN_HEIGHT = 920 #altura da janela principal
FPS = 60
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
WIN_IMAGE = pygame.image.load('background2.png').convert_alpha()
IMAGE_SCALE = pygame.transform.scale(WIN_IMAGE, (1280,920))
pygame.display.set_caption("The Star Combat")

#imagem da vitória caso o jogador ganhe
victory_image = pygame.image.load('victory_image.png').convert_alpha()
victory_scale = pygame.transform.scale(victory_image,(750,400))

#imagem do game over caso o jogador morra
game_over_image = pygame.image.load('game_over.png').convert_alpha()
game_over_scaled = pygame.transform.scale(game_over_image, (500,500))



#imagem e tamanho da nave
starship_load = pygame.image.load('spaceship.png').convert_alpha()
img_width = 100
img_height = 100
starship_image = pygame.transform.scale(starship_load,(img_width, img_height))



#criação da nave            
starship = Starship(WIN_WIDTH//2, WIN_HEIGHT//2, starship_image, WIN_WIDTH, WIN_HEIGHT)
 

#criação das balas            
bullet = pygame.Surface((10,10))
bullet.fill(((0,255,255)))

            
#imagem e tamanho dos inimigos
enemy_load = pygame.image.load('enemy.png').convert_alpha()
img_width = 60
img_height = 60
enemy_image = pygame.transform.scale(enemy_load,(img_width, img_height))

#imagem e tamanho da explosao da nave e dos inimigos
explosion_load = pygame.image.load('explosion.png').convert_alpha()
explosion_image = pygame.transform.scale(explosion_load,(100,100))
explosion_load_enemies = pygame.image.load('explosion_enemies.png').convert_alpha()
explosion_image2 = pygame.transform.scale(explosion_load_enemies,(100,100))


#função que cria um unico inimigo
def create_enemy(x, y, image, enemy_group, enemy_list):
    new_enemy = Enemy(x, y, image)  # Crie um novo inimigo com as coordenadas x e y
    new_enemy.movimentation(starship.rect.x,starship.rect.y)
    enemy_group.add(new_enemy)  # Adicione o novo inimigo ao grupo de todos os sprites
    enemy_list.append(new_enemy)  # Adicione o novo inimigo à lista de inimigosd
    global enemies_remaining 
    enemies_remaining += 1

#grupo de sprites inimigos e lista de sprites inimigos
enemy_group = pygame.sprite.Group()
enemies = []

#imagens e tamanhos dos elementos da tela de start
image_back = pygame.image.load('init_win.png').convert_alpha()
scale_back = pygame.transform.scale(image_back,(1280,920))
image_start = pygame.image.load('start_button.png').convert_alpha()
scale_start = pygame.transform.scale(image_start,(300,125))
image_exit = pygame.image.load('exit_button.png').convert_alpha()
scale_exit = pygame.transform.scale(image_exit,(300,125))

#criação dos botões de start e exit
button_start = Button(scale_start,WIN_WIDTH//2  , WIN_HEIGHT//2 + 80)
button_exit = Button(scale_exit,WIN_WIDTH//2  ,WIN_HEIGHT//2 + 250)


#loop para exibir a tela de start/exit
start = True
while start:
    WIN.blit(scale_back,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            start = False
            pygame.quit()
    if button_start.draw(WIN):
        start = False
    if button_exit.draw(WIN):
        run = False
        start = False
        pygame.quit()
    pygame.display.update()


#grupo onde os sprites são guardados
all_sprites = pygame.sprite.Group()#cria a variável que vai guardar os sprites
all_sprites.add(starship)#adiciona um sprite dentro dela


stage = 1 #estágios do jogo

#variáveis que definem se os inimigos foram criados ou não a cada estágio
enemies_created1 = False
enemies_created2 = False
enemies_created3 = False
enemies_created4 = False
enemies_created5 = False
enemies_created6 = False
enemies_created7 = False
enemies_created8 = False
enemies_created9 = False
enemies_created10 = False
next_stage_time = pygame.time.get_ticks() #timer para mudança de estágio
enemies_remaining = 0

end_time = pygame.time.get_ticks() #time para finalização do jogo
starship_alive = True #variável que define se a nave está viva ou nao
starship_win = True

run = True #condiçao para o loop principal rodar

#loop principal do jogo, janela que vai ser exibida até que o usuário a feche
while run:
    WIN.blit(WIN_IMAGE, (0,0))
    if starship_alive and starship_win:

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
                starship.starship_aim(starship_image)
                
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        shot = Shot(bullet, starship.rect.centerx, starship.rect.centery,mouse_x,mouse_y,8)
                        all_sprites.add(shot)
                    
        if (keys[pygame.K_a] or keys[pygame.K_w] 
            or keys[pygame.K_d] or keys[pygame.K_s]):
                starship.movimentation()

        for shot in all_sprites:
            if isinstance(shot, Shot):
                shot.move()
                for enemy in enemy_group:
                    if isinstance(enemy,Enemy):
                        if shot.enemy_collision(enemy):
                            damage = shot.enemy_collision(enemy)
                            shot.shot_excluded()
                            lost_health = enemy.lost_health(damage, WIN, explosion_image2)
                            if lost_health:
                                enemy.enemy_killed()
                                enemies_remaining -= 1
                        
        for enemy in enemy_group:
            if isinstance(enemy, Enemy):
                enemy.health_bar(WIN)
                enemy.movimentation(starship.rect.x, starship.rect.y)
                enemy.other_enemy_collision(enemy_group)
                if enemy.starship_collision(starship):
                    damage2 = enemy.starship_collision(starship)
                    lost_health2 = starship.starship_lost_health(damage2,WIN,explosion_image)
                    if lost_health2:
                        starship.starship_killed()
                        starship_alive = False

        #criação dos inimigos conforme se passam os estágios
        if stage == 1 and not enemies_created1:
            enemy1 = create_enemy(350, -100, enemy_image, enemy_group, enemies)
            enemies_created1 = True
            pygame.display.flip()

        elif stage == 2 and not enemies_created2:
            enemy1 = create_enemy(350, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(350, 1000, enemy_image, enemy_group, enemies)
            enemies_created2 = True

        elif stage == 3 and not enemies_created3:
            enemy1 = create_enemy(350, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(350, 1000, enemy_image, enemy_group, enemies)
            enemy3 = create_enemy(-100, 350, enemy_image, enemy_group, enemies)
            enemies_created3 = True
            pygame.display.update()
        
        elif stage == 4 and not enemies_created4:
            enemy1 = create_enemy(350, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(350, 1000, enemy_image, enemy_group, enemies)
            enemy3 = create_enemy(-100, 350, enemy_image, enemy_group, enemies)
            enemy4 = create_enemy(1300, 350, enemy_image, enemy_group, enemies)
            enemies_created4 = True
        
        elif stage == 5 and not enemies_created5:
            enemy1 = create_enemy(350, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(350, 1000, enemy_image, enemy_group, enemies)
            enemy3 = create_enemy(-100, 350, enemy_image, enemy_group, enemies)
            enemy4 = create_enemy(1300, 350, enemy_image, enemy_group, enemies)
            enemy5 = create_enemy(750, -100, enemy_image, enemy_group, enemies)
            enemies_created5 = True
            pygame.display.update()
        
        elif stage == 6 and not enemies_created6:
            enemy1 = create_enemy(350, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(350, 1000, enemy_image, enemy_group, enemies)
            enemy3 = create_enemy(-100, 350, enemy_image, enemy_group, enemies)
            enemy4 = create_enemy(1300, 350, enemy_image, enemy_group, enemies)
            enemy5 = create_enemy(750, -100, enemy_image, enemy_group, enemies)
            enemy6 = create_enemy(750, 1000, enemy_image, enemy_group, enemies)
            enemies_created6 = True
            pygame.display.update()
        
        elif stage == 7 and not enemies_created7:
            enemy1 = create_enemy(350, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(350, 1000, enemy_image, enemy_group, enemies)
            enemy3 = create_enemy(-100, 100, enemy_image, enemy_group, enemies)
            enemy4 = create_enemy(1300, 350, enemy_image, enemy_group, enemies)
            enemy5 = create_enemy(750, -100, enemy_image, enemy_group, enemies)
            enemy6 = create_enemy(750, 1000, enemy_image, enemy_group, enemies)
            enemy7 = create_enemy(-100, 800, enemy_image, enemy_group, enemies)
            enemies_created7 = True
            pygame.display.update()
            
        elif stage == 8 and not enemies_created8:
            enemy1 = create_enemy(350, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(350, 1000, enemy_image, enemy_group, enemies)
            enemy3 = create_enemy(-100, 350, enemy_image, enemy_group, enemies)
            enemy4 = create_enemy(1300, 350, enemy_image, enemy_group, enemies)
            enemy5 = create_enemy(750, -100, enemy_image, enemy_group, enemies)
            enemy6 = create_enemy(750, 1000, enemy_image, enemy_group, enemies)
            enemy7 = create_enemy(-100, 750, enemy_image, enemy_group, enemies)
            enemy8 = create_enemy(1300, 750, enemy_image, enemy_group, enemies)
            enemies_created8 = True
            pygame.display.update()
        
        elif stage == 9 and not enemies_created9:
            enemy1 = create_enemy(100, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(100, 1000, enemy_image, enemy_group, enemies)
            enemy3 = create_enemy(-100, 350, enemy_image, enemy_group, enemies)
            enemy4 = create_enemy(1300, 350, enemy_image, enemy_group, enemies)
            enemy5 = create_enemy(500, -100, enemy_image, enemy_group, enemies)
            enemy6 = create_enemy(500, 1000, enemy_image, enemy_group, enemies)
            enemy7 = create_enemy(-100, 750, enemy_image, enemy_group, enemies)
            enemy8 = create_enemy(900, 1000, enemy_image, enemy_group, enemies)
            enemy9 = create_enemy(900, -100, enemy_image, enemy_group, enemies)
            enemies_created9 = True
            pygame.display.update()
        
        elif stage == 10 and not enemies_created10:
            enemy1 = create_enemy(100, -100, enemy_image, enemy_group, enemies)
            enemy2 = create_enemy(100, 1000, enemy_image, enemy_group, enemies)
            enemy3 = create_enemy(-100, 350, enemy_image, enemy_group, enemies)
            enemy4 = create_enemy(1300, 350, enemy_image, enemy_group, enemies)
            enemy5 = create_enemy(500, -100, enemy_image, enemy_group, enemies)
            enemy6 = create_enemy(500, 1000, enemy_image, enemy_group, enemies)
            enemy7 = create_enemy(-100, 750, enemy_image, enemy_group, enemies)
            enemy8 = create_enemy(900, 1000, enemy_image, enemy_group, enemies)
            enemy9 = create_enemy(900, -100, enemy_image, enemy_group, enemies)
            enemy10 = create_enemy(900, -100, enemy_image, enemy_group, enemies)
            enemies_created10 = True
            pygame.display.update()

                                 
        if enemies_remaining == 0:
            if pygame.time.get_ticks() - next_stage_time >= 4000:
                stage += 1
                enemies_created1 = False
                enemies_created2 = False
                enemies_created3 = False
                enemies_created4 = False
                enemies_created5 = False
                enemies_created6 = False
                enemies_created7 = False
                enemies_created8 = False
                enemies_created9 = False
                enemies_created10 = False
                next_stage_time = pygame.time.get_ticks()
        
        if enemies_remaining == 0 and stage > 10:
            starship_win = False

        starship.health_bar(WIN)
        starship.edge_collision()
        enemy_group.draw(WIN)
        all_sprites.draw(WIN)
        pygame.display.update()
        clock.tick(FPS)   

    elif starship_alive == False:
        WIN.blit(game_over_image, (390,100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    elif starship_win == False:
        WIN.blit(victory_image,(98.5,314))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

