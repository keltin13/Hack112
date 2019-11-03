##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################
import copy

class Player(object):
    def __init__(self, app, x, y):
        self.app = app
        self.pos = [x, y]
        self.width = 10
        self.height = 20
        self.swimStamina = 100
        self.gravity = -1
        self.underwater = False
        self.waterCount = self.swimStamina
        self.jumpForce = 5
        self.movementSpeed = 5
        self.velocity = [0,0]

    def reset(self):
        self.pos = copy.copy(self.app.init)
        self.velocity = [0,0]

    def draw(self, canvas):
        x, y = self.pos[0], self.pos[1]
        canvas.create_rectangle((x-self.width//2), (y-self.height//2),
                                (x+self.width//2), (y+self.height//2),
                                fill = 'black')

    def up(self):
        if self.standingOnPlatform():
            self.velocity[1] = -self.jumpForce
        elif self.underwater:
            self.velocity[1] = self.movementSpeed*0.8

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
        return (self.app.checkInBounds(self.pos[0], self.pos[1] + 1 + self.height//2)
                or self.pos[1] + self.height//2 + 1 > self.app.height)

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
        self.swimStamina = 300
        self.waterCount = self.swimStamina

class GravityBoy(Player):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.gravity = 1
        self.jumpForce = -5

    def standingOnPlatform(self):
        return (self.app.checkInBounds(self.pos[0], self.pos[1] - 1 - self.height//2)
                or self.pos[1] - self.height//2 - 1 <= 0)

    def returnToPlatform(self):
        while self.standingOnPlatform():
            self.pos[1] += 1
        self.pos[1] -= 1

class JumpMan(Player):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.jumpForce = 10
