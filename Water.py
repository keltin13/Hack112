##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

class Water(object):
    def __init__(self, left, top, right, bottom, scale):
        self.left = left*scale
        self.top = top*scale
        self.right = right*scale
        self.bottom = bottom*scale

    def draw(self, canvas):
        canvas.create_rectangle(self.left, self.top,
                                self.right, self.bottom,
                                fill = 'lightblue', outline = 'black', width = 1)
