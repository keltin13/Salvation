############################
##     Keltin Grimes      ##
## kgrimes@andrew.cmu.edu ##
##                        ##
##     Term Project:      ##
##       Salvation        ##
##           -            ##
##      Mode Classes      ##
############################

import pygame
import math, string, random, decimal
from Button import *
from Enemy import *
from Item import *
from Animations import *

##################################
## Mode Superclass
##################################
class Mode(object):
    # Initialize the mode
    def __init__(self, width, height, res, fps, texW, texH):
        self.width = width
        self.height = height
        self.resolution = res
        self.fps = fps
        self.textureWidth = texW
        self.textureHeight = texH
        self.importAssets()
        self.createFonts()
        self.addButtons()
        self.appStarted()

    def importAssets(self):     pass
    def createFonts(self):      pass
    def addButtons(self):       pass
    def appStarted(self):       pass

    def checkModeSwitch(self, currentMode):
        if self.tempName != currentMode:
            currentMode = self.tempName
            self.tempName = self.name
        return currentMode

    # Function from http://blog.lukasperaza.com/getting-started-with-pygame/
    def isKeyPressed(self, key, _keys):
        return _keys.get(key, False)

    def timerFired(self):               pass
    def mousePressed(self, x, y):       pass
    def mouseReleased(self, x, y):      pass
    def mouseMotion(self, x, y):        pass
    def mouseDrag(self, x, y):          pass
    def keyPressed(self, key, mod):     pass
    def keyReleased(self, key, mod):    pass
    def checkDownKeys(self, _keys):     pass

    # Event handler from http://blog.lukasperaza.com/getting-started-with-pygame/
    def eventWrapper(self, events, _keys):
        self.timerFired()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousePressed(*(event.pos))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouseReleased(*(event.pos))
            elif event.type == pygame.MOUSEMOTION and event.buttons == (0, 0, 0):
                self.mouseMotion(*(event.pos))
            elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                self.mouseDrag(*(event.pos))
            elif event.type == pygame.KEYDOWN:
                _keys[event.key] = True
                self.keyPressed(event.key, event.mod)
            elif event.type == pygame.KEYUP:
                _keys[event.key] = False
                self.keyReleased(event.key, event.mod)
                if event.key == pygame.K_ESCAPE:    return False
            elif event.type == pygame.QUIT:
                return False
        self.checkDownKeys(_keys)
        return True

    def redrawAll(self, screen):
        font = pygame.font.Font(None, 40)
        screen.blit(font.render(self.name, False, pygame.Color(255, 255, 255)),
                        (self.width/2, self.height/2))

