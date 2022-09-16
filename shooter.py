from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, height, width, speed):
        super().__init__()
        self.image = transform.scale(image.load(filename), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= 2
        if keys[K_RIGHT]:
            self.rect.x += 2
        if keys[K_DOWN]:
            self.rect.y += 2
        if keys[K_UP]:
            self.rect.y -= 2
    def shoot(self):
        bullet = Bullet("/Users/kimyen/Desktop/Algo code/Shooter game/Bullet.png", self.rect.x, self.rect.top, 50, 50, 2)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > win_height:
            self.rect.y = randint(-10, -1)
            self.rect.x = randint(0, win_width-50)
            miss += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            
        
enemies = sprite.Group()

bullets = sprite.Group()

win_width = 700
win_height = 500

for i in range(7):
    enemy = Enemy("/Users/kimyen/Desktop/Algo code/Shooter game/asteroid.png", randint(0, 700), randint(0, 300), 60, 50, 1)
    enemies.add(enemy)


window = display.set_mode((win_width, win_height))
display.set_caption("Shooter game")

background = transform.scale(image.load("/Users/kimyen/Desktop/Algo code/Shooter game/space.jpg"), (700, 500))

rocket = Player("/Users/kimyen/Desktop/Algo code/Shooter game/rocket#1.png", 300, 450, 80, 80, 3)

mixer.init()
mixer.music.load('/Users/kimyen/Desktop/Algo code/Shooter game/space.ogg')
mixer.music.play()

score = 0
miss = 0
font.init()
font1 = font.Font(None, 40)
lose = font1.render("Wasted!", True, (175, 175, 255))
win = font1.render("You win", True, (255, 255, 144))
score_1 = font1.render(f"Score:{score}", True, (166, 225, 235))
miss_1 = font1.render(f"Missed:{miss}", True, (166, 225, 235))
game = True
tick = 0
finish = False

while game:
    score_1 = font1.render(f"Score:{score}", True, (166, 225, 235))
    window.blit(background,(0,0))

    rocket.draw()

    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if finish == False:
                    rocket.shoot()
                else:
                    rocket = Player("/Users/kimyen/Desktop/Algo code/Shooter game/rocket#1.png", 300, 450, 80, 80, 3)
                    score = 0
                    miss = 0
                    finish = False
    
        if e.type == QUIT:
            game = False

    enemies.draw(window)
    if tick % 2 == 0:
        enemies.update()

    bullets.draw(window)
    bullets.update()

    rocket.update()
    if not finish:
        
        window.blit(score_1, (10, 10))

        miss_1 = font1.render(f"Missed:{miss}", True, (166, 225, 235))

        window.blit(miss_1, (10, 40))
        if sprite.spritecollide(rocket, enemies, True):
            finish = True
            window.blit(lose, (290, 260))

        collisions = sprite.groupcollide(enemies, bullets, True, True)

        for i in collisions:
            score += 1
            score_1 = font1.render(f"Score: {score}", True, (166, 225, 235))

            enemy = Enemy("/Users/kimyen/Desktop/Algo code/Shooter game/asteroid.png", randint(0, 700), randint(0, 300), 60, 50, 1)
            enemies.add(enemy)

        if miss == 20:
            finish = True
            window.blit(lose, (290, 260))

        if score == 10:
            finish = True
            window.blit(win, (290, 260))

        display.update()
        tick += 1