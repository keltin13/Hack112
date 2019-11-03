##########################################
##      Suicide Squad - Hack112         ##
## Keltin Grimes, Alex White, Kevin Xie ##
##########################################

class Boundary(object):
    def __init__(self, name, left, top, right, bottom, scale):
        self.name = name
        self.left = left*scale
        self.top = top*scale
        self.right = right*scale
        self.bottom = bottom*scale

    def draw(self, canvas, scale):
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