##################################
## MainMenuMode Class
##################################
# To do:
#   - tighten button box
#   - hovering cursor for button
#   - moving clouds, etc.
class MainMenuMode(Mode):
    def appStarted(self):
        self.name = 'mainMenu'
        self.tempName = self.name
        self.startRandom = False
        self.clouds = []
        self.timerCount = 300

    def importAssets(self):
        self.textures = []
        scale = 1.3
        folder = 'Assets/'
        urls =  [
                    'cloud1.png',
                    'cloud2.png',
                    'cloud3.png'
                ]
        for url in urls:
            image = pygame.image.load(folder + url)  # Load image
            image = image.convert_alpha()            # Convert pixel format
            image = pygame.transform.scale(image,
                                            (int(image.get_width()*scale),
                                             int(image.get_height()*scale)))
            self.textures.append(image)
        self.background = []
        self.background.append(pygame.image.load('Assets/cloud1.png').convert_alpha())
        self.background.append(pygame.image.load('Assets/cloud2.png').convert_alpha())
        self.background.append(pygame.image.load('Assets/cloud3.png').convert_alpha())
        self.background.append(pygame.image.load('Assets/cloud4.png').convert_alpha())
        self.background.append(pygame.image.load('Assets/cloud5.png').convert_alpha())

    def createFonts(self):
        # Title
        self.titleFont = pygame.font.SysFont('Vivaldi', 150)
        self.titleSurface = self.titleFont.render('Salvation', True, (0, 0, 0))
        self.titleWidth, self.titleHeight = self.titleSurface.get_size()
        self.titleX = self.width/2 - self.titleWidth/2
        self.titleY = self.height/10
        # Buttons
        self.buttonFont = pygame.font.SysFont('Vivaldi', 40)
        self.bigButtonFont = pygame.font.SysFont('Vivaldi', 50)
        self.campaignButton = self.bigButtonFont.render('Campaign', True, (0, 0, 0))
        self.levelEditorButton = self.buttonFont.render('Level Editor', True, (0, 0, 0))
        self.randomButton = self.buttonFont.render('Random Map', True, (0, 0, 0))

    def addButtons(self):
        # Menu buttons
        self.cx1, self.cy1 = 3*self.width/12, 4*self.height/7
        self.cx2, self.cy2 = 9*self.width/12, 4*self.height/7
        self.cx3, self.cy3 = self.width/2, 5*self.height/7
        self.buttons = [
            Button(self.cx1, self.cy1+self.randomButton.get_height()//2,
                    *self.randomButton.get_size(), self.randomButton),
            Button(self.cx2, self.cy2, *self.levelEditorButton.get_size(), self.levelEditorButton),
            Button(self.cx3, self.cy3+2*self.campaignButton.get_height()/3, *self.campaignButton.get_size(), self.campaignButton),
        ]

    def timerFired(self):
        for i in range(len(self.clouds)-1,-1,-1):
            if self.clouds[i].cx > self.width + 50:
                self.clouds.pop(i)
            else:
                self.clouds[i].cx += 2 * self.clouds[i].scale
        if self.timerCount > 300:
            self.timerCount = 1
            surface = random.choice(self.background)
            y = random.randint(0, self.height//2)
            scale = random.randint(2, 5)/10
            self.clouds.append(Button(-20, y, scale*surface.get_width(),
                                        scale*surface.get_height(), surface))
            self.clouds[-1].scale = scale

        self.timerCount += 1

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

    def distance(self, x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5

    def getLegalMoves(self, current, width, height):
        dirs = [(0,1),(1,0),(-1,0),(0,-1)]
        legalMoves = []
        for dx, dy in dirs:
            x = current[0] + dx
            y = current[1] + dy
            if x >= 0 and x < width and y >= 0 and y < height:
                legalMoves.append((x, y))
        return legalMoves

    def exportMap(self, grid):
        width, height = len(grid), len(grid[0])
        mapString = f'1.5,1.5:{width},{height}\n'
        mapString += self.spawnItems(grid)
        mapString += '1' * (height+2) + '\n'
        for row in grid:
            mapString += '1'
            mapString += ''.join(row)
            mapString += '1\n'
        mapString += '1' * (height+2)
        mapString = mapString[:-2] + '41'
        # From http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
        with open('Levels/randomLevel1.txt', "w+") as f:
            f.write(mapString)

    def spawnItems(self, grid):
        itemString = ''
        items = [None, 'S', 'A', 'D', 'K']
        weights = [588, 593, 598, 599, 600]
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[x][y] == '0':
                    item = random.choices(items, cum_weights = weights, k = 1)[0]
                    if item != None:
                        itemString += f'{item}{x+1.5},{y+1.5}:'
        return itemString[:-1] + '\n'

    def generateMap(self, width = 20, height = 60, iters = 2):
        grid = [['1'] * height for _ in range(width)]
        start, end = (0, 0), (width-1, height-1)
        grid[start[0]][start[1]] = '0'

        for current in [(0,0), (width//2, 0), (0, height//2), (width//2, height-1), (width-1, height//2)]:
            for i in range(iters):
                if i < iters-1:
                    goal = (random.randint(0, width-1), random.randint(0, height-1))
                else:
                    goal = end
                while current != goal:
                    moves = self.getLegalMoves(current, width, height)
                    distances = [self.distance(move[0], move[1], goal[0], goal[1]) for move in moves]
                    moves = self.dualSort(moves, distances)
                    moves.reverse()
                    weights = [40, 65, 85, 100]
                    weights = weights[0:len(moves)]
                    current = random.choices(moves, cum_weights = weights, k = 1)[0]
                    grid[current[0]][current[1]] = '0'
        self.exportMap(grid)

    def mousePressed(self, x, y):
        # Random Map Button
        w, h = self.textures[0].get_width()/2, self.textures[0].get_height()/2
        if x >= self.cx1-w and x <= self.cx1+w and y >= self.cy1-h and y <= self.cy1+h:
            self.generateMap()
            self.startRandom = True
            self.tempName = 'campaign'
        # Level editor button
        w, h = self.textures[1].get_width()/2, self.textures[1].get_height()/2
        if x >= self.cx2-w and x <= self.cx2+w and y >= self.cy2-h and y <= self.cy2+h:
            self.tempName = 'levelEditor'
        # Campaign Button
        w, h = self.textures[2].get_width()/2, self.textures[2].get_height()/2
        cy3 = self.cy3+2*self.campaignButton.get_height()/3
        if x >= self.cx3-w and x <= self.cx3+w and y >= self.cy3-h and y <= self.cy3+h:
            self.tempName = 'campaign'

    def redrawAll(self, screen):
        screen.fill((145, 238, 255))
        for cloud in self.clouds:
            cloud.draw(screen)
        cloud1, cloud2, cloud3 = self.textures[0], self.textures[1], self.textures[2]
        screen.blit(cloud1, (self.cx1-cloud1.get_width()//2, self.cy1-cloud1.get_height()//2))
        screen.blit(cloud2, (self.cx2-cloud2.get_width()//2, self.cy2-cloud2.get_height()//2))
        screen.blit(cloud3, (self.cx3-cloud3.get_width()//2, self.cy3-cloud3.get_height()//2))
        screen.blit(self.titleSurface, (self.titleX, self.titleY))
        for button in self.buttons:
            button.draw(screen)

##################################
## CampaignMode Class
##################################
# To Do:
#   - Ammo flickering
class CampaignMode(Mode):
    def appStarted(self, levelName = 'sysLevel1'):
        self.name = 'campaign'
        self.tempName = self.name
        self.playerHealth = 100
        # Item storage
        self.backpack = []
        # Shooting variables
        self.lastMouseX = None
        self.shotFired = False
        self.enemyHit = -1
        self.ammo = 25
        self.damage = 1
        self.bullets = []
        # Level map
        self.levelName = levelName
        self.levelMap = self.importMap()
        self.mapWidth = len(self.levelMap)
        self.mapHeight = len(self.levelMap[0])
        # Initializes enemies and objects
        self.textureWidth, self.textureHeight = 64, 64
        self.shadowScale = 27
        #self.createSprites()
        # Set scale for walls
        self.wallScale = 1.27
        # Player position, direction vector, and camera plane
        #self.posX, self.posY = 3, 3
        self.dirX, self.dirY = 1.0, 0.0
        self.planeX, self.planeY = 0.0, -0.66

    def importAssets(self):
        self.textures = []
        folder = 'Assets/'
        urls =  [
                    'DUNGEONBRICKS2.bmp',
                    'SPOOKYDOOR.png',
                    'GOOBRICKS.bmp',
                    'portal.png',
                    'demon.png',
                    'key.png',
                    'plasmaAmmo.png',
                    'monsterSpawn.png',
                    'doubleDamage.png',
                    'key2.png',
                    'monsterSpawnHard.png',
                    'blob.png',
                    'alien.png',
                ]
        for url in urls:
            image = pygame.image.load(folder + url)     # Load image
            image = image.convert_alpha()               # Convert pixel format
            image = pygame.transform.scale(image,       # Scale to standard size
                (self.textureWidth, self.textureHeight))
            self.textures.append(image)
        # Animations
        self.bullet = pygame.image.load('Assets/plasmaBullet.png').convert_alpha()
        self.bullet = pygame.transform.rotate(self.bullet, -32)
        # HUD
        self.weapon = pygame.image.load('Assets/plasmaGun2.png').convert_alpha()
        self.weapon = pygame.transform.scale(self.weapon, (408, 90))
        self.weapon = pygame.transform.rotate(self.weapon, -32)
        self.crosshair = pygame.image.load('Assets/crosshair.png').convert_alpha()
        self.healthIcon = pygame.image.load('Assets/healthIcon.png').convert_alpha()

    def createFonts(self):
        # Ammo count
        self.HUDFont = pygame.font.SysFont('Bahnschrift', 30)
        self.ammoTitleSurface = self.HUDFont.render('Ammo:', True, (0, 0, 0))

    def createSprites(self):
        self.sprites = [
            Enemy(11.5, 5, 4),
            Ammo(6.5, 5.5, 6),
            Key(2, 2, 5),
            EnemySpawn(5.5, 16.5, 7),
            DoubleDamage(2.5, 25, 8)
        ]
        # Lists used during sprite drawing
        self.spriteOrder = [None] * len(self.sprites)
        self.spriteDistance = [None] * len(self.sprites)

    def importMap(self):
        with open(f'Levels/{self.levelName}.txt') as f:
            text = f.read()
        map = []
        self.sprites = []
        currentLine = 1
        for line in text.splitlines():
            if currentLine == 1:
                playerPos, exit = line.split(':')
                self.posX, self.posY = playerPos.split(',')
                self.posX, self.posY = float(self.posX), float(self.posY)
                self.exitX, self.exitY = exit.split(',')
                self.exitX, self.exitY = float(self.exitX), float(self.exitY)
            elif currentLine == 2:
                for item in line.split(':'):
                    itemType = item[0]
                    x, y = item[1:].split(',')
                    x, y = float(x), float(y)
                    if itemType == 'E':
                        self.sprites.append(Enemy(x, y, 4))
                    elif itemType == 'A':
                        self.sprites.append(Ammo(x, y, 6))
                    elif itemType == 'K':
                        self.sprites.append(Key(x, y, 5))
                    elif itemType == 'S':
                        self.sprites.append(EnemySpawn(x, y, 7))
                    elif itemType == 'D':
                        self.sprites.append(DoubleDamage(x, y, 8))
                    elif itemType == 'H':
                        self.sprites.append(EnemySpawnHard(x, y, 10))
            else:
                map.append([int(c) for c in line])
            currentLine += 1
        return map

    def timerFired(self):
        if (int(self.posX), int(self.posY)) == (self.exitX, self.exitY):
            if self.levelName == 'sysLevel1':
                self.interlevelMode.appStarted(self.levelName, 'sysLevel2')
                self.tempName = 'interlevel'
            elif self.levelName == 'sysLevel2':
                self.interlevelMode.appStarted(self.levelName, 'sysLevel3')
                self.tempName = 'interlevel'
            elif self.levelName == 'sysLevel3':
                self.tempName = 'mainMenu'
            elif self.levelName == 'userLevel1':
                self.tempName = 'levelEditor'
            elif self.levelName == 'randomLevel1':
                self.tempName = 'mainMenu'
        self.spawnEnemies()
        self.moveEnemies()
        self.checkItemPickup()
        self.stepAnimations()
        if not self.enemyHit == -1:
            if self.sprites[self.enemyHit].health > self.damage:
                self.sprites[self.enemyHit].health -= self.damage
            else:
                self.sprites.pop(self.enemyHit)
            self.enemyHit = -1

    def spawnEnemies(self):
        for sprite in self.sprites:
            if isinstance(sprite, EnemySpawn):
                sprite.spawn(self.sprites, self.posX, self.posY)

    def moveEnemies(self):
        # Update position of each enemy
        for sprite in self.sprites:
            if isinstance(sprite, Enemy):
                damage = sprite.move(self.levelMap, self.posX, self.posY, self.time)
                if damage != None:
                    self.playerHealth -= damage
                    if self.playerHealth <= 0:
                        self.appStarted(self.levelName)
                        self.tempName = 'mainMenu'

    def checkItemPickup(self):
        # Check if we have collided with an item
        for i in range(len(self.sprites)-1, -1, -1):
            if isinstance(self.sprites[i], Item) and self.sprites[i].checkCollision(self.posX, self.posY):
                if isinstance(self.sprites[i], Ammo):
                    self.ammo += 25
                elif isinstance(self.sprites[i], Key):
                    if 'key' not in self.backpack:
                        self.backpack.append('key')
                elif isinstance(self.sprites[i], DoubleDamage):
                    if 'double' not in self.backpack:
                        self.backpack.append('double')
                        self.damage += 1
                self.sprites.pop(i)

    def stepAnimations(self):
        for i in range(len(self.bullets)-1, -1, -1):
            if self.bullets[i].step(self.time):
                self.bullets.pop(i)

    def mousePressed(self, x, y):
        if self.ammo > 0:
            self.bullets.append(Bullet(self.width, self.height, self.bullet))
            self.shotFired = True
            self.ammo -= 1

    def keyPressed(self, key, mod):
        if key == pygame.K_b:
            self.tempName = 'mainMenu'
        elif key == pygame.K_SPACE:
            self.openDoor()

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

    # Movement algorithm taken from https://lodev.org/cgtutor/raycasting.html
    def mouseMotion(self, x, y):
        if self.lastMouseX == None:
            self.lastMouseX = x
        deltaX = (x - self.lastMouseX)/1000
        if deltaX <= 0:
            deltaX = abs(deltaX)
            # Rotate direction vector by rotaion matrix
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(deltaX) - self.dirY * math.sin(deltaX)
            self.dirY = oldDirX * math.sin(deltaX) + self.dirY * math.cos(deltaX)
            # Rotate camera plane vector by rotation matrix
            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(deltaX) - self.planeY * math.sin(deltaX)
            self.planeY = oldPlaneX * math.sin(deltaX) + self.planeY * math.cos(deltaX)
        else:
            # Rotate direction vector by rotaion matrix
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(-deltaX) - self.dirY * math.sin(-deltaX)
            self.dirY = oldDirX * math.sin(-deltaX) + self.dirY * math.cos(-deltaX)
            # Rotate camera plane vector by rotation matrix
            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(-deltaX) - self.planeY * math.sin(-deltaX)
            self.planeY = oldPlaneX * math.sin(-deltaX) + self.planeY * math.cos(-deltaX)
        self.lastMouseX = x
        self.centerMouse(x)

    def centerMouse(self, x):
        # Keep mouse on screen
        if x > self.width/2 + 100:
            pygame.mouse.set_pos([self.width/2, self.height/2])
            self.lastMouseX = self.width/2
        elif x < self.width/2 - 100:
            pygame.mouse.set_pos([self.width/2, self.height/2])
            self.lastMouseX = self.width/2
        x, y = pygame.mouse.get_pos()
        if y > self.height - 150:
            pygame.mouse.set_pos([x, 150])
        elif y < 150:
            pygame.mouse.set_pos([x, self.height-150])

    # From http://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#HelperFunctions
    def roundHalfUp(self, d):
        rounding = decimal.ROUND_HALF_UP
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    def openDoor(self):
        xDir = round(self.dirX)
        yDir = round(self.dirY)
        faceX = int(self.posX) + xDir
        faceY = int(self.posY) + yDir
        if 'key' in self.backpack and self.levelMap[faceX][faceY] == 2:
            self.levelMap[faceX][faceY] = 0

    # Movement algorithm taken from https://lodev.org/cgtutor/raycasting.html
    # Left and right strafing, though derivitave, are my own work
    def checkDownKeys(self, _keys):
        # Movement speed is based on time since last call
        self.moveSpeed = self.time * 5 / 1000
        self.strafeSpeed = self.moveSpeed / 2
        # Strafe leftward
        if self.isKeyPressed(pygame.K_a, _keys):
            # Check for wall collision in x direction
            if not self.levelMap[int(self.posX - self.dirY * self.strafeSpeed)][int(self.posY)]:
                self.posX -= self.dirY * self.strafeSpeed
            # Check for wall collision in y direction
            if not self.levelMap[int(self.posX)][int(self.posY + self.dirX * self.strafeSpeed)]:
                self.posY += self.dirX * self.strafeSpeed
        # Strafe rightward
        if self.isKeyPressed(pygame.K_d, _keys):
            # Check for wall collision in x direction
            if not self.levelMap[int(self.posX + self.dirY * self.strafeSpeed)][int(self.posY)]:
                self.posX += self.dirY * self.strafeSpeed
            # Check for wall collision in y direction
            if not self.levelMap[int(self.posX)][int(self.posY - self.dirX * self.strafeSpeed)]:
                self.posY -= self.dirX * self.strafeSpeed
        # Walk forward
        if self.isKeyPressed(pygame.K_w, _keys):
            # Check for wall collision in x direction
            if(not self.levelMap[int(self.posX + self.dirX * self.moveSpeed)][int(self.posY)]):
                self.posX += self.dirX * self.moveSpeed     # Move in x direction
            # Check for wall collision in y direction
            if(not self.levelMap[int(self.posX)][int(self.posY + self.dirY * self.moveSpeed)]):
                self.posY += self.dirY * self.moveSpeed     # Move in y direction
        # Walk backwards
        if self.isKeyPressed(pygame.K_s, _keys):
            # Check for wall collision in -x direction
            if(not self.levelMap[int(self.posX - self.dirX * self.moveSpeed)][int(self.posY)]):
                self.posX -= self.dirX * self.moveSpeed     # Move in -x direction
            if(not self.levelMap[int(self.posX)][int(self.posY - self.dirY * self.moveSpeed)]):
                self.posY -= self.dirY * self.moveSpeed     # Move in -y direction

    # Raycasting algorithm from https://lodev.org/cgtutor/raycasting.html
    # Enhanced wall drawing algoritm from https://codereview.stackexchange.com/a/160096
    def rayCast(self, screen):
        # ZBuffer stores distances to nearest wall for each column in screen
        ZBuffer = []
        # Loop through every column of the screen
        for x in range(0, self.width, self.resolution):
            # Initial camera vector setup
            cameraX = 2 * x / self.width - 1
            rayDirX = self.dirX + self.planeX * cameraX + 0.000000000000001 # Prevent division by 0
            rayDirY = self.dirY + self.planeY * cameraX + 0.000000000000001 # Prevent division by 0
            # Which square of the map the player is in
            mapX = int(self.posX)
            mapY = int(self.posY)
            # Distance from subsequent x-side to x-side and y to y
            deltaDistX = math.sqrt(1 + rayDirY ** 2 / rayDirX ** 2)
            deltaDistY = math.sqrt(1 + rayDirX ** 2 / rayDirY ** 2)
            # Calculate step and initial side distance
            if rayDirX < 0:
                stepX = -1
                sideDistX = (self.posX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1 - self.posX) * deltaDistX
            if rayDirY < 0:
                stepY = -1
                sideDistY = (self.posY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1 - self.posY) * deltaDistY
            # Digital differential analysis (DDA)
            while True:
                # Jump to next map square
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1
                # Check if ray hits wall or leaves the map boundries
                if (mapX >= self.mapWidth or mapY >= self.mapHeight or mapX < 0 or
                    mapY < 0 or self.levelMap[mapX][mapY] > 0):
                    break
            # Length of the perpendicular ray
            if side == 0: perpWallDist = (mapX - self.posX + (1 - stepX) / 2) / rayDirX
            else:         perpWallDist = (mapY - self.posY + (1 - stepY) / 2) / rayDirY
            # Length of the line to draw on the screen
            lineHeight = (self.height / perpWallDist) * self.wallScale
            # Start and end point of each line
            drawStart = -lineHeight / 2 + self.height / 2
            drawEnd =  lineHeight / 2 + self.height / 2
            # Draw textured walls
            #####################
            # Get texture number from map
            texture = self.textures[self.levelMap[mapX][mapY] - 1]
            # Get relative x-coord of wall slice
            if side == 0: wallX = self.posY + perpWallDist * rayDirY
            else:         wallX = self.posX + perpWallDist * rayDirX
            wallX -= int(wallX)
            # Scale wallX to texture size
            textureX = int(wallX * self.textureWidth)
            if side == 0 and rayDirX > 0:   textureX = self.textureWidth - textureX - 1
            if side == 1 and rayDirY < 0:   textureX = self.textureWidth - textureX - 1
            # Enhanced drawing algoritm cited at top of function
            ####################################################
            # Scale color so farther walls are darker
            c = max(1, (255 - perpWallDist * self.shadowScale) * (1 - side * .25))
            # Get location on screen
            yStart, yStop = max(0, drawStart), min(self.height, drawEnd)
            # Scale to texture size
            pixelsPerTexel = lineHeight / self.textureHeight
            colStart = int((yStart - drawStart) / pixelsPerTexel + .5)
            colHeight = int((yStop - yStart) / pixelsPerTexel + .5)
            # Recalculate screen location to reduce pixel creep
            yStart = int(colStart * pixelsPerTexel + drawStart + .5)
            yHeight = int(colHeight * pixelsPerTexel + .5)
            # Subsurface column from texture
            column = texture.subsurface((textureX, colStart, 1, colHeight))
            column = column.copy()
            # Blend with mask calculated previously
            column.fill((c, c, c), special_flags=pygame.BLEND_MULT)
            # Scale and blit to screen
            column = pygame.transform.scale(column, (self.resolution, yHeight))
            screen.blit(column, (x, yStart))
            ZBuffer.append(perpWallDist)
        return ZBuffer

    # Sprite drawing algorithm from https://lodev.org/cgtutor/raycasting.html
    # Enhanced drawing algorithm adapted from https://codereview.stackexchange.com/a/160096
    def drawSprites(self, screen, ZBuffer):
        numSprites = len(self.sprites)
        # Record the distance from each sprite to the player
        spriteOrder = []
        spriteDistance = []
        for i in range(numSprites):
            spriteOrder.append(i)
            spriteDistance.append((self.posX - self.sprites[i].x)**2 + (self.posY - self.sprites[i].y)**2)
        # Sort the sprites from nearest to furthest
        spriteOrder = self.dualSort(spriteOrder, spriteDistance)
        # Project each sprite to screen and draw if showing
        for i in range(numSprites):
            sprite = self.sprites[spriteOrder[i]]
            # Retrieve coordinates relative to player
            spriteX = sprite.x - self.posX
            spriteY = sprite.y - self.posY
            # Determinant of projection matrix
            invDet = 1.0 / (self.planeX * self.dirY - self.dirX * self.planeY)
            # Project coordinates to 3D with projection matrix
            transformX = invDet * (self.dirY * spriteX - self.dirX * spriteY)
            transformY = invDet * (-self.planeY * spriteX + self.planeX * spriteY)
            # Scales and shift for the sprite
            xScale, yScale = sprite.xScale, sprite.yScale
            vShift = sprite.vShift
            if transformY == 0: continue
            vMoveScreen = int(vShift / transformY)
            # Column of sprite on screen
            spriteScreenX = int((self.width/2) * (1 + transformX / transformY))
            # Scale sprite height to screen
            spriteHeight = abs(int(self.height / transformY)) / yScale
            drawStartY = -spriteHeight / 2 + self.height / 2 + vMoveScreen
            if drawStartY < 0: drawStartY = 0
            drawEndY = spriteHeight / 2 + self.height / 2 + vMoveScreen
            if drawEndY >= self.height: drawEndY = self.height - 1
            # Scale sprite width to screen
            spriteWidth = abs(int(self.height / transformY)) / xScale
            drawStartX = -spriteWidth / 2 + spriteScreenX
            if drawStartX < 0: drawStartX = 0
            drawEndX = spriteWidth / 2 + spriteScreenX
            if drawEndX >= self.width: drawEndX = self.width - 1
            # Get the corresponding texture
            texture = self.textures[self.sprites[spriteOrder[i]].textureNum]
            # Blit each column of the sprite to screen
            for stripe in range(int(drawStartX), int(drawEndX)):
                # Get column of texture
                texX = int((stripe - (-spriteWidth / 2 + spriteScreenX)) * self.textureWidth / spriteWidth)
                if texX < 0 or texX > 63: break     # break if out of texture dimensions
                # Draw if on screen, in front of the camera plane, and closer than the nearest wall
                if (transformY > 0 and stripe > 0 and stripe < self.width and
                        transformY < ZBuffer[stripe]):
                    if self.shotFired:
                        self.checkEnemyHit(stripe, spriteOrder[i])
                    # Enhanced drawing algoritm cited at top of function
                    ####################################################
                    # Scale color so farther walls are darker
                    c = max(1, 255 - transformY * self.shadowScale)
                    # Get location on screen
                    yStart, yStop = max(0, drawStartY), min(self.height, drawEndY)
                    # Scale to texture size
                    pixelsPerTexel = spriteHeight / self.textureHeight
                    colStart = int((yStart - drawStartY) / pixelsPerTexel + .5)
                    colHeight = int((yStop - yStart) / pixelsPerTexel + .5)
                    if colHeight < 0:   colHeight = 0
                    # Recalculate screen location to reduce pixel creep
                    yStart = int(colStart * pixelsPerTexel + drawStartY + .5)
                    yHeight = int(colHeight * pixelsPerTexel + .5)
                    # Subsurface column from texture
                    column = texture.subsurface((texX, colStart, 1, colHeight))
                    column = column.copy()
                    # Blend with mask calculated previously
                    column.fill((c, c, c), special_flags=pygame.BLEND_MULT)
                    # Scale and blit to screen
                    column = pygame.transform.scale(column, (self.resolution, yHeight))
                    screen.blit(column, (stripe, yStart))
        self.shotFired = False

    def checkEnemyHit(self, x, index):
        if x < self.width/2+5 and x > self.width/2-5 and isinstance(self.sprites[index], Enemy):
            self.enemyHit = index

    def drawAnimations(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def drawHUD(self, screen):
        # Weapon
        screen.blit(self.weapon, (self.width-325, self.height-225))
        # Crosshair
        screen.blit(self.crosshair, (self.width/2-7, self.height/2-7))
        # Item bar
        pygame.draw.rect(screen, pygame.Color(155, 155, 155),
                (0, self.height-50, self.width/3, 50), 0)
        screen.blit(self.ammoTitleSurface, (10, self.height-45))
        self.ammoCountSurface = self.HUDFont.render(f'{self.ammo}', True, (0, 0, 0))
        screen.blit(self.ammoCountSurface, (110, self.height-45))
        for i in range(len(self.backpack)):
            if self.backpack[i] == 'key':
                texture = self.textures[9]
            elif self.backpack[i] == 'double':
                texture = self.textures[8]
            texture = pygame.transform.scale(texture, (64, 64))
            screen.blit(texture, (self.width/3-64-i*80, self.height-54))
        # Health Bar
        healthStep = 2
        screen.blit(self.healthIcon, (10, 10))
        pygame.draw.rect(screen, pygame.Color(255, 0, 0),
                    (40, 10, 100*healthStep, 20))
        pygame.draw.rect(screen, pygame.Color(0, 255, 0),
                    (40, 10, self.playerHealth*healthStep, 20))

    def redrawAll(self, screen):
        pygame.draw.rect(screen, (0,0,0), (0, self.height/2, self.width, self.height), 0)
        pygame.draw.rect(screen, (0,0,50), (0, 0, self.width, self.height/2), 0)
        # Draw walls and return list of nearest wall for each screen column
        ZBuffer = self.rayCast(screen)
        self.drawSprites(screen, ZBuffer)
        self.drawAnimations(screen)
        self.drawHUD(screen)

##################################
## LevelEditorMode Class
##################################
# To-do:
# - Ensure map meets conditions
# - Drag and place
# - back button
class LevelEditorMode(Mode):
    def appStarted(self):
        self.name = 'levelEditor'
        self.startLevel = False
        self.tempName = self.name
        self.boardRows, self.boardCols = 20, 30
        self.size = 20
        self.boardLeft, self.boardTop = 300, 40
        self.buttonBoard = [[0]*self.boardCols for i in range(self.boardRows)]
        self.intBoard = [[0]*self.boardCols for i in range(self.boardRows)]
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                if i == 0 or j == 0 or i == self.boardRows-1 or j == self.boardCols-1:
                    self.buttonBoard[i][j] = Button(self.boardLeft+j*self.size, self.boardTop+i*self.size,
                                                self.size, self.size, self.textures[2])
                    self.intBoard[i][j] = 2
                else:
                    self.buttonBoard[i][j] = Button(self.boardLeft+j*self.size, self.boardTop+i*self.size,
                                                self.size, self.size, self.textures[0])
                    self.intBoard[i][j] = 0
        self.buttonSelect = None
        self.issues = []

    def importAssets(self):
        self.textures = []
        folder = 'Assets/'
        urls =  [
                    'gridCell.png',
                    'playerIcon.png',
                    'DUNGEONBRICKS2.bmp',
                    'portal.png',
                    'GOOBRICKS.bmp',
                    'monsterSpawn.png',
                    'monsterSpawnHard.png',
                    'plasmaAmmo.png',
                    'doubleDamage.png',
                    'key2.png',
                    'exitIcon.png',
                    'SPOOKYDOOR.png',
                ]
        for url in urls:
            image = pygame.image.load(folder + url)  # Load image
            image = image.convert_alpha()                     # Convert pixel format
            image = pygame.transform.scale(image,       # Scale to standard size
                (self.textureWidth, self.textureHeight))
            self.textures.append(image)

    def createFonts(self):
        # Title
        self.titleFont = pygame.font.SysFont('Vivaldi', 45)
        self.titleSurface = self.titleFont.render('Level Editor', True, pygame.Color(0, 0, 0))
        # Create level
        self.createLevelFont = pygame.font.SysFont('Vivaldi', 40)
        self.createButton = self.createLevelFont.render('Create and Play', True, pygame.Color(0, 0, 0))
        # Back button
        self.backSurface = self.createLevelFont.render('Back', True, pygame.Color(0, 0, 0))
        # Descriptions
        self.descFont = pygame.font.SysFont('Vivaldi', 25)
        self.wallsSurface = self.descFont.render('Walls', True, pygame.Color(0, 0, 0))
        self.playerSurface = self.descFont.render('Player Spawn', True, pygame.Color(0, 0, 0))
        self.spawnerSurface = self.descFont.render('Monsters', True, pygame.Color(0, 0, 0))
        self.itemsSurface = self.descFont.render('Items', True, pygame.Color(0, 0, 0))
        self.exitSurface = self.descFont.render('Exit', True, pygame.Color(0, 0, 0))
        # Issues
        self.playerIssue = self.descFont.render('Add a player spawn!', True, pygame.Color(255, 50, 50))
        self.itemIssue = self.descFont.render('Add at least one item!', True, pygame.Color(255, 50, 50))
        self.exitIssue = self.descFont.render('Add an exit!', True, pygame.Color(255, 50, 50))

    def addButtons(self):
        self.buttons = {
            'player':   Button(235, 90, 40, 40, self.textures[1], hoverAction = 'mouseClick'),
            'stone':    Button(235, 150, 40, 40, self.textures[2], hoverAction = 'mouseClick'),
            'gate':     Button(185, 150, 40, 40, self.textures[3], hoverAction = 'mouseClick'),
            'goo':      Button(135, 150, 40, 40, self.textures[4], hoverAction = 'mouseClick'),
            'easy':     Button(185, 210, 40, 40, self.textures[5], hoverAction = 'mouseClick'),
            'hard':     Button(235, 210, 40, 40, self.textures[6], hoverAction = 'mouseClick'),
            'ammo':     Button(235, 270, 40, 40, self.textures[7], hoverAction = 'mouseClick'),
            'double':   Button(185, 270, 40, 40, self.textures[8], hoverAction = 'mouseClick'),
            'key':      Button(135, 270, 40, 40, self.textures[9], hoverAction = 'mouseClick'),
            'exit':     Button(235, 330, 40, 40, self.textures[10], hoverAction = 'mouseClick'),
            'door':     Button(235, 390, 40, 40, self.textures[11], hoverAction = 'mouseClick'),
            'create':   Button(self.width-self.createButton.get_width()/1.5,
                                self.height-self.createButton.get_height(),
                                *self.createButton.get_size(), self.createButton),
            'back':     Button(350, self.height-self.backSurface.get_height(),
                                *self.backSurface.get_size(), self.backSurface)
        }

    def mouseMotion(self, x, y):
        for button in self.buttons:
            self.buttons[button].updateHover(x, y)
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                self.buttonBoard[i][j].updateHover(x, y)

    def mousePressed(self, x, y):
        if self.buttonSelect != None:
            for i in range(self.boardRows):
                for j in range(self.boardCols):
                    if self.buttonBoard[i][j].mouseOver(x, y):
                        if self.intBoard[i][j] != self.buttonSelect:
                            self.buttonBoard[i][j].surface = pygame.transform.scale(
                                                                self.textures[self.buttonSelect],
                                                                (self.size, self.size))
                            self.intBoard[i][j] = self.buttonSelect
                        else:
                            self.buttonBoard[i][j].surface = pygame.transform.scale(
                                                                self.textures[0],
                                                                (self.size, self.size))
                            self.intBoard[i][j] = 0
                        self.buttonBoard[i][j].click(x, y)
                        return
        for button in self.buttons:
            self.buttons[button].clicked = False
            self.buttons[button].click(x, y)
        self.updateButtonSelection()
        if self.buttons['create'].mouseOver(x, y):
            if self.checkConditions():
                self.exportMap()
                self.tempName = 'campaign'
        elif self.buttons['back'].mouseOver(x, y):
            self.tempName = 'mainMenu'

    def updateButtonSelection(self):
        if self.buttons['player'].clicked:  self.buttonSelect = 1; return
        elif self.buttons['stone'].clicked: self.buttonSelect = 2; return
        elif self.buttons['gate'].clicked:  self.buttonSelect = 3; return
        elif self.buttons['goo'].clicked:   self.buttonSelect = 4; return
        elif self.buttons['easy'].clicked:  self.buttonSelect = 5; return
        elif self.buttons['hard'].clicked:  self.buttonSelect = 6; return
        elif self.buttons['ammo'].clicked:  self.buttonSelect = 7; return
        elif self.buttons['double'].clicked:  self.buttonSelect = 8; return
        elif self.buttons['key'].clicked:  self.buttonSelect = 9; return
        elif self.buttons['exit'].clicked:  self.buttonSelect = 10; return
        elif self.buttons['door'].clicked:  self.buttonSelect = 11; return

    def checkConditions(self):
        hasPlayer = hasItem = hasExit = False
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                value = self.intBoard[i][j]
                if value == 1:          hasPlayer = True
                elif 5 <= value <= 9:   hasItem = True
                elif value == 10:       hasExit = True
        self.issues = []
        if not hasPlayer:   self.issues.append('player')
        if not hasItem:     self.issues.append('item')
        if not hasExit:     self.issues.append('exit')
        return hasPlayer and hasItem and hasExit


    def exportMap(self):
        spriteString = ''
        mapString = ''
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                value = self.intBoard[i][j]
                if value == 0:
                    pass
                elif value == 1:
                    playerPos = f"{i+0.5},{j+0.5}:"
                    value = 0
                elif value == 3:
                    value = 4
                elif value <= 4:
                    value -= 1
                elif value <= 9:
                    if value == 5:      spriteString += 'S'
                    elif value == 6:    spriteString += 'H'
                    elif value == 7:    spriteString += 'A'
                    elif value == 8:    spriteString += 'D'
                    elif value == 9:    spriteString += 'K'
                    spriteString += f"{i+0.5},{j+0.5}:"
                    value = 0
                elif value == 10:
                    exitPos = f"{i},{j}\n"
                    value = 0
                elif value == 11:
                    value = 2
                mapString += str(value)
            mapString += '\n'
        spriteString = spriteString[:-1] + '\n'
        mapString = playerPos + exitPos + spriteString + mapString
        # From http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
        with open('Levels/userLevel1.txt', "w+") as f:
            f.write(mapString)
        self.tempName = 'campaign'
        self.startLevel = True

    def redrawAll(self, screen):
        screen.fill((145, 238, 255))
        screen.blit(self.titleSurface, (15, 10))
        pygame.draw.rect(screen, pygame.Color(252, 253, 222), (15, 10+self.titleSurface.get_height(),
                        30+self.titleSurface.get_width(), self.height-25-self.titleSurface.get_height()), 0)
        self.drawOptions(15, 10+self.titleSurface.get_height(), screen)
        self.drawBoard(200, 40, 20, screen)
        self.drawIssues(screen)
        for button in self.buttons:
            self.buttons[button].draw(screen)

    def drawBoard(self, x, y, size, screen):
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                self.buttonBoard[i][j].draw(screen)

    def drawOptions(self, left, top, screen):
        screen.blit(self.playerSurface, (left+5, top+5))
        screen.blit(self.wallsSurface, (left+5, top+65))
        screen.blit(self.spawnerSurface, (left+5, top+125))
        screen.blit(self.itemsSurface, (left+5, top+185))
        screen.blit(self.exitSurface, (left+5, top+245))

    def drawIssues(self, screen):
        if len(self.issues) == 0:
            return
        issue = self.issues[0]
        if issue == 'player':
            screen.blit(self.playerIssue, (self.width - 250, self.height - 40))
        elif issue == 'item':
            screen.blit(self.itemIssue, (self.width - 250, self.height - 40))
        elif issue == 'exit':
            screen.blit(self.exitIssue, (self.width - 250, self.height - 40))

##################################
## InterlevelMode Class
##################################
class InterlevelMode(Mode):
    def __init__(self, width, height, res, fps, texW, texH, campaignMode):
        super().__init__(width, height, res, fps, texW, texH)
        self.campaignMode = campaignMode

    def appStarted(self, currentLevel = 'sysLevel1', nextLevel = 'sysLevel2'):
        self.name = 'interlevel'
        self.tempName = self.name
        self.currentLevel = currentLevel
        self.nextLevel = nextLevel

    def importAssets(self):
        self.background = pygame.image.load('Assets/background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background,
                                                    (self.width, self.height))

    def createFonts(self):
        # Button font
        self.buttonFont = pygame.font.SysFont('Vivaldi', 45)
        self.playAgainSurface = self.buttonFont.render('Restart Level', True, pygame.Color(255, 255, 255))
        self.nextLevelSurface = self.buttonFont.render('Next Level', True, pygame.Color(255, 255, 255))

    def addButtons(self):
        self.buttons = {
            'play':     Button(self.width/4, 2*self.height/3, *self.playAgainSurface.get_size(),
                                self.playAgainSurface),
            'next':     Button(3*self.width/4, 2*self.height/3, *self.nextLevelSurface.get_size(),
                                self.nextLevelSurface)
        }

    def mousePressed(self, x, y):
        if self.buttons['play'].mouseOver(x, y):
            self.campaignMode.appStarted(self.currentLevel)
            self.tempName = 'campaign'
        elif self.buttons['next'].mouseOver(x, y):
            if self.nextLevel == 'mainMenu':
                self.tempName = 'mainMenu'
            else:
                self.campaignMode.appStarted(self.nextLevel)
                self.tempName = 'campaign'

    def redrawAll(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            self.buttons[button].draw(screen)
