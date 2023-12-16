from pygame import *
from random import randint
from time import time as timer
clock = time.Clock()
FPS = 60
win_width = 600
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption('shooter')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 535:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
lost = 0
score = 0
num_fire = 0
rel_time = False
rel_start = timer()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 565:
            self.rect.y = 0
            self.rect.x = randint(50, 550)
            self.speed = randint(2,5)
            lost = lost + 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 565:
            self.rect.y = 0
            self.rect.x = randint(50, 550)
            self.speed = randint(2,4)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

player = Player('rocket.png', 5, 500, 65, 65, 7)
enemies = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(50, 550), 50, 65, 50, randint(2, 3))
    enemies.add(enemy)
for i in range(3) :
    asteroid = Asteroid('asteroid.png', randint(50, 550), 50, 65, 50, randint(2, 3))
    asteroids.add(asteroid)
font.init()
bullets = sprite.Group()
   
font1 = font.SysFont(None, 36)
font2 = font.SysFont(None, 70)
win = font2.render('ес - 3 вуху  ', True, (213, 89, 99))
lose = font2.render('ты проиграл', True, (123,177,93))
mixer.init()

# mixer.music.load('space.ogg')
# mixer.music.play()
# fireSound = mixer.Sound('fire.ogg')

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                    # fireSound.play()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    rel_start = timer()
                

                
    if finish != True:
        window.blit(background, (0, 0))
        text_lose = font1.render('Пропущено: ' + str (lost), 1, (255, 255, 255))
        text_score = font1.render('уничтожен : ' + str (score), 1, (255, 255, 255))
        window.blit(text_score, (10, 50))
        window.blit(text_lose, (10, 10))
        player.reset()
        player.update()
        enemies.update()
        enemies.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        sprites_list = sprite.groupcollide(enemies, bullets, True, True)
        for e in sprites_list:
            score += 1
            enemy = Enemy('ufo.png', randint(50, 550), 50, 65, 50, randint(2, 3 ))
            enemies.add(enemy)
        for e in sprites_list:  
            asteroid = Asteroid('ufo.png', randint(50, 550), 50, 65, 50, randint(2, 3))
            asteroids.add(enemy)
        if sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose, (50,300))
            mixer.music.stop() 
        
        if score >= 30:
            finish = True
            window.blit(win, (150, 300))
        if lost >= 20:
            finish = True
            window.blit(lose, (50, 300))
        if rel_time == True:
            rel_end = timer()
            if rel_end - rel_start < 3:
                reload = font1  .render('reloading....', 1, (150,0,0))
                window.blit(reload, (200, 400))
            else:
                num_fire = 0
                rel_time = False
                
        
            
        
    display.update()
    clock.tick(FPS)
