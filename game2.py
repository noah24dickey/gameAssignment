import pygame
pygame.init()

screenheight = 480 #sets the parameters of the game window
screenwidth = 500

clock = pygame.time.Clock()
score = 0 #counts your score in the top left corner

win = pygame.display.set_mode((screenwidth, screenheight))

walkRight = [pygame.image.load('resources/characters/R1.png'), #images of the player
             pygame.image.load('resources/characters/R2.png'), #walking right
             pygame.image.load('resources/characters/R3.png'),
             pygame.image.load('resources/characters/R4.png'),
             pygame.image.load('resources/characters/R5.png'),
             pygame.image.load('resources/characters/R6.png'),
             pygame.image.load('resources/characters/R7.png'),
             pygame.image.load('resources/characters/R8.png'),
             pygame.image.load('resources/characters/R9.png')]
walkLeft = [pygame.image.load('resources/characters/L1.png'), #images of the player
            pygame.image.load('resources/characters/L2.png'), #walking left
            pygame.image.load('resources/characters/L3.png'),
            pygame.image.load('resources/characters/L5.png'),
            pygame.image.load('resources/characters/L4.png'),
            pygame.image.load('resources/characters/L6.png'),
            pygame.image.load('resources/characters/L7.png'),
            pygame.image.load('resources/characters/L8.png'),
            pygame.image.load('resources/characters/L9.png')]
bg = pygame.image.load('resources/bg.jpg')
char = pygame.image.load('resources/characters/standing.png') #image of hero standing

class player(object):
    def __init__(self, x, y, width, height): #characteristics of the player
        self.x = x
        self.y = y
        self.width = width
        self.height = height #player dimensions
        self.vel = 5
        self.isJump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #player hitbox

    def hit(self):
        self.x = 60 # We are resetting the player position
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100) #font and size of letters
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

    def draw(self, win):
        if self.walkCount + 1>=27:
            self.walkCount = 0
            
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y)) #defining the player walking
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y)) 
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #drawing hitbox

class projectile(object):
    def __init__(self, x, y, radius, color, facing): #characteristics of the projectile
        self.x = x
        self.y = y
        self.radius = radius #size and direction of the projectile
        self.facing = facing
        self.color = color
        self.vel = 8 * facing #speed of projectile
        
    def draw(self , win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('resources/enemy/R1E.png'), #images of the enemy walking right
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
    walkLeft = [pygame.image.load('resources/enemy/L1E.png'), #images of enemy walking left
            pygame.image.load('resources/enemy/L2E.png'),
            pygame.image.load('resources/enemy/L3E.png'),
            pygame.image.load('resources/enemy/L5E.png'),
            pygame.image.load('resources/enemy/L4E.png'),
            pygame.image.load('resources/enemy/L6E.png'),
            pygame.image.load('resources/enemy/L7E.png'),
            pygame.image.load('resources/enemy/L8E.png'),
            pygame.image.load('resources/enemy/L9E.png'),
            pygame.image.load('resources/enemy/L10E.png'),
            pygame.image.load('resources/enemy/L11E.png')]

    def __init__(self, x, y, width, height, end): #characteristics of the enemy
        self.x = x 
        self.y = y
        self.width = width #dimensions of enemy
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3 #enemy speed
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10 #enemy health
        self.visible = True
        
        

    def draw(self, win):
        self.move()
        if self.visible: 
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))#where the hitbox spawns in
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y +2, 31, 57)#hitbox size around enemy 

    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]: #showing direction and velocity of the player
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0: #defining damage done to player when enemy hits you
            self.health -= 1
        else:
            self.visible = False #makes self invisible after hit
            self.hitbox = (self.x + 0, self.y + 0, 0, 0)
            
        
    
    
def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0)) #amount of score rewarded for a hit on the enemy and score redacted when damage is taken
    win.blit(text, (0, 10))
    man.draw(win)
    goblin.draw(win)
    
    for bullet in bullets: #drawing bullets
        bullet.draw(win)
        
    pygame.display.update()

font = pygame.font.SysFont('cosmicsans', 30, True) #variables of players
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
run = True
bullets = []
while run: #shootloop
    clock.tick(27)

    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()
            score -= 5
        
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
            
        else:
            bullets.pop(bullets.index(bullet))
                

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets)< 100:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0,0,255), facing))

        shootLoop = 1 #shootloop
        
    if keys[pygame.K_LEFT] and man.x > man.vel: #defining that left arrow key moves left
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (screenwidth - (man.width - man.vel)): #defining that right arrow key moves right
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.walkCount = 0
        man.standing = True
            
    if not (man.isJump):
        if keys[pygame.K_UP]: #defining that up arrow key makes player move in the upo direction (jump)
            man.isJump = True
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

    redrawGameWindow()
        
pygame.quit() #End game
