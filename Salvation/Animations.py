############################
##     Keltin Grimes      ##
## kgrimes@andrew.cmu.edu ##
##                        ##
##     Term Project:      ##
##       Salvation        ##
##           -            ##
##   Animation Classes    ##
############################

import math

# Class for bullets to be drawn when shooting
class Bullet(object):
    def __init__(self, width, height, surface):
        self.x, self.y = width-300, height-200
        # Set path for bullet to follow
        self.target = (width/2, height/2)
        self.angle = math.asin((self.y-self.target[1])/(self.x-self.target[0]))
        self.surface = surface
        self.speedScale = 3
        self.distScale = 1

    # Step the animation
    def step(self, time):
        # Speed is independent of time and decreases towards the target
        speed = time * self.speedScale * self.distScale
        self.distScale -= 0.01
        # Move bullet
        xStep = speed * math.cos(self.angle)
        yStep = speed * math.sin(self.angle)
        self.x -= xStep
        self.y -= yStep
        # If we have reached target return True to delete instance
        if self.x < self.target[0] or self.y < self.target[1]:
            return True
        else:
            return False

    # Draw the animation
    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))
