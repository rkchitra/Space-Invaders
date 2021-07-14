import pygame 
from pygame.locals import (K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,QUIT,KEYDOWN,RLEACCEL,K_SPACE)
import random 
import time 
from pygame import mixer

score = 0
class Spaceship(pygame.sprite.Sprite) :
    def __init__(self) :
        super(Spaceship,self).__init__()
        self.surf = pygame.image.load("player.png")
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect(center = (370,480))
        self.speed = 6
        self.max_health = 100
        self.health = 100
        self.lives = 3
    
    def update(self,keys_pressed) :
        if keys_pressed[K_LEFT] :
            self.rect.move_ip(-self.speed,0)
        if keys_pressed[K_RIGHT] :
            self.rect.move_ip(self.speed,0)
        if keys_pressed[K_UP] :
            self.rect.move_ip(0,-self.speed)
        if keys_pressed[K_DOWN] :
            self.rect.move_ip(0,self.speed)
        
        if self.rect.left <= 0 :
            self.rect.left = 0
        
        if self.rect.right >= SCREEN_WIDTH - 1 :
            self.rect.right = SCREEN_WIDTH - 1
        
        if self.rect.top <= 2 :
            self.rect.top = 2
        
        if self.rect.bottom>= SCREEN_HEIGHT - 20 :
            self.rect.bottom = SCREEN_HEIGHT - 20 
    
    def healthbar(self,window) :
        pygame.draw.rect(window,(255,0,0),(self.rect[0],self.rect[1] + self.surf.get_height() + 10,self.surf.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.rect[0],self.rect[1] + self.surf.get_height() + 10,self.surf.get_width() * (self.health/self.max_health),10))

class Enemy(pygame.sprite.Sprite) :
    def __init__(self) :
        super(Enemy,self).__init__()
        self.surf = pygame.image.load("enemy.png")
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(20,SCREEN_WIDTH-20),
                random.randint(-50,-20)
            ),
        )
        self.speed = random.randint(1,3)
    
    def update(self) :
        if self.rect.top >= SCREEN_HEIGHT :
            self.kill()
        else :
            self.rect.move_ip(0,self.speed)

class Bullet(pygame.sprite.Sprite) :
    def __init__(self,x,y) :
        super(Bullet,self).__init__()
        self.surf = pygame.image.load("bullet.png")
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center = (x+32,y))
        self.speed = 5
    
    def update(self) :
        if self.rect.bottom < 0 :
            self.kill()
        else :
            self.rect.move_ip(0,-self.speed)

        



def disp(screen,lives) :
    font = pygame.font.Font('freesansbold.ttf',32)
    score_val = font.render("Score: " + str(score),True,(255,255,255))
    screen.blit(score_val,(15,15))
    
    lives_render = font.render("Lives: "+str(lives),True,(255,255,255))
    screen.blit(lives_render,(650,15))


def game_over() :
    global all_sprites
    for entity in all_sprites :
        entity.kill()
    
    font = pygame.font.Font('freesansbold.ttf',64)
    score_val = font.render("GAME OVER",True,(255,255,255))
    disp = pygame.font.Font('freesansbold.ttf',32)
    disp_score = disp.render("Score: "+str(score),True,(255,255,255))
    screen.blit(score_val,(SCREEN_WIDTH//2 - 200,SCREEN_HEIGHT//2 - 50))
    screen.blit(disp_score,(SCREEN_WIDTH//2 - 70,SCREEN_HEIGHT//2 + 50))
    pygame.display.flip()
    time.sleep(3)
        

pygame.init()
#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
background = pygame.image.load("space.png")

player = Spaceship()

#sprite groups 
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
celestials = pygame.sprite.Group()

all_sprites.add(player)
#custom events 
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,500)

#booster
ADDBOOSTER = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBOOSTER,3000)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


#game loop
running = True
while running :
    screen.blit(background,(0,0))
    for event in pygame.event.get() :
        if event.type == QUIT :
            running = False
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                running = False
            elif event.key == K_SPACE :
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                bullet = Bullet(player.rect[0],player.rect[1])
                bullets.add(bullet)
                all_sprites.add(bullet)
            elif event.key == pygame.K_q :
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                bullet1 = Bullet(player.rect[0]-32,player.rect[1])
                bullets.add(bullet1)
                all_sprites.add(bullet1)

                bullet2 = Bullet(player.rect[0] + 32,player.rect[1])
                bullets.add(bullet2)
                all_sprites.add(bullet2)


        elif event.type == ADDENEMY :
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
    
    if pygame.sprite.groupcollide(bullets,enemies,True,True) :
        score += 1
        explosion_Sound = mixer.Sound('explosion.wav')
        explosion_Sound.play()
    if pygame.sprite.spritecollide(player, enemies,True) :
        explosion_Sound = mixer.Sound('explosion.wav')
        explosion_Sound.play()
        player.health -= 10
        score += 1
        if player.health <= 0 :
            player.lives -= 1
            if player.lives < 1 :
                game_over()
                break
            else :
                player.health = 100
    keys_pressed = pygame.key.get_pressed()
    disp(screen,player.lives)
    player.update(keys_pressed)
    enemies.update()
    bullets.update()
    celestials.update()
    player.healthbar(screen)

    for entity in all_sprites :
        screen.blit(entity.surf,entity.rect)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()