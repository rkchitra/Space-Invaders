import pygame 
from pygame.locals import (K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,QUIT,KEYDOWN,RLEACCEL,K_SPACE)
import random 
import time 
from pygame import mixer

#1. CLASSES
class Spaceship(pygame.sprite.Sprite) :
    def __init__(self) :
        super(Spaceship,self).__init__()
        self.surf = pygame.image.load(folder+"player.png")
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect(center = (370,480))
        self.speed = 6
        self.max_health = 100
        self.health = 100
        self.lives = 2
    
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

class Bullet(pygame.sprite.Sprite) :
    def __init__(self,x,y) :
        super(Bullet,self).__init__()
        self.surf = pygame.image.load(folder+"bullet.png")
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center = (x+32,y))
        self.speed = 5
    
    def update(self) :
        if self.rect.bottom < 0 :
            self.kill()
        else :
            self.rect.move_ip(0,-self.speed)

class Enemy(pygame.sprite.Sprite) :
    def __init__(self) :
        super(Enemy,self).__init__()
        self.surf = pygame.image.load(folder+"enemy.png")
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

class Booster(pygame.sprite.Sprite) :
    def __init__(self) :
        super(Booster,self).__init__()
        global dict
        global rand_val
        global l1
        #rand_val = "shield.png"
        rand_val = random.choice(l1)
        self.surf = pygame.image.load(folder+rand_val)
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(20,SCREEN_WIDTH-20),
                random.randint(-50,-20)
            ),
        )
        self.speed = 1
    
    def update(self) :
        if self.rect.top >= SCREEN_HEIGHT :
            self.kill()
        else :
            self.rect.move_ip(0,self.speed)


#2. UTIL FUNCTIONS 

def welcome() :
    #window = pygame.display.set_mode((800,600))
    pos2 = 110
    font = pygame.font.SysFont('Consolas', 30)
    small_font = pygame.font.SysFont('Consolas',24)
    disp_text = font.render("Welcome Space Adventurer!",True,(255,255,255))
    screen.blit(disp_text,(200,30))
    screen.blit(small_font.render("Here's everything you need to know:",True,(255,255,255)),(30,90))

    #display game elements 
    elements_font = pygame.font.SysFont('Consolas',20)
    #player spaceship
    screen.blit(pygame.image.load(folder+"player.png"),(30,pos2+30))
    screen.blit(elements_font.render("Player Spaceship:Can move Up, Down, Left, Right using arrows",True,(255,255,255)),(100,pos2+50))
    
    #enemy spaceship
    screen.blit(pygame.image.load(folder+"enemy.png"),(30,pos2+120))
    screen.blit(elements_font.render("Enemy Spaceship:Try to avoid them or shoot them down",True,(255,255,255)),(100,pos2+140))

    #bullet 
    screen.blit(pygame.image.load(folder+"bullet.png"),(45,pos2+ 200))
    screen.blit(elements_font.render("Can shoot down enemy spaceships.Press spacebar to shoot",True,(255,255,255)),(100,pos2 + 210))
    
    #boosters 
    screen.blit(small_font.render("Boosters:",True,(255,255,255)),(30,pos2 + 250))

    #1. health 
    screen.blit(pygame.image.load(folder+"health.png"),(45,pos2+ 280))
    screen.blit(elements_font.render("improves player health by 20",True,(255,255,255)),(100,pos2 + 290))

    #2. extra life
    screen.blit(pygame.image.load(folder+"extra_life.png"),(500,pos2+ 280))
    screen.blit(elements_font.render("gives an extra life",True,(255,255,255)),(530,pos2 + 290))

    #3. triple bullets 
    screen.blit(pygame.image.load(folder+"triple_bullets.png"),(45,pos2+ 350))
    screen.blit(elements_font.render("makes spaceship shoot 3 bullets",True,(255,255,255)),(100,pos2 + 360))
    
    #4. immunity 
    screen.blit(pygame.image.load(folder+"shield.png"),(500,pos2+ 350))
    screen.blit(elements_font.render("provides immunity",True,(255,255,255)),(540,pos2 + 360))
    
    smallest_font = pygame.font.SysFont('Consolas', 18)
    screen.blit(smallest_font.render("P.S: You start off with 2 lives initially and max. no. of lives = 5",True,(255,255,255)),(30,pos2+410))
    screen.blit(font.render("Press any key to continue",True,(255,255,255)),(170,pos2+450))
    
    pygame.display.flip()
    run = True
    while run :
        for event in pygame.event.get() :
            if event.type == QUIT :
                run = False
            elif event.type == KEYDOWN :
                return None
    exit(0)


def fire_bullet():
    bullet_Sound.play()
    bullet = Bullet(player.rect[0],player.rect[1])
    bullets.add(bullet)
    all_sprites.add(bullet)

def fire_triple_bullet() :
    fire_bullet()
    bullet_Sound.play()
    bullet1 = Bullet(player.rect[0]-32,player.rect[1])
    bullets.add(bullet1)
    all_sprites.add(bullet1)

    bullet2 = Bullet(player.rect[0] + 32,player.rect[1])
    bullets.add(bullet2)
    all_sprites.add(bullet2)

