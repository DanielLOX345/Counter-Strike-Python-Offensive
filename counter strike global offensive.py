from pygame import *
from random import randint
from time import time as timer
font.init()

window = display.set_mode((700, 500))
display.set_caption('Лабиринт')

score = 0
lost = 0
hp = 100
num_fire = 0
timer1 = timer()





background = transform.scale(image.load("galaxy.png"), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        sprite.Sprite.__init__(self)
        super().__init__ ()
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_d] and self.rect.x < 590:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -20)
        bullets.add(bullet)


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, health):
        super(). __init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.health = health
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500 :
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost = lost + 1
    def bossupdate(self):
        if self.rect.x <= 0:
            self.direction = "right"
        if self.rect.x >= 500:
            self.direction = "left"
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        
    def Bossfire(self):
        bossbullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 20)
        bossbullets.add(bossbullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
    def bossbulletupdate(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

        
            

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 700 - 80), -40, 80, 80, randint(1, 5), 1)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Enemy('asteroid.png', randint(80, 700 - 80), -40, 100, 60, randint(1,3), 2)
    asteroids.add(asteroid)

bullets = sprite.Group()
bossbullets = sprite.Group()


rocket = Player('rocket.png', 300, 400, 150, 100 , 9)
boss = Enemy('boss.png', -200, 50, 200, 200, 3, 10)



mixer.init()
mixer.music.load('mainmenu.mp3')
mixer.music.play()
kick = mixer.Sound('fire.ogg')


font3 = font.Font(None, 70)
font4 = font.Font(None, 70)

font1 = font.Font(None, 30)
font2 = font.Font(None, 30)

font5 = font.Font(None, 30)
font6 = font.Font(None, 30)


win = font3.render('COUNTER-TERRORIST WIN', True, (0, 0, 255))
lose = font4.render('TERRORIST WIN', True, (255, 0, 0))


rel_time = False
finish = False
run = True

#clock = time.Clock()
FPS = 60

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            if num_fire < 10 and rel_time == False:
                num_fire = num_fire + 1
                rocket.fire()
                kick.play()
                #boss.Bossfire()
        if num_fire >= 10 and rel_time == False:
            rel_time = True
            last_time = timer()
    

    
    timer2 = timer()
    

            

    if not finish:

        window.blit(background, (0, 0))
        bullets.update()
        rocket.reset()
        rocket.update()
        monsters.update()
        asteroids.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font6.render('Перезарядка', 1, (150, 0, 0))
                window.blit(reload,(250, 460))
            else:
                num_fire = 0
                rel_time = False
        

   
        

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 700 - 80), -40, 100, 80, randint(1, 5), 1)
            monsters.add(monster)


        
            
        collides2 = sprite.groupcollide(asteroids, bullets, False, True)
        for i in collides2:
            if i.health == 0:
                i.kill()
                asteroid = Enemy('asteroid.png', randint(80, 700 - 80), -40, 100, 80, randint(1, 3), 2)
                asteroids.add(asteroid)
            else:
                i.health -= 1
                lost += 1

        if sprite.spritecollide(rocket, asteroids, True):
            hp -= 20
        elif sprite.spritecollide(rocket, bossbullets, True):
            hp -= 100
            window.blit(lose,(140, 200))
        elif hp <= 0:
            finish = True
            window.blit(lose,(140, 200))
    
                                                                                                                                                                   

        if lost >= 15:
            finish = True
            window.blit(lose,(140, 200))
        

        text = font1.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text = font2.render('Пропущено::' + str(lost), 1, (255, 255, 255))
        window.blit(text, (10, 45))

        text = font5.render('HP:' + str(hp), 1, (255, 255, 255))
        window.blit(text, (10, 480))

        if sprite.spritecollide(rocket, monsters, True):
            hp -= 10
            
        elif hp <= 0:
            finish = True
            window.blit(lose,(140, 200))
        


        if score == 20:
            for i in monsters:
                i.kill()
            for i in asteroids:
                i.kill()
            boss.reset()
            boss.bossupdate()
            bossbullets.update()
            bossbullets.draw(window)
        
        if round(timer2 - timer1, 1)%2 == 0:
            boss.Bossfire()
            

        if sprite.spritecollide(boss, bullets, True):
                boss.health -= 1
            
            
        if boss.health == 0:  
            boss.kill()  
            finish = True
            window.blit(win,(30, 200))

    



    #clock.time.tick(FPS)            

    display.update()

