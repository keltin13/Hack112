##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

from tkinter import *
from PIL import *

class Boundary(object):
    def __init__(self, name, left, top, right, bottom, scale):
        self.name = name
        self.left = left*scale
        self.top = top*scale
        self.right = right*scale
        self.bottom = bottom*scale
        #self.importSprites()

    def importSprites(self):
        pass

    def draw(self, canvas):
        canvas.create_rectangle(self.left, self.top,
                                self.right, self.bottom,
                                fill = 'white', outline = 'red', width = 1)
        canvas.create_line(self.left, self.top,
                            self.right, self.bottom,
                            fill = 'red')
        canvas.create_line(self.right, self.top,
                            self.left, self.bottom,
                            fill = 'red')

    def getHashables(self):
        return self.name

    def __eq__(self):
        return (isinstance(other, Boundary) and
                self.getHashables() == other.getHashables())

    def __hash__(self):
        return hash(self.getHashables())

class Spikes(Boundary):
    def importSprites(self):
        spike1 = 'Assets/spikes1.png'
        spike2 = 'Assets/spikes2.png'
        spike3 = 'Assets/spikes3.png'
        self.sprites = []
        self.sprites.append(Image.open(spike1).resize((50, 50)))
        self.sprites.append(Image.open(spike2).resize((50, 50)))
        self.sprites.append(Image.open(spike3).resize((50, 50)))

    def draw(self, canvas):
        midX = (self.right+self.left)/2
        midY = (self.top+self.bottom)/2
        canvas.create_polygon(self.left, self.top, midX, self.bottom,
                                self.right, self.top, fill = 'red')
        '''
        sprite = self.sprites[0]
        canvas.create_image(400, 400,  image=ImageTk.PhotoImage(sprite))
        start = 0
        while start + 50 < self.right - self.left:
            sprite = self.sprites[0]
            canvas.create_image(midX+start, self.bottom, image=ImageTk.PhotoImage(sprite))
            start += 50
        '''
