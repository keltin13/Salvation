############################
##     Keltin Grimes      ##
## kgrimes@andrew.cmu.edu ##
##                        ##
##     Term Project:      ##
##       Salvation        ##
##           -            ##
##      Item Classes      ##
############################

class Item(object):
    def __init__(self, x, y, textureNum):
        self.x, self.y = x, y
        self.mapX, self.mapY = int(x), int(y)
        self.textureNum = textureNum

    def checkCollision(self, playerX, playerY):
        if self.distance(self.x, self.y, playerX, playerY) < 1:
            return self.type
        return None

    def distance(self, x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5

class Ammo(Item):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.type = 'ammo'
        self.xScale = 2
        self.yScale = 2
        self.vShift = 128

class Key(Item):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.type = 'key'
        self.xScale = 1
        self.yScale = 1
        self.vShift = 64

class DoubleDamage(Item):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.type = 'doubleDamamge'
        self.xScale = self.yScale = 1
        self.vShift = 0
