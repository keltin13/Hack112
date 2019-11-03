##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20

    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.width//2, self.y-self.height//2,
                                self.x+self.width//2, self.y+self.height//2,
                                fill = 'black')
