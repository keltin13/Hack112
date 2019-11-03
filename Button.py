##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

from tkinter import *
from PIL import *
import random

class Button(object):
    def __init__(self, app, x, y, boundary, enabled = True):
        self.app = app
        self.x = x
        self.y = y
        self.r = 5
        self.left = self.x - self.r
        self.right = self.x + self.r
        self.top = self.y - self.r
        self.bottom = self.y + self.r
        self.boundary = boundary
        self.enabled = enabled
        self.importSprite()

    def activate(self):
        self.boundary.enabled = True
    
    def draw(self, canvas):
        photoImage = self.app.getCachedImages(self.sprite)
        canvas.create_image(self.x, self.y, image=photoImage)
    
    def importSprite(self):
        candy = 'Assets/lollipopFruitGreen.png'
        self.sprite = (Image.open(candy).resize((10, 10)))


class MovingButton(Button):
    def __init__(self, app, x, y, boundary, left, top, right, bottom):
        super().__init__(app, x, y, boundary)
        self.newLeft = left
        self.newTop = top
        self.newRight = right
        self.newBottom = bottom
        self.shiftSpeed = 1
        self.updating = False
    
    def update(self):
        if self.boundary.top > self.newTop:
            self.boundary.top -= self.shiftSpeed
        elif self.boundary.top < self.newTop:
            self.boundary.top += self.shiftSpeed
        if self.boundary.bottom < self.newBottom:
            self.boundary.bottom += self.shiftSpeed
        elif self.boundary.bottom > self.newBottom:
            self.boundary.bottom -= self.shiftSpeed
        if self.boundary.left > self.newLeft:
            self.boundary.left -= self.shiftSpeed
        elif self.boundary.left < self.newLeft:
            self.boundary.left += self.shiftSpeed
        if self.boundary.right < self.newRight:
            self.boundary.right += self.shiftSpeed
        elif self.boundary.right > self.newRight:
            self.boundary.right -= self.shiftSpeed
        if (self.boundary.top == self.newTop and
            self.boundary.bottom == self.newBottom and
            self.boundary.left == self.newLeft and
            self.boundary.right == self.newRight):
            self.updating = False

    def activate(self):
        self.updating = True