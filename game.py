##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

from tkinter import *
from cmu_112_graphics import *

from Player import Player
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
                        text = "press space to start")

    def keyPressed(mode, event):
        if event.key == 'Space':    # Press 'Space' to go to game
            mode.app.setActiveMode(mode.app.gameMode)

class GameMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'black')

class Introduction(GameMode):
    def __init__(self):
        super().__init__(self)

class Level1(GameMode):
    def __init__(self):
        super().__init__(self)

# From http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.mainMenuMode = MainMenuMode()
        app.gameMode = GameMode()
        app.setActiveMode(app.mainMenuMode)
        app.timerDelay = 50

def main():
    app = MyModalApp(width=800, height=500)

if __name__ == '__main__':
    main()
