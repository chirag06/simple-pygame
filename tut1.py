import pygame
from random import seed
from random import randint
seed(1)
pygame.init()
screenWidth = 500
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("First Game")


clock = pygame.time.Clock()
score = 0
level = 0
dead = 0

walkRight = [pygame.image.load('img/R1.png'), pygame.image.load('img/R2.png'), pygame.image.load('img/R3.png'), pygame.image.load('img/R4.png'), pygame.image.load('img/R5.png'), pygame.image.load('img/R6.png'), pygame.image.load('img/R7.png'), pygame.image.load('img/R8.png'), pygame.image.load('img/R9.png')]
walkLeft = [pygame.image.load('img/L1.png'), pygame.image.load('img/L2.png'), pygame.image.load('img/L3.png'), pygame.image.load('img/L4.png'), pygame.image.load('img/L5.png'), pygame.image.load('img/L6.png'), pygame.image.load('img/L7.png'), pygame.image.load('img/L8.png'), pygame.image.load('img/L9.png')]
bg = pygame.image.load('img/bg.jpg')
char = pygame.image.load('img/standing.png')

bulletSound = pygame.mixer.Sound('img/bullet.wav')
hitSound = pygame.mixer.Sound('img/hit.wav')
music = pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1)

class player(object):
    def __init__(self,x,y,width,height):
        self.x = 50
        self.y = 400
        self.width = 64
        self.height = 64
        self.vel = 5
        self.left = False
        self.right = True
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x+17, self.y+11, 29, 52)
        self.life = 5
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x+17, self.y+11, 29, 52)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        self.isJump =False
        self.jumpCount = 10
        self.x = 10
        self.y = 400
        self.walkCount = 0
        fontHit = pygame.font.SysFont('comicsans',100)
        text = fontHit.render('-5',1,(255,0,0))
        win.blit(text, ((screenWidth/2) - (text.get_width()/2),screenHeight/2))
        resetGoblin(0)
        pygame.display.update()
        i = 0
        self.life-=1
        while( i < 100):
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    i = 301
                    pygame.quit()

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('img/R1E.png'), pygame.image.load('img/R2E.png'), pygame.image.load('img/R3E.png'), pygame.image.load('img/R4E.png'), pygame.image.load('img/R5E.png'), pygame.image.load('img/R6E.png'), pygame.image.load('img/R7E.png'), pygame.image.load('img/R8E.png'), pygame.image.load('img/R9E.png'), pygame.image.load('img/R10E.png'), pygame.image.load('img/R11E.png')]
    walkLeft = [pygame.image.load('img/L1E.png'), pygame.image.load('img/L2E.png'), pygame.image.load('img/L3E.png'), pygame.image.load('img/L4E.png'), pygame.image.load('img/L5E.png'), pygame.image.load('img/L6E.png'), pygame.image.load('img/L7E.png'), pygame.image.load('img/L8E.png'), pygame.image.load('img/L9E.png'), pygame.image.load('img/L10E.png'), pygame.image.load('img/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [0, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x+17, self.y+2, 31, 57)
        self.health = 10
        self.visible = True
# Goes inside the enemy class
    def draw(self, win):
        self.move()
        if(self.visible):
            if self.walkCount + 1 >= 33: # Since we have 11 images for each animtion our upper bound is 33.
                                         # We will show each image for 3 frames. 3 x 11 = 33.
                self.walkCount = 0

            if self.vel > 0: # If we are moving to the right we will display our walkRight images
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:  # Otherwise we will display the walkLeft images
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1

            pygame.draw.rect(win,(255,0,0),(self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0], self.hitbox[1] - 20,50 - (5*(10 - self.health)),10))
            self.hitbox = (self.x+17, self.y+2, 31, 57)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    # Goes inside the enemy class
    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x +  self.vel < self.path[1]: # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else: # Change direction and move back the other way
                self.vel = self.vel * -1
                #self.x += self.vel
                self.walkCount = 0
        else: # If we are moving left
            if self.x -  self.vel > self.path[0]: # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                #self.x += self.vel
                self.walkCount = 0
    def hit(self):
        if(self.health > 0 ):
            self.health -=1
        else:
            self.visible = False




def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Life:' + str(man.life) + ' Level: ' + str(level) + ' Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (150,10))
    man.draw(win)
    for goblin in goblins:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

def resetGoblin(newGoblin):
    for goblin in goblins:
        goblin.health = 10
        if(newGoblin):
            goblin.visible = True
        goblin.x = randint(80, 300)
    if(newGoblin):
        x_pos = randint(80, 300)
        goblins.append(enemy(x_pos, 410, 64, 64, 450))

#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
goblins = [enemy(350, 410, 64, 64, 450)]
#goblins[0] = enemy(0, 410, 64, 64, 450)
#goblins[1] = enemy(200, 410, 64, 64, 450)
man = player(200, 410, 64,64)
run = True
bullets = [] # This goes right above the while loop
shootLoop = 0

while run:
    clock.tick(27)   #every second at most 27 frames should pass.

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    killed = 0
    for goblin in goblins:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1] and goblin.visible: # Checks x coords
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]: # Checks y coords
                score -= 5
                man.hit() # calls enemy hit method
        if(not goblin.visible):
            killed+=1
    for bullet in bullets:
        for goblin in goblins:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1] and goblin.visible: # Checks x coords
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: # Checks y coords
                    score += 1
                    goblin.hit() # calls enemy hit method
                    hitSound.play()
                    if(bullet in bullets):
                        bullets.pop(bullets.index(bullet)) # removes bullet from bullet list

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel  # Moves the bullet by its vel
        elif bullet in bullets:
            bullets.pop(bullets.index(bullet))  # This will remove the bullet if it is off the screen
    if(killed==len(goblins)):
        killed = 0
        resetGoblin(1)
        man.x = 10
        man.y = 400
        man.isJump = False
        man.jumpCount = 10
        level = level + 1
        fontHit = pygame.font.SysFont('comicsans',100)
        text = fontHit.render('Level Up', 1, (255,0,0))
        win.blit(text, ((screenWidth/2) - (text.get_width()/2),screenHeight/2))
        i = 0
        pygame.display.update()
        while( i < 200):
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    i = 301
                    pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and (man.x < screenWidth-man.width):
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else: # If the character is not moving we will set both left and right false and reset the animation counter (walkCount)
        man.standing = True
        man.walkCount = 0
    # Goes inside the while loop, under keys = ...
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5+level:  # This will make sure we cannot exceed 5 bullets on the screen at once
            bullets.append(projectile(round(man.x+man.width//2), round(man.y + man.height//2), 6, (0,0,0), facing))
    # This will create a bullet starting at the middle of the character
        shootLoop = 1
    if not(man.isJump):
         if keys[pygame.K_UP]:
            man.isJump = True
            #right = False
            #left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10 :
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.jumpCount = 10
            man.isJump = False

    if(man.life<1):
        fontHit = pygame.font.SysFont('comicsans',100)
        text = fontHit.render('Game Over', 1, (255,0,0))
        win.blit(text, ((screenWidth/2) - (text.get_width()/2),screenHeight/2))
        i = 0
        pygame.display.update()
        while( i < 200):
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    i = 301
                    pygame.quit()
        man.life = 2
        level = 0
        score = 0
        goblins = goblins[0:1]
        resetGoblin(0)
    redrawGameWindow()
pygame.quit()
