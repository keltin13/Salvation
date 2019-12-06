############################
##     Keltin Grimes      ##
## kgrimes@andrew.cmu.edu ##
##                        ##
##     Term Project:      ##
##       Salvation        ##
##           -            ##
##      Item Classes      ##
############################

# Item superclass
class Item(object):
    def __init__(self, x, y, textureNum):
        # Items are static
        self.x, self.y = x, y
        self.mapX, self.mapY = int(x), int(y)
        self.textureNum = textureNum

    # Check is the player and item are within a distance of one
    def checkCollision(self, playerX, playerY):
        if self.distance(self.x, self.y, playerX, playerY) < 1:
            return self.type
        return None

    # Finds the distance between two points
    def distance(self, x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5

# Ammo - Item subclass
class Ammo(Item):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.type = 'ammo'
        # Scale properties for drawing
        self.xScale = 2
        self.yScale = 2
        self.vShift = 128

# Key - Item subclass
class Key(Item):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.type = 'key'
        # Scale properties for drawing
        self.xScale = 1
        self.yScale = 1
        self.vShift = 64

# Double Damage - Item subclass
class DoubleDamage(Item):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.type = 'doubleDamamge'
        # Scale properties for drawing
        self.xScale = self.yScale = 1
        self.vShift = 0
