class Button(object):
    def __init__(self, x, y, boundary, enabled = True):
        self.x = x
        self.y = y
        self.r = 5
        self.left = self.x - self.r
        self.right = self.x + self.r
        self.top = self.y - self.r
        self.bottom = self.y + self.r
        self.boundary = boundary
        self.enabled = enabled

    def activate(self):
        self.boundary.enabled = True
    
    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r,
                           self.x + self.r, self.y + self.r,
                           fill = "blue")


class MovingButton(Button):
    def __init__(self, x, y, boundary, left, top, right, bottom):
        super().__init__(x, y, boundary)
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