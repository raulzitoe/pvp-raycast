class Sprites():

    def __init__(self, x, y, dir_x, dir_y, image):
        self.x = x
        self.y = y
        self.image = image
        self.speed = 0.3
        self.dir_x = dir_x
        self.dir_y = dir_y
    
    def move(self):
        self.x +=  self.dir_x*self.speed
        self.y += self.dir_y*self.speed