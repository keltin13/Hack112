##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

from tkinter import *
from cmu_112_graphics import *
from PIL import *
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
        if mode.players[mode.activePlayer].velocity[0] < 0:
            mode.players[mode.activePlayer].facingRight = False
            mode.players[mode.activePlayer].stepAnimation()
        elif mode.players[mode.activePlayer].velocity[0] > 0:
            mode.players[mode.activePlayer].facingRight = True
            mode.players[mode.activePlayer].stepAnimation()
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

    def getCachedImages(mode, image):
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

class Introduction(GameMode):
    def __init__(self):
        super().__init__()
        super().appStarted()
        self.scale = 2
        self.createBoundaries()
        self.createWater()
        self.createSpikes()
        self.numActives = 5
        self.buttonLocations = [(360, 335), (360, 335), (360, 335), (400, 335), (515, 90)]
        self.createButtons()
        self.init = [25*self.scale, 250*self.scale]
        self.players = [Player(self, self.init[0], self.init[1]),
                        GravityBoy(self, self.init[0], self.init[1]),
                        JumpMan(self, self.init[0], self.init[1]),
                        WaterBoy(self,self.init[0],self.init[1])]
        self.playerTypes = len(self.players)
        self.activePlayer = 0
        self.activeButton = 0

    def createBoundaries(self):
        self.boundaries = set()
        self.boundaries.add(Boundary(self, '1', 0, 150, 50, 160, self.scale))
        self.boundaries.add(Boundary(self, '2', 0, 315, 50, 325, self.scale))
        self.boundaries.add(Boundary(self, '3', 55, 345, 105, 355, self.scale))
        self.boundaries.add(Boundary(self, '4', 60, 50, 110, 60, self.scale))
        self.boundaries.add(Boundary(self, 'Shift 1', 150, 440, 300, 450, self.scale, 
                                     order = 0, shiftY = -95))
        self.boundaries.add(Boundary(self, 'Shift 2', 150, 150, 295, 355, self.scale, 
                                     order = 1, shiftY = -50))
        self.boundaries.add(Boundary(self, 'Shift 3', 150, 100, 300, 110, self.scale, 
                                     order = 2, shiftY = -50))
        self.boundaries.add(Boundary(self, 'Shift 4', 375, 280, 385, 400, self.scale, 
                                     order = 4, shiftY = 75))
        self.boundaries.add(Boundary(self, '5', 350, 345, 450, 355, self.scale))
        self.boundaries.add(Boundary(self, '6', 325, 60, 425, 70, self.scale))
        self.boundaries.add(Boundary(self, 'Shift 5', 550, 70, 650, 80, self.scale,
                                     order = 3, shiftX = -80))
        self.boundaries.add(Boundary(self, '9', 650, 345, 800, 355, self.scale))
        self.boundaries.add(Boundary(self, '10', 675, 315, 700, 355, self.scale))
        self.boundaries.add(Boundary(self, '11', 700, 285, 750, 355, self.scale))
        self.boundaries.add(Boundary(self, '12', 750, 255, 800, 355, self.scale))
        self.boundaries.add(Boundary(self, '13', 450, 345, 460, 450, self.scale))

    def createWater(self):
        self.waterBodies = set()
        self.waterBodies.add(Water(self, 0, 350, 800, 450, self.scale))

    def createButtons(self):
        self.buttons = [None] * self.numActives
        for boundary in self.boundaries:
            if not boundary.enabled:
                self.buttons[boundary.order] = (Button(self, self.buttonLocations[boundary.order][0],
                                                self.buttonLocations[boundary.order][1], boundary))
            if 'Shift' in boundary.name:
                self.buttons[boundary.order] = (MovingButton(self, self.buttonLocations[boundary.order][0],
                                                self.buttonLocations[boundary.order][1], boundary, 
                                                boundary.left + boundary.shiftX*self.scale, 
                                                boundary.top + boundary.shiftY*self.scale, 
                                                boundary.right + boundary.shiftX*self.scale, 
                                                boundary.bottom + boundary.shiftY*self.scale))

    def createSpikes(self):
        self.spikes = set()
        self.spikes.add(Spikes(self, 'Spike 1', 0, 0, 800, 20, self.scale))

