##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

from tkinter import *
from cmu_112_graphics import *

from Button import *
from Player import *
from Boundary import *
from Water import Water

# From http://www.cs.cmu.edu/~112/notes/notes-graphics-part2.html
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class MainMenuMode(Mode):
    def redrawAll(mode, canvas):
        backgroundColor = rgbString(241, 156, 183)
        canvas.create_rectangle(0, 0, mode.width, mode.height,
                                fill = backgroundColor)
        canvas.create_text(mode.width//2, mode.height//2, fill = 'black',
                        text = "Press space to start")

    def keyPressed(mode, event):
        if event.key == 'Space':    # Press 'Space' to go to game
            mode.app.setActiveMode(mode.app.introLevel)

class GameMode(Mode):
    def appStarted(mode):
        mode.activeKeys = {'a': False, 'd': False, 'w': False, 's': False}

    def keyPressed(mode, event):
        if event.key == 'q':
            mode.activePlayer = (mode.activePlayer - 1) % mode.playerTypes
            mode.players[mode.activePlayer].reset()
        elif event.key == 'e':
            mode.activePlayer = (mode.activePlayer + 1) % mode.playerTypes
            mode.players[mode.activePlayer].reset()
        elif event.key == 'Space':
            mode.players[mode.activePlayer].up()
        elif event.key in mode.activeKeys:
            mode.activeKeys[event.key] = True

    def keyReleased(mode, event):
        if event.key in mode.activeKeys:
            mode.activeKeys[event.key] = False

    def checkInBounds(mode, x, y):
        for b in mode.boundaries:
            if b.enabled == True:
                if b.left <= x <= b.right and b.top <= y <= b.bottom:
                    return True
        return False

    def checkIntersect(mode, player, boundsList):
        for b in boundsList:
            if b.enabled == True:
                if (player.pos[0] + player.width//2 >= b.left and
                    player.pos[0] - player.width//2 <= b.right and
                    player.pos[1] + player.height//2 >= b.top and
                    player.pos[1] - player.height//2 <= b.bottom):
                    return True
        return False

    def updatePhysics(mode):
        player = mode.players[mode.activePlayer]
        player.isUnderwater()
        for i in range(len(player.pos)):
            player.pos[i] += player.velocity[i]
            if mode.checkIntersect(player, mode.boundaries):
                while mode.checkIntersect(player, mode.boundaries):
                    player.pos[i] -= (player.velocity[i]/abs(player.velocity[i]))
                player.velocity[i] = 0
        if player.underwater:
            if isinstance(player, WaterBoy):
                player.airCount = player.airStamina
            if player.waterCount == player.swimStamina:
                player.velocity = [0,0]
            player.waterCount -= 1
            player.velocity[0] = 0
            if player.velocity[1] < 0:
                player.velocity[1] = 0
            player.velocity[1] -= player.gravity * 0.1       
            if player.waterCount <= 0:
                player.reset()
        else:
            if isinstance(player, WaterBoy):
                player.airCount -= 1
                if player.airCount <= 0:
                    player.airCount = player.airStamina
                    player.reset()
            player.velocity[0] = 0
            if player.standingOnPlatform():
                player.velocity[1] = 0
            else:
                player.velocity[1] -= player.gravity
        player.returnToBounds()

    def timerFired(mode):
        if mode.activeKeys['a'] == True:
            mode.players[mode.activePlayer].left()
        elif mode.activeKeys['d'] == True:
            mode.players[mode.activePlayer].right()
        if mode.activeKeys['s'] == True:
            mode.players[mode.activePlayer].down()
        elif mode.activeKeys['w'] == True:
            mode.players[mode.activePlayer].up()
        if mode.checkIntersect(mode.players[mode.activePlayer], mode.spikes):
            mode.players[mode.activePlayer].reset()
        if mode.activeButton < len(mode.buttons):
            if mode.checkIntersect(mode.players[mode.activePlayer], [mode.buttons[mode.activeButton]]):
                mode.buttons[mode.activeButton].activate()
                mode.activeButton += 1
        for button in mode.buttons:
            if isinstance(button, MovingButton) and button.updating:
                button.update()
        mode.updatePhysics()

    def redrawAll(mode, canvas):
        player = mode.players[mode.activePlayer]
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'white')
        canvas.create_text(mode.width//2, mode.height//2, fill = 'black',
                        text = f"{player}, swimTime = {player.waterCount}/{player.swimStamina}")
        for water in mode.waterBodies:
            water.draw(canvas)
        for spike in mode.spikes:
            spike.draw(canvas)
        for boundary in mode.boundaries:
            if boundary.enabled:
                boundary.draw(canvas)
        if mode.activeButton < len(mode.buttons):
            mode.buttons[mode.activeButton].draw(canvas)
        player.draw(canvas)

class Introduction(GameMode):
    def __init__(self):
        super().__init__()
        super().appStarted()
        self.scale = 1
        self.createBoundaries()
        self.createWater()
        self.createSpikes()
        self.numActives = 4
        self.createButtons()
        self.init = [25, 230]
        self.players = [Player(self, self.init[0], self.init[1]),
                        GravityBoy(self, self.init[0], self.init[1]),
                        JumpMan(self, self.init[0], self.init[1]),
                        WaterBoy(self,self.init[0],self.init[1])]
        self.playerTypes = len(self.players)
        self.activePlayer = 0
        self.activeButton = 0
        self.activeKeys = {'a': False, 'd': False, 'w': False, 's': False}

    def createBoundaries(self):
        self.boundaries = set()
        self.boundaries.add(Boundary('1', 0, 200, 50, 210, self.scale, False, 0))
        self.boundaries.add(Boundary('2', 0, 315, 50, 325, self.scale))
        self.boundaries.add(Boundary('3', 55, 345, 105, 355, self.scale))
        self.boundaries.add(Boundary('4', 60, 50, 110, 60, self.scale))

        self.boundaries.add(Boundary('Shift 1', 150, 440, 300, 450, self.scale, order = 1))
        self.boundaries.add(Boundary('Shift 2', 150, 150, 300, 400, self.scale, order = 2))
        self.boundaries.add(Boundary('Shift 3', 150, 100, 300, 110, self.scale, order = 3))

        self.boundaries.add(Boundary('5', 375, 315, 385, 450, self.scale))
    
    def createButtons(self):
        self.buttons = [None] * self.numActives
        for boundary in self.boundaries:
            if not boundary.enabled:
                self.buttons[boundary.order] = (Button(50, 300, boundary))
            if 'Shift' in boundary.name:
                self.buttons[boundary.order] = (MovingButton(100, 100, boundary, boundary.left, boundary.top+100, boundary.right, boundary.bottom+100))

    def createWater(self):
        self.waterBodies = set()
        self.waterBodies.add(Water(0, 350, 800, 450, self.scale))

    def createSpikes(self):
        self.spikes = set()
        self.spikes.add(Spikes('Spike 1', 0, 0, 100, 20, self.scale))
        self.spikes.add(Spikes('Spike 2', 100, 0, 200, 20, self.scale))

class Level1(GameMode):
    def __init__(self):
        super().__init__()

# From http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.scale = app.width/800
        app.mainMenuMode = MainMenuMode()
        app.introLevel = Introduction()
        app.level1 = Level1()
        app.setActiveMode(app.mainMenuMode) # Change to main menu
        app.timerDelay = 50

def main():
    app = MyModalApp(width=800, height=450)
    #app = MyModalApp(width=960, height=540)

if __name__ == '__main__':
    main()
