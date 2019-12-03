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
import random

class EnemySpawn(object):
    def __init__(self, x, y, textureNum):
        self.x, self.y, = x, y
        self.textureNum = textureNum
        self.time = pygame.time.get_ticks()
        self.dt = 0
        self.spawnTime = 10 * 10**5
        self.xScale = self.yScale = 1
        self.vShift = 0

    def distance(self, x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5

    def spawn(self, sprites, playerX, playerY):
        if self.distance(self.x, self.y, playerX, playerY < 10):
            time = pygame.time.get_ticks()
            self.dt += time - self.time
            if self.dt > self.spawnTime:
                self.time = time
                self.dt = 0
                sprites.append(Enemy(self.x, self.y, 4))

class EnemySpawnHard(EnemySpawn):
    def spawn(self, sprites, playerX, playerY):
        if self.distance(self.x, self.y, playerX, playerY < 10):
            time = pygame.time.get_ticks()
            self.dt += time - self.time
            if self.dt > self.spawnTime:
                self.time = time
                self.dt = 0
                monster = random.choices(['d', 'b', 'a'], cum_weights = [10, 15, 20])[0]
                if monster == 'd':      sprites.append(Demon(self.x, self.y, 4))
                elif monster == 'b':    sprites.append(Blob(self.x, self.y, 11))
                elif monster == 'a':    sprites.append(Alien(self.x, self.y, 12))

class Enemy(object):
    def __init__(self, x, y, textureNum):
        self.x = x
        self.y = y
        self.health = 2
        self.speedScale = 0.00117
        self.damage = 1
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

    # Sorts a list based on corresponding values in second list
    def dualSort(self, L, values):
        assert(len(L) == len(values))
        d = dict()
        for i in range(len(L)):
            d[L[i]] = values[i]
        sortedValues = sorted(list(d.values()), reverse=True)
        sortedKeys = []
        for val in sortedValues:
            for key in d:
                if d[key] == val:
                    sortedKeys.append(key)
                    del d[key]
                    break
        return sortedKeys

    def move(self, grid, playerX, playerY, time):
        # Move the enemy
        speed = self.speedScale * time
        if self.distance(self.x, self.y, playerX, playerY) > 1:
            self.step(speed)
            newDistance = self.distance(self.x, self.y, self.target[0], self.target[1])
        else:   # If the enemy is in attacking range, stop
            return self.damage
        # If we moved farther away from the current target calculate a new target
        if newDistance >= self.targetDist:
            # Get map coordinates
            x, y = int(self.x), int(self.y)
            # Check the legality of all possible directions
            allDirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            possibleDirs = []
            for dx, dy in allDirs:
                newX, newY = x + dx, y + dy
                if (newX > 0 and newX < len(grid) and newY > 0 and newY < len(grid[0])
                    and grid[newX][newY] == 0 and
                    not (newX == self.target[0] and newY == self.target[0])):
                    possibleDirs.append((dx, dy))
            diagonals = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
            for dx, dy in diagonals:
                newX, newY = x + dx, y + dy
                if (newX > 0 and newX < len(grid) and newY > 0 and newY < len(grid[0])
                    and grid[newX][newY] == 0 and (dx, 0) in possibleDirs and
                    (0, dy) in possibleDirs and
                    not (newX == self.target[0] and newY == self.target[0])):
                    possibleDirs.append((dx, dy))
            # Weight directions based off distance to player
            distances = []
            for dx, dy in possibleDirs:
                newX, newY = x + dx, y + dy
                distances.append(self.distance(newX, newY, playerX, playerY))
            possibleDirs = self.dualSort(possibleDirs, distances)
            possibleDirs.reverse()
            weights = [50, 65, 75, 80, 81, 82, 83, 84] # Cumulative weights
            weights = weights[0:len(possibleDirs)]
            chosenDir = random.choices(possibleDirs, cum_weights = weights, k = 1)[0]
            self.target = (chosenDir[0] + x + 0.5, chosenDir[1] + y + 0.5)
            self.dir = chosenDir
            self.targetDist = self.distance(playerX, playerY, *self.target)
        else:   # Otherwise just update distance
            self.targetDist = newDistance

class Demon(Enemy):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.health = 2
        self.speedScale = 0.00117
        self.damage = 1

class Blob(Enemy):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.health = 4
        self.speedScale = 0.00067
        self.damage = 2

class Alien(Enemy):
    def __init__(self, x, y, textureNum):
        super().__init__(x, y, textureNum)
        self.health = 1
        self.speedScale = 0.00217
        self.damage = 5
