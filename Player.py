##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################
import copy
from tkinter import *
from PIL import *

class Player(object):
    def __init__(self, app, x, y):
        self.app = app
        self.pos = [x, y]
        self.width = 20
        self.height = 30
        self.swimStamina = 50
        self.gravity = -1
        self.underwater = False
        self.waterCount = self.swimStamina
        self.jumpForce = 8
        self.movementSpeed = 5
        self.velocity = [0,0]
        self.name = "Normal Boy"
        self.importSprites()

    def importSprites(self):
        url = 'Assets/normalBoy.png'
        spritestrip = Image.open(url)
        self.sprites = [ ]
        for i in range(2):
            sprite = spritestrip.crop((70*i, 0, 70*(i+1), 100))
            sprite = sprite.resize((self.width, self.height))
            self.sprites.append(sprite)
        self.spriteCounter = 1
        self.facingRight = True

    def __repr__(self):
        return self.name

    def reset(self):
        self.pos = copy.copy(self.app.init)
        self.velocity = [0,0]

    def draw(self, canvas):
        x, y = self.pos[0], self.pos[1]
        # canvas.create_rectangle((x-self.width//2), (y-self.height//2),
        #                         (x+self.width//2), (y+self.height//2),
        #                         fill = None, outline = 'black')
        sprite = self.sprites[self.spriteCounter]
        if self.facingRight:
            photoImage = self.app.getCachedImages(sprite)
        else:
            sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            photoImage = self.app.getCachedImages(sprite)
        canvas.create_image(self.pos[0], self.pos[1], image=photoImage)

    def stepAnimation(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)

    def up(self):
        if self.underwater:
            self.velocity[1] = -self.movementSpeed*0.8
        elif self.standingOnPlatform():
            self.velocity[1] = -self.jumpForce

    def down(self):
        if self.underwater:
            self.velocity[1] = self.movementSpeed*0.8

    def left(self):
        if self.underwater:
            self.velocity[0] = -self.movementSpeed*0.8
        else:
            self.velocity[0] = -self.movementSpeed

    def right(self):
        if self.underwater:
            self.velocity[0] = self.movementSpeed*0.8
        else:
            self.velocity[0] = self.movementSpeed

    def standingOnPlatform(self):
        return ((self.app.checkInBounds(self.pos[0] + self.width//2, self.pos[1] + 1 + self.height//2)
                or self.pos[1] + self.height//2 + 1 >= self.app.height) or 
                (self.app.checkInBounds(self.pos[0] - self.width//2, self.pos[1] + 1 + self.height//2)
                or self.pos[1] + self.height//2 + 1 >= self.app.height))

    def isUnderwater(self):
        if self.app.checkIntersect(self, self.app.waterBodies):
            self.underwater = True
        else:
            self.waterCount = self.swimStamina
            self.underwater = False

    def returnToBounds(self):
        if self.pos[1] + self.height//2 >= self.app.height:
            self.pos[1] = self.app.height - self.height//2
        elif self.pos[1] - self.height//2 <= 0:
            self.pos[1] = self.height//2
        if self.pos[0] + self.width//2 >= self.app.width:
            self.pos[0] = self.app.width - self.width//2
        elif self.pos[0] - self.width//2 <= 0:
            self.pos[0] = self.width//2

class WaterBoy(Player):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.airStamina = 50
        self.airCount = self.airStamina
        self.swimStamina = 500
        self.waterCount = self.swimStamina
        self.name = "Aquaman"

    def importSprites(self):
        url = 'Assets/waterBoy.png'
        spritestrip = Image.open(url)
        self.sprites = [ ]
        for i in range(2):
            sprite = spritestrip.crop((68*i, 0, 68*(i+1), 96))
            sprite = sprite.resize((self.width, self.height))
            self.sprites.append(sprite)
        self.spriteCounter = 1
        self.facingRight = True

class GravityBoy(Player):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.gravity = 1
        self.jumpForce = -8
        self.name = "GravityBoy"

    def importSprites(self):
        url = 'Assets/gravityBoy.png'
        spritestrip = Image.open(url)
        self.sprites = [ ]
        for i in range(2):
            sprite = spritestrip.crop((70*i, 0, 70*(i+1), 96))
            sprite = sprite.resize((self.width, self.height))
            sprite = sprite.transpose(Image.FLIP_TOP_BOTTOM)
            self.sprites.append(sprite)
        self.spriteCounter = 1
        self.facingRight = True

    def standingOnPlatform(self):
        return ((self.app.checkInBounds(self.pos[0] + self.width//2, self.pos[1] - 1 - self.height//2)
                or self.pos[1] + self.height//2 + 1 <= 0) or 
                (self.app.checkInBounds(self.pos[0] - self.width//2, self.pos[1] - 1 - self.height//2)
                or self.pos[1] + self.height//2 + 1 <= 0))

    def returnToPlatform(self):
        while self.standingOnPlatform():
            self.pos[1] += 1
        self.pos[1] -= 1

class JumpMan(Player):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.jumpForce = 14
        self.swimStamina = 0
        self.waterCount = self.swimStamina
        self.name = "Jump Man"

    def importSprites(self):
        url = 'Assets/jumpBoy.png'
        spritestrip = Image.open(url)
        self.sprites = [ ]
        for i in range(2):
            sprite = spritestrip.crop((70*i, 0, 70*(i+1), 96))
            sprite = sprite.resize((self.width, self.height))
            self.sprites.append(sprite)
        self.spriteCounter = 1
        self.facingRight = True
