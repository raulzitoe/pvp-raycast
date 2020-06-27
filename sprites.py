class Sprites():

    def __init__(self, x, y, dir_x, dir_y, image, speed, is_player=False, uDiv=0, vDiv=0, name="Player"):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.uDiv = uDiv
        self.vDiv = vDiv
        self.is_player = is_player
        self.kills = 0
        self.deaths = 0
        self.name = name
    
    def move(self):
        self.x +=  self.dir_x*self.speed
        self.y += self.dir_y*self.speed