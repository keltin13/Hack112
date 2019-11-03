##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

from tkinter import *
from PIL import *
import random

class Boundary(object):
    sprite = None
    photoImage = None
    
    def __init__(self, app, name, left, top, right, bottom, scale, enabled = True, order = -1, shiftY = 0, shiftX = 0):
        self.app = app
        self.name = name
        self.left = left*scale
        self.top = top*scale
        self.right = right*scale
        self.bottom = bottom*scale
        self.enabled = enabled
        self.order = order
        self.shiftX, self.shiftY = shiftX, shiftY
        self.importSprites()

    def importSprites(self):
        pass

    def draw(self, canvas):
        canvas.create_rectangle(self.left, self.top,
                                self.right, self.bottom,
                                fill = 'sienna', outline = 'sienna', width = 1)

    def getHashables(self):
        return self.name

    def __eq__(self):
        return (isinstance(other, Boundary) and
                self.getHashables() == other.getHashables())

    def __hash__(self):
        return hash(self.getHashables())

class Spikes(Boundary):
    def importSprites(self):
        spike2 = 'Assets/spikes2.png'
        Boundary.sprite = (Image.open(spike2).resize((50, 50)))
        Boundary.photoImage = self.app.getCachedImages(Boundary.sprite)

    def draw(self, canvas):
        start = self.left + 25
        while start <= self.right - self.left:
            canvas.create_image(start, self.top + 25, image=Boundary.photoImage)
            start += 50