############################
##     Keltin Grimes      ##
## kgrimes@andrew.cmu.edu ##
##                        ##
##     Term Project:      ##
##       Salvation        ##
##           -            ##
##      Button Class      ##
############################

import pygame

class Button(object):
    # Initialize a Button at a center point
    def __init__(self, cx, cy, w, h, surface, hoverAction = 'mouse'):
        self.cx, self.cy = cx, cy
        self.w, self.h = int(w), int(h)
        self.surface = pygame.transform.scale(surface, (self.w, self.h))
        self.hoverAction = hoverAction
        self.hovering = False
        self.clicked = False

    def mouseOver(self, x, y):
        if (x > self.cx-self.w/2 and x < self.cx+self.w/2 and
                y >= self.cy-self.h/2 and y <= self.cy+self.h/2):
            return True
        return False

    def updateHover(self, x, y):
        if self.mouseOver(x, y):
            self.hovering = True
        else:
            self.hovering = False

    def click(self, x, y):
        if self.hoverAction == 'mouseClick' and self.mouseOver(x, y):
            if self.clicked:
                self.clicked = False
            else:
                self.clicked = True

    def drawHover(self, screen):
        left = self.cx - self.w/2
        top = self.cy - self.h/2
        screen.blit(self.surface, (left, top))
        pygame.draw.rect(screen, pygame.Color(255,0,0), (left, top, self.w, self.h), 1)

    def drawStandard(self, screen):
        left = self.cx - self.w/2
        top = self.cy - self.h/2
        screen.blit(self.surface, (left, top))

    def draw(self, screen):
        if self.hovering or self.clicked:
            self.drawHover(screen)
        else:
            self.drawStandard(screen)