def disp(screen,lives) :
    font = pygame.font.SysFont('Consolas', 32)
    score_val = font.render("Score:" + str(score),True,(255,255,255))
    screen.blit(score_val,(15,15))
    
    lives_disp = pygame.image.load("images/lives_icon.png")
    pos = [750,15]
    for i in range(lives) :
        screen.blit(lives_disp,pos)
        pos[0] -= 36

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
    run = True
    while run :
        for event in pygame.event.get() :
            if event.type == QUIT :
                run = False
            if event.type == KEYDOWN :
                if event.key == K_ESCAPE :
                    run = False
    pygame.quit()

        

pygame.init()



#3. VARIABLES & MISCELLANEOUS
score = 0
dict = {"health.png":1,"extra_life.png":2,"triple_bullets.png":3,"shield.png":4}
l1 = ["health.png","extra_life.png","triple_bullets.png","shield.png"]
rand_val = ""
folder = "images/"
music_folder = "sound/"
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(folder+"ufo.png")
pygame.display.set_icon(icon)
#variable for fire method; 0 => fire_bullet(), 1 => fire_triple_bullet() 
fire_method_var = 0

#variable for immunity; 0 => health reduces on collison with alien spaceship; 1 => immune to collision 
immunity = 0

#variables for displaying timer
counter, text = 0, '0'.rjust(3)
font = pygame.font.SysFont('Consolas', 36)
booster_img = ""

#4.SOUNDS 
#background sound
mixer.music.load(music_folder+'background.wav')
mixer.music.play(-1)

#sound effects
explosion_Sound = mixer.Sound(music_folder+'explosion.wav')
bullet_Sound = mixer.Sound(music_folder+'laser.wav')
booster_Sound = mixer.Sound(music_folder + 'booster.wav')

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
background = pygame.image.load(folder+"space.png")

player = Spaceship()

#5. SPRITE GROUPS 
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
celestials = pygame.sprite.Group()
boosters = pygame.sprite.Group()

all_sprites.add(player)
#6. CUSTOM EVENTS
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,500)

#booster
ADDBOOSTER = pygame.USEREVENT + 2 #add booster
pygame.time.set_timer(ADDBOOSTER,13000)

SWITCHFIRE = pygame.USEREVENT + 3 #triple bullets booster event

IMMUNITY = pygame.USEREVENT + 4 #shield booster event

ADDTIMER= pygame.USEREVENT + 5 #timer 

screen.blit(background,(0,0))
welcome()

#7. GAME LOOP
running = True
while running :
    screen.blit(background,(0,0))
    for event in pygame.event.get() :
        if event.type == QUIT :
            running = False
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                game_over()
            elif event.key == K_SPACE :
                if fire_method_var == 0 :
                    fire_bullet()
                else :
                    fire_triple_bullet()
        elif event.type == ADDENEMY :
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
        elif event.type == ADDBOOSTER :
            booster = Booster()
            boosters.add(booster)
            all_sprites.add(booster)
        
        elif event.type == SWITCHFIRE : 
            fire_method_var = 0
        
        elif event.type == IMMUNITY :
            immunity = 0
        
        elif event.type == ADDTIMER :
            counter -= 1
            text = ":"+str(counter)
            if counter > 1 :
                pygame.time.set_timer(ADDTIMER,1000)

    
    #collision between bullet and enemy
    if pygame.sprite.groupcollide(bullets,enemies,True,True) :
        score += 1
        explosion_Sound.play()

    
    #collision between player and boosters 
    if pygame.sprite.spritecollide(player,boosters,True) : #collision with health booster
        booster_Sound.play()
        boost_val = dict[rand_val]
        if boost_val == 1:
            player.health += 20
            if player.health > 100 :
                player.health = 100

        elif boost_val == 2: #collision with extra life booster
            if player.lives < 5 :
                player.lives += 1
        
        elif boost_val == 3 : #triple bullets
            fire_method_var = 1
            pygame.time.set_timer(SWITCHFIRE,7000)
            counter, text = 7, ':7'
            booster_img = "triple_bullets.png"
            pygame.time.set_timer(ADDTIMER,1000)
        
        elif boost_val == 4 : #immunity booster
            immunity = 1
            pygame.time.set_timer(IMMUNITY,7000)
            counter, text = 7, ':7'
            booster_img = "shield.png"
            pygame.time.set_timer(ADDTIMER,1000)

    
    #collision between player and enemy
    if pygame.sprite.spritecollide(player, enemies,True):
        explosion_Sound.play()
        score += 1
        if immunity == 0 :
            player.health -= 10
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
    boosters.update()
    player.healthbar(screen)

    for entity in all_sprites :
        screen.blit(entity.surf,entity.rect)
    if counter > 0 :
        screen.blit(pygame.image.load(folder+booster_img), (25, 48))
        screen.blit(font.render(text, True, (255, 255, 255)), (55, 48))
    pygame.display.flip()
    clock.tick(120)

pygame.quit()