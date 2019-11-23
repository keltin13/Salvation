############################
##     Keltin Grimes      ##
## kgrimes@andrew.cmu.edu ##
##                        ##
##     Term Project:      ##
##       Salvation        ##
##           -            ##
##     Enemy Classes      ##
############################

import pygame

class EnemySpawn(object):
    def __init__(self, x, y, textureNum):
        self.x, self.y, = x, y
        self.textureNum = textureNum
        self.time = pygame.time.get_ticks()
        self.dt = 0
        self.spawnTime = 100000
        self.xScale = self.yScale = 1
        self.vShift = 0

    def spawn(self, sprites):
        time = pygame.time.get_ticks()
        self.dt += time - self.time
        if self.dt > self.spawnTime:
            self.time = time
            self.dt = 0
            sprites.append(Enemy(self.x, self.y, 4))

class Enemy(object):
    def __init__(self, x, y, textureNum):
        self.x = x
        self.y = y
        self.speedScale = 0.00117
        self.target = (x, y)
        self.dir = (1, 0)
        self.targetDist = self.distance(self.x, self.y, *self.target)
        self.textureNum = textureNum
        self.xScale = self.yScale = 1
        self.vShift = 0

    def distance(self, x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5

    def step(self, speed):
        # Increment the position of the player
        self.x += speed * self.dir[0]
        self.y += speed * self.dir[1]

    def move(self, grid, playerX, playerY, time):
        # Move the enemy
        speed = self.speedScale * time
        self.step(speed)
        newDistance = self.distance(self.x, self.y, self.target[0], self.target[1])
        # If we moved farther away from the current target calculate a new target
        if  newDistance >= self.targetDist:
            # Get map coordinates
            x, y = int(self.x), int(self.y)
            # Check the legality of all possible directions
            allDirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            possibleDirs = []
            for dx, dy in allDirs:
                newX, newY = x + dx, y + dy
                if (newX > 0 and newX < len(grid) and newY > 0 and newY < len(grid[0])
                    and grid[newX][newY] == 0):
                    possibleDirs.append((dx, dy))
            # Find the direction closest to the player
            bestDir = possibleDirs[0]
            playerX, playerY = int(playerX), int(playerY)
            for i in range(len(possibleDirs)):
                if (self.distance(playerX, playerY, possibleDirs[i][0]+x, possibleDirs[i][1]+y) <
                        self.distance(playerX, playerY, bestDir[0]+x, bestDir[1]+y)):
                    bestDir = possibleDirs[i]
            # Update target, direction, and distance
            self.target = (bestDir[0] + x + 0.5, bestDir[1] + y + 0.5)
            self.dir = bestDir
            self.targetDist = self.distance(playerX, playerY, *self.target)
        else:   # Otherwise just update distance
            self.targetDist = newDistance
