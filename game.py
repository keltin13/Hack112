##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

from tkinter import *
from cmu_112_graphics import *

from Player import *
from Boundary import Boundary
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
        #mode.scale = mode.app.scale
        pass

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
            if b.left <= x <= b.right and b.top <= y <= b.bottom:
                return True
        return False

    # Intersection calculator from notes
    def boundaryIntersect(mode, b, ax0, ay0, ax1, ay1):
        (bx0, by0, bx1, by1) = b.left, b.top, b.right, b.bottom
        return ((ax1 >= bx0) and (bx1 >= ax0) and
                (ay1 >= by0) and (by1 >= ay0))

    def getXIntersection(mode, pos, w, h, dir):
        x, y = pos[0], pos[1]
        for b in mode.boundaries:
            if mode.boundaryIntersect(b, x-w/2, y-h/2, x+w/2, y+h/2):
                if dir == -1 and (b.left <= x-w/2 <= b.right):
                    return b.right
                elif dir == 1 and (b.right >= x+w/2 >= b.left):
                    return b.left
        return False

    def checkIntersect(mode, player, boundsList):
        for b in boundsList:
            if b.left <= player.x <= b.right and b.top <= player.y <= b.bottom:
                return True
        return False

    def updatePhysics(mode):
        player = mode.players[mode.activePlayer]
        # if mode.checkIntersect(player, mode.waters):
        #     player.underwater = True
        # else:
        #     player.underwater = False
        for i in range(len(player.pos)):
            player.pos[i] += player.velocity[i]
        if player.underwater:
            player.velocity = [0,0]
            player.waterCount -= 1
        else:
            player.waterCount = player.swimStamina
            player.velocity[0] = 0
            if player.standingOnPlatform():
                player.returnToPlatform()
                player.velocity[1] = 0
            else:
                player.velocity[1] -= player.gravity
            player.returnToBounds()

    def timerFired(mode):
        if mode.activeKeys['a'] == True:
            mode.players[mode.activePlayer].left()
        elif mode.activeKeys['d'] == True:
            mode.players[mode.activePlayer].right()
        elif mode.activeKeys['s'] == True:
            mode.players[mode.activePlayer].down()
        elif mode.activeKeys['w'] == True:
            mode.players[mode.activePlayer].up()
        mode.updatePhysics()

    def redrawAll(mode, canvas):
        player = mode.players[mode.activePlayer]
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'white')
        canvas.create_text(mode.width//2, mode.height//2, fill = 'black',
                        text = "The game is here")
        for water in mode.waterBodies:
            water.draw(canvas, mode.scale)
        for boundary in mode.boundaries:
            boundary.draw(canvas, mode.scale)
        player.draw(canvas, mode.scale)

class Introduction(GameMode):
    def __init__(self):
        super().__init__()
        super().appStarted()
        print(self.width)
        self.scale = 1
        self.createBoundaries()
        self.createWater()
        self.init = [25, 230]
        self.players = [Player(self, self.init[0], self.init[1]),
                        GravityBoy(self, self.init[0], self.init[1]),
                        JumpMan(self, self.init[0], self.init[1])]
        self.playerTypes = len(self.players)
        self.activePlayer = 0
        self.activeKeys = {'a': False, 'd': False, 'w': False, 's': False}

    def createBoundaries(self):
        self.boundaries = set()
        self.boundaries.add(Boundary('1', 0, 200, 50, 210, self.scale))
        self.boundaries.add(Boundary('2', 0, 315, 50, 325, self.scale))
        self.boundaries.add(Boundary('3', 55, 345, 105, 355, self.scale))
        self.boundaries.add(Boundary('4', 60, 50, 110, 60, self.scale))

        self.boundaries.add(Boundary('Shift 1', 150, 440, 300, 450, self.scale))
        self.boundaries.add(Boundary('Shift 2', 150, 150, 300, 400, self.scale))
        self.boundaries.add(Boundary('Shift 3', 150, 100, 300, 110, self.scale))

        self.boundaries.add(Boundary('5', 375, 315, 385, 450, self.scale))

    def createWater(self):
        self.waterBodies = set()
        self.waterBodies.add(Water(0, 350, 800, 450, self.scale))

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
