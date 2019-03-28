import pygame
pygame.init()

screenheight = 480
screenwidth = 500

win = pygame.display.set_mode((screenwidth, screenheight))

pygame.display.set_caption("First pyGame") 

clock = pygame.time.Clock()

walkRight = [pygame.image.load('resources/characters/R1.png'),
             pygame.image.load('resources/characters/R2.png'),
             pygame.image.load('resources/characters/R3.png'),
             pygame.image.load('resources/characters/R4.png'),
             pygame.image.load('resources/characters/R5.png'),
             pygame.image.load('resources/characters/R6.png'),
             pygame.image.load('resources/characters/R7.png'),
             pygame.image.load('resources/characters/R8.png'),
             pygame.image.load('resources/characters/R9.png')]
walkLeft = [pygame.image.load('resources/characters/L1.png'),
            pygame.image.load('resources/characters/L2.png'),
            pygame.image.load('resources/characters/L3.png'),
            pygame.image.load('resources/characters/L5.png'),
            pygame.image.load('resources/characters/L4.png'),
            pygame.image.load('resources/characters/L6.png'),
            pygame.image.load('resources/characters/L7.png'),
            pygame.image.load('resources/characters/L8.png'),
            pygame.image.load('resources/characters/L9.png')]
bg = pygame.image.load('resources/bg.jpg')
char = pygame.image.load('resources/characters/standing.png')

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1>=27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.color = color
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('resources/enemy/R1E.png'),
             pygame.image.load('resources/enemy/R2E.png'),
             pygame.image.load('resources/enemy/R3E.png'),
             pygame.image.load('resources/enemy/R4E.png'),
             pygame.image.load('resources/enemy/R5E.png'),
             pygame.image.load('resources/enemy/R6E.png'),
             pygame.image.load('resources/enemy/R7E.png'),
             pygame.image.load('resources/enemy/R8E.png'),
             pygame.image.load('resources/enemy/R9E.png'),
             pygame.image.load('resources/enemy/R10E.png'),
             pygame.image.load('resources/enemy/R11E.png')]
    walkLeft = [pygame.image.load('resources/enemy/L1E.png'),
            pygame.image.load('resources/enemy/L2E.png'),
            pygame.image.load('resources/enemy/L3E.png'),
            pygame.image.load('resources/enemy/L4E.png'),
            pygame.image.load('resources/enemy/L5E.png'),
            pygame.image.load('resources/enemy/L6E.png'),
            pygame.image.load('resources/enemy/L7E.png'),
            pygame.image.load('resources/enemy/L8E.png'),
            pygame.image.load('resources/enemy/L9E.png'),
            pygame.image.load('resources/enemy/L10E.png'),
            pygame.image.load('resources/enemy/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        


#print("hello game")
def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
run = True
bullets = []
while run:
    clock.tick(27)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #exit the loop, this will stop pygame from running and not just the visual disaperrance you get from clicking the "X"
    keys = pygame.key.get_pressed()

    for bullet in bullets:
        if bullet.x< 500 and bullet.x> 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (screenwidth - (man.width - man.vel)):
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        #man.left = False
        #man.right = False
        man.walkCount = 0
        man.standing = True
        

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets)< 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0,0,0), facing))
            
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0

    else:
        if man.jumpcount >= -10:
            neg = 1
            if man.jumpcount < 0:
                neg = -1
            man.y -= (man.jumpcount ** 2) * 0.5 * neg
            man.jumpcount -= 1

        else:
            man.isJump = False
            man.jumpcount = 10


    #win.fill((0,0,0))   
    #pygame.draw.rect(win,(165, 255, 25), (x, y, width, height))
    #pygame.display.update()

    redrawGameWindow()
        
pygame.quit()
