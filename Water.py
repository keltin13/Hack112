##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

from tkinter import *
from PIL import *
import random

class Water(object):
    def __init__(self, app, left, top, right, bottom, scale, enabled = True):
        self.app = app
        self.left = left*scale
        self.top = top*scale
        self.right = right*scale
        self.bottom = bottom*scale
        self.enabled = enabled
        self.importSprites()

    def importSprites(self):
        water = 'Assets/iceWaterDeepAlt.png'
        self.sprite = (Image.open(water).resize((self.right-self.left, self.bottom-self.top)))

    def draw(self, canvas):
        photoImage = self.app.getCachedImages(self.sprite)
        cy = self.top + (self.bottom - self.top)/2
        cx = self.left + (self.right - self.left)/2
        canvas.create_image(cx, cy, image=photoImage)