'''
_1¶¶¶¶¶¶1____________________________________
8¶8__¶¶1_____________________________________
1¶¶¶¶¶¶______________________________________
8¶¶¶¶¶¶______________________________________
¶¶¶88¶¶1_____________________________________
_¶¶¶¶81______________________________________
_1__¶¶_______________________________________
_8_1¶¶¶______________________________________
__¶¶¶¶¶______________________________________
__8¶¶¶8______________________________________
___¶¶¶¶______________________________________
___1_¶¶______________________________________
___8__¶¶__________81_________________________
___8__8¶__________¶¶_____88__________________
___¶___¶8__1¶8____8¶____¶¶___________________
___¶___¶¶____¶¶8___¶1__¶¶____181_____________
___¶___¶¶______¶¶¶¶¶¶¶¶¶1_1¶¶8_______________
___18__¶¶1__11_8¶¶¶¶¶¶¶¶¶¶¶1_________________
____8__8¶¶¶88¶¶¶¶¶¶118¶¶¶¶8__111_____________
____8__18¶¶___¶¶¶¶¶18¶¶¶¶¶¶¶¶¶811____________
___8¶_8¶_1¶¶8¶¶¶8___¶__¶¶¶8__________________
__1¶¶181_1¶¶__8¶___8¶¶¶¶¶¶8__________________
__¶¶8_81188¶¶1_¶8__88¶¶¶¶¶¶__________________
__¶8_18¶¶¶_1¶¶¶88¶¶¶¶¶¶¶__¶1_________________
__¶8_8¶¶1881¶¶¶¶¶8__8¶¶¶1__8_________________
___1¶¶8888818¶¶¶¶¶____¶¶¶__8_________________
___111_88181_8¶¶¶¶¶¶¶888¶¶8¶_________________
___81__1881_8___¶¶¶1__8888_11________________
____88_881____1¶¶¶__188_8¶11_81______________
_____¶1¶8__8¶¶¶¶1_1_1¶8_¶_1¶¶8¶______________
_____¶181_8¶¶¶__8¶_1_¶1_¶1_¶¶¶¶1_______111___
_____811¶118__8¶8_8_¶¶_8¶__¶¶¶¶8_____1¶111__¶
_____8_¶8_1_8¶¶1_¶_1¶_181¶¶88¶¶81___81_____¶¶
_____81__8¶¶818_¶__¶_¶_81¶¶¶1¶¶8¶1_81_¶¶1_¶¶8
_____¶___¶81_8_¶8_¶_¶8_¶__¶¶¶¶8¶¶¶8__8___¶¶8_
____811_8_1_8_¶¶_¶_1¶__¶¶¶¶8¶¶8¶811_11_188¶8_
____8_8811_¶_1¶_81_¶118¶¶81¶¶¶¶8¶¶¶11_8¶¶¶¶1_
___1¶_88__¶8_¶8_8__¶¶81¶8__¶_¶¶¶¶¶¶1_8¶¶8¶¶__
___1¶_¶118¶_¶¶_¶___¶8__8___¶_8¶¶8¶___¶¶88¶1__
____¶_111¶__¶_1__¶__1__¶1__¶¶¶11¶1_1¶¶¶8¶1___
____¶¶18¶¶_¶¶_8_¶¶_11__¶1__¶¶___¶_1¶¶1¶¶_____
____8111¶_¶¶_1_8¶__11__¶8__¶¶___¶¶¶¶¶¶¶¶_____
____11_¶8_¶8_8_¶___8___¶8__¶¶___¶¶¶¶¶¶¶¶_____
____818¶_¶¶_1_¶¶__¶¶___¶8__¶¶___¶¶¶¶¶¶¶8_____
____88¶_1¶____¶__888___¶1__¶¶___1¶81¶¶¶______
____¶¶1_¶¶___1_1_______¶1__¶¶____18__¶8______
____¶¶__¶_____1¶_______¶1__¶¶___11¶¶1________
_____¶_¶¶____1¶1_______¶___¶¶1__¶11__________
_____¶¶¶___8¶¶1___8____¶___¶¶¶8_8____________
_____1¶8__88¶8___8¶___8¶___¶¶___¶____________
_____8¶___118____¶1___8¶___¶¶___¶____________
_____81__1¶11____¶___1¶___1¶¶___¶____________
_____8___¶1______¶___¶1__¶8__1__¶____________
_____81__1_______1_____¶8____1__¶____________
_____¶8____________8¶8¶88_18_188¶____________
_____¶¶__________8¶¶¶18¶1¶¶¶¶8¶¶¶____________
_____¶¶___1______¶¶1_8_¶1¶¶__¶__¶1___________
_____88__¶1______8¶__¶_¶881___11¶____________
_____81__8_________¶¶¶_¶81111_8¶1____________
_____8__8__________8¶¶_¶8_118_8¶_____________
_____8_18_____1118881¶_¶1_118_81_____________
_____811____¶¶¶8¶8_11¶_¶8111¶_8______________
_____88___1¶88__8__18¶_¶818_8_81_____________
_____88__1¶_1¶_188__¶¶_¶818_8_1______________
_____81__8__¶8_¶¶¶__¶¶_¶¶81_¶¶¶______________
_____18___18¶11818__¶¶_¶¶81_8¶¶______________
______¶__188118__8_1¶¶_¶¶81__¶1______________
______111¶8111¶_81__¶¶_¶¶81_1¶¶______________
_______¶8¶11811_¶88_¶¶_¶¶1__1¶1______________
______881¶181___8818¶¶_¶¶_1_181______________
_____81__8_¶1_1¶_818¶¶_¶¶___1_81_____________
___1¶___1_111_¶¶__1_¶¶_¶8_1_1118_____________
__1¶¶¶11____11¶¶8___1¶_¶8_1__11¶_____________
__¶¶¶¶¶¶88888¶¶¶¶¶888¶¶¶¶¶¶¶¶¶¶¶1_8¶1111_____
_18____________________________88__1_1_______
_18____________________________18___8¶11818¶_
_18____________________________18___81118888_
'''
