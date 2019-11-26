############################
##     Keltin Grimes      ##
## kgrimes@andrew.cmu.edu ##
##                        ##
##     Term Project:      ##
##       Salvation        ##
##           -            ##
##     Enemy Classes      ##
############################

import math

class Bullet(object):
    def __init__(self, width, height, surface):
        self.x, self.y = width-300, height-200
        self.target = (width/2, height/2)
        self.angle = math.asin((self.y-self.target[1])/(self.x-self.target[0]))
        self.surface = surface
        self.speedScale = 2
        self.distScale = 1

    def step(self, time):
        speed = time * self.speedScale * self.distScale
        self.distScale -= 0.01
        xStep = speed * math.cos(self.angle)
        yStep = speed * math.sin(self.angle)
        self.x -= xStep
        self.y -= yStep
        if self.x < self.target[0] or self.y < self.target[1]:
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))