class Level1(GameMode):
    def __init__(self):
        super().__init__()
        super().appStarted()
        self.scale = 1
        self.createBoundaries()
        self.createWater()
        self.createSpikes()
        self.numActives = -1
        self.buttonLocations = [(360, 335), (360, 335), (360, 335), (400, 335), (515, 90)]
        self.createButtons()
        self.init = [25, 400]
        self.players = [Player(self, self.init[0], self.init[1]),
                        GravityBoy(self, self.init[0], self.init[1]),
                        JumpMan(self, self.init[0], self.init[1]),
                        WaterBoy(self,self.init[0],self.init[1])]
        self.playerTypes = len(self.players)
        self.activeButton = 0
        self.activePlayer = 0
        self.activeKeys = {'a': False, 'd': False, 'w': False, 's': False}
    
    def createButtons(self):
        self.buttons = [None] * self.numActives
        for boundary in self.boundaries:
            if boundary.order != -1:
                self.buttons[boundary.order] = (Button(self, self.buttonLocations[boundary.order][0],
                                                self.buttonLocations[boundary.order][1], boundary))                      
            if 'Shift' in boundary.name:
                self.buttons[boundary.order] = (MovingButton(self, self.buttonLocations[boundary.order][0],
                                                self.buttonLocations[boundary.order][1], boundary, 
                                                boundary.left + boundary.shiftX, 
                                                boundary.top + boundary.shiftY, 
                                                boundary.right + boundary.shiftX, 
                                                boundary.bottom + boundary.shiftY))

    def createBoundaries(self):
        self.boundaries = set()
        self.boundaries.add(Boundary(self, '1', 0, 150, 100, 170, self.scale))
        self.boundaries.add(Boundary(self, '2', 0, 450, 100, 470, self.scale))
        self.boundaries.add(Boundary(self, '3', 175, 520, 275, 540, self.scale))
        self.boundaries.add(Boundary(self, '4', 320, 535, 330, 605, self.scale))
        self.boundaries.add(Boundary(self, '5', 330, 595, 360, 605, self.scale))
        self.boundaries.add(Boundary(self, '6', 320, 505, 410, 535, self.scale))
        self.boundaries.add(Boundary(self, '7', 320, 485, 365, 505, self.scale))
        self.boundaries.add(Boundary(self, '8', 320, 380, 365, 445, self.scale))
        self.boundaries.add(Boundary(self, '9', 365, 380, 400, 395, self.scale))
        self.boundaries.add(Boundary(self, '10', 400, 150, 410, 395, self.scale))
        self.boundaries.add(Boundary(self, '11', 310, 285, 330, 305, self.scale))
        self.boundaries.add(Boundary(self, '12', 200, 230, 210, 250, self.scale))
        self.boundaries.add(Boundary(self, '13', 125 , 175, 175, 190, self.scale))
        self.boundaries.add(Boundary(self, '14', 410, 535, 440, 720, self.scale))
        self.boundaries.add(Boundary(self, '15', 440, 700, 600, 720, self.scale))
        self.boundaries.add(Boundary(self, '16', 600, 580, 700, 720, self.scale))
        self.boundaries.add(Boundary(self, '17', 740, 590, 840, 610, self.scale))
        self.boundaries.add(Boundary(self, '18', 700, 710, 760, 720, self.scale))
        self.boundaries.add(Boundary(self, '19', 760, 675, 770, 720, self.scale))
        self.boundaries.add(Boundary(self, '20', 770, 675, 830, 685, self.scale))
        self.boundaries.add(Boundary(self, '21', 830, 610, 840, 685, self.scale))
        self.boundaries.add(Boundary(self, '22', 900, 590, 1000, 900, self.scale))
        self.boundaries.add(Boundary(self, '23', 830, 550, 840, 590, self.scale))
        self.boundaries.add(Boundary(self, '24', 830, 530, 945, 550, self.scale))
        self.boundaries.add(Boundary(self, '25', 935, 550, 945, 590, self.scale))
        self.boundaries.add(Boundary(self, '26', 910, 250, 925, 500, self.scale))
        self.boundaries.add(Boundary(self, '27', 770, 560, 790, 570, self.scale))
        self.boundaries.add(Boundary(self, '28', 900, 300, 910, 320, self.scale))
        self.boundaries.add(Boundary(self, '29', 725, 400, 825, 420, self.scale))
        self.boundaries.add(Boundary(self, '30', 850, 235, 925, 250, self.scale))
        self.boundaries.add(Boundary(self, '31', 210, 0, 500, 10, self.scale))
        self.boundaries.add(Boundary(self, '32', 500, 0, 575, 20, self.scale))
        self.boundaries.add(Boundary(self, '33', 625, 10, 700, 20, self.scale))

    def createWater(self):
        self.waterBodies = set()
        self.waterBodies.add(Water(self, 0, 600, 1600, 900, self.scale))

    def createSpikes(self):
        self.spikes = set()
        self.spikes.add(Spikes(self, 'Spike 1', 0, 0, 50, 10, self.scale))
        self.spikes.add(Spikes(self, 'Spike 2', 50, 0, 100, 10, self.scale))

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
    app = MyModalApp(width=1600, height=900)

if __name__ == '__main__':
    main()
