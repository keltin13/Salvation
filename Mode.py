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
import math
import string
from Button import *
from Enemy import *
from Item import *

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
        self.appStarted()

    def importAssets(self):     pass
    def createFonts(self):      pass
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
        # Font setup
        self.titleFont = pygame.font.SysFont('Vivaldi', 150)
        self.titleSurface = self.titleFont.render('Salvation', True, (0, 0, 0))
        self.titleWidth, self.titleHeight = self.titleSurface.get_size()
        self.titleX = self.width/2 - self.titleWidth/2
        self.titleY = self.height/6
        # Menu buttons
        self.cx1, self.cy1 = 4*self.width/12, 5*self.height/7
        self.cx2, self.cy2 = 8*self.width/12, 5*self.height/7
        self.addButtons()

    def importAssets(self):
        self.textures = []
        scale = 1.3
        folder = 'Assets/'
        urls =  [
                    'cloud1.png',
                    'cloud2.png'
                ]
        for url in urls:
            image = pygame.image.load(folder + url)  # Load image
            image = image.convert_alpha()            # Convert pixel format
            image = pygame.transform.scale(image,
                                            (int(image.get_width()*scale),
                                             int(image.get_height()*scale)))
            self.textures.append(image)

    def createFonts(self):
        # Title
        self.titleFont = pygame.font.SysFont('Vivaldi', 150)
        self.titleSurface = self.titleFont.render('Salvation', True, (0, 0, 0))
        self.titleWidth, self.titleHeight = self.titleSurface.get_size()
        self.titleX = self.width/2 - self.titleWidth/2
        self.titleY = self.height/6
        # Buttons
        self.buttonFont = pygame.font.SysFont('Vivaldi', 40)
        self.campaignButton = self.buttonFont.render('Campaign', True, (0, 0, 0))
        self.levelEditorButton = self.buttonFont.render('Level Editor', True, (0, 0, 0))

    def addButtons(self):
        pass

    def mousePressed(self, x, y):
        # Campaign Button
        w, h = self.textures[0].get_width()/2, self.textures[0].get_height()/2
        if x >= self.cx1-w and x <= self.cx1+w and y >= self.cy1-h and y <= self.cy1+h:
            self.tempName = 'campaign'
        # Level editor button
        w, h = self.textures[1].get_width()/2, self.textures[1].get_height()/2
        if x >= self.cx2-w and x <= self.cx2+w and y >= self.cy2-h and y <= self.cy2+h:
            self.tempName = 'levelEditor'

    def redrawAll(self, screen):
        screen.fill((145, 238, 255))
        cloud1 = self.textures[0]
        cloud2 = self.textures[1]
        screen.blit(cloud1, (self.cx1-cloud1.get_width()//2, self.cy1-cloud1.get_height()//2))
        screen.blit(cloud2, (self.cx2-cloud2.get_width()//2, self.cy2-cloud2.get_height()//2))
        screen.blit(self.campaignButton, (self.cx1-self.campaignButton.get_width()//2,
                                          self.cy1))
        screen.blit(self.levelEditorButton, (self.cx2-self.levelEditorButton.get_width()//2,
                                             self.cy2-self.levelEditorButton.get_height()//2))
        screen.blit(self.titleSurface, (self.titleX, self.titleY))

##################################
## CampaignMode Class
##################################
# To Do:
#   - Ammo flickering
class CampaignMode(Mode):
    def appStarted(self, levelName = 'sysLevel1'):
        self.name = 'campaign'
        self.tempName = self.name
        pygame.mouse.set_visible(0)
        pygame.event.set_grab(0)
        self.lastMouseX = None
        self.shotFired = False
        self.enemyHit = -1
        self.ammo = 25
        # Level map
        self.levelName = levelName
        self.levelMap = self.importMap()
        self.mapWidth = len(self.levelMap)
        self.mapHeight = len(self.levelMap[0])
        # Initializes enemies and objects
        self.textureWidth, self.textureHeight = 64, 64
        self.shadowScale = 27
        self.createSprites()
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
                    'DUNGEONCELL.bmp',
                    'GOOBRICKS.bmp',
                    'portal.png',
                    'blueGhost.png',
                    'key.png',
                    'plasmaAmmo.png',
                    'monsterSpawn.png'
                ]
        for url in urls:
            image = pygame.image.load(folder + url)  # Load image
            image = image.convert_alpha()                     # Convert pixel format
            image = pygame.transform.scale(image,       # Scale to standard size
                (self.textureWidth, self.textureHeight))
            self.textures.append(image)
        # HUD
        self.weapon = pygame.image.load('Assets/plasmaGun.png').convert_alpha()
        self.weapon = pygame.transform.scale(self.weapon, (450, 150))
        self.weapon = pygame.transform.rotate(self.weapon, -32)
        self.crosshair = pygame.image.load('Assets/crosshair.png').convert_alpha()

    def createFonts(self):
        # Ammo count
        self.HUDFont = pygame.font.SysFont('Bahnschrift', 30)
        self.ammoTitleSurface = self.HUDFont.render('Ammo:', True, (0, 0, 0))

    def createSprites(self):
        self.sprites = [
            Enemy(11.5, 5, 4),
            Ammo(6.5, 5.5, 6),
            Key(2, 2, 5),
            EnemySpawn(5.5, 16.5, 7)
        ]
        # Lists used during sprite drawing
        self.spriteOrder = [None] * len(self.sprites)
        self.spriteDistance = [None] * len(self.sprites)

    def importMap(self):
        with open(f'Levels/{self.levelName}.txt') as f:
            text = f.read()
        map = []
        firstLine = True
        for line in text.splitlines():
            if firstLine:
                firstLine = False
                playerPos, exit = line.split(':')
                self.posX, self.posY = playerPos.split(',')
                self.posX, self.posY = float(self.posX), float(self.posY)
                self.exitX, self.exitY = exit.split(',')
                self.exitX, self.exitY = float(self.exitX), float(self.exitY)
            else:
                map.append([int(c) for c in line])
        return map

    def keyReleased(self, key, mod):
        if key == pygame.K_c:
            self.tempName = 'levelEditor'

    def timerFired(self):
        if (int(self.posX), int(self.posY)) == (self.exitX, self.exitY):
            self.appStarted(levelName = 'sysLevel2')
        self.spawnEnemies()
        self.moveEnemies()
        self.checkItemPickup()
        if not self.enemyHit == -1:
            print('remove enemy')
            self.sprites.pop(self.enemyHit)
            self.enemyHit = -1

    def spawnEnemies(self):
        for sprite in self.sprites:
            if isinstance(sprite, EnemySpawn):
                sprite.spawn(self.sprites)

    def moveEnemies(self):
        # Update position of each enemy
        for sprite in self.sprites:
            if isinstance(sprite, Enemy):
                sprite.move(self.levelMap, self.posX, self.posY, self.time)

    def checkItemPickup(self):
        # Check if we have collided with an item
        for i in range(len(self.sprites)-1, -1, -1):
            if isinstance(self.sprites[i], Item) and self.sprites[i].checkCollision(self.posX, self.posY):
                if isinstance(self.sprites[i], Ammo):
                    self.ammo += 25
                elif isinstance(self.sprites[i], Key):
                    # add keys
                    print('got key')
                self.sprites.pop(i)

    def mousePressed(self, x, y):
        self.shotFired = True
        self.ammo -= 1

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
        if x > self.width - 400:
            pygame.mouse.set_pos([400, self.height/2])
            self.lastMouseX = 400
        elif x < 400:
            pygame.mouse.set_pos([self.width-400, self.height/2])
            self.lastMouseX = self.width-400
        x, y = pygame.mouse.get_pos()
        if y > self.height - 150:
            pygame.mouse.set_pos([x, 150])
        elif y < 150:
            pygame.mouse.set_pos([x, self.height-150])

    # Movement algorithm taken from https://lodev.org/cgtutor/raycasting.html
    # Left and right stafing, though derivitave, are my own work
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
            print('enemy hit', self.enemyHit)

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

    def redrawAll(self, screen):
        pygame.draw.rect(screen, (0,0,0), (0, self.height/2, self.width, self.height), 0)
        pygame.draw.rect(screen, (0,0,100), (0, 0, self.width, self.height/2), 0)
        # Draw walls and return list of nearest wall for each screen column
        ZBuffer = self.rayCast(screen)
        self.drawSprites(screen, ZBuffer)
        self.drawHUD(screen)

##################################
## LevelEditorMode Class
##################################
# To-do:
# - Ensure map meets conditions
# - Drag and place
class LevelEditorMode(Mode):
    def appStarted(self):
        self.name = 'levelEditor'
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
        self.addButtons()
        self.buttonSelect = None

    def importAssets(self):
        self.textures = []
        folder = 'Assets/'
        urls =  [
                    'gridCell.png',
                    'playerIcon.png',
                    'DUNGEONBRICKS2.bmp',
                    'DUNGEONCELL.bmp',
                    'GOOBRICKS.bmp',
                    'easyIcon.png',
                    'hardIcon.png',
                    'ammo.png',
                    'exitIcon.png'
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
        # Descriptions
        self.descFont = pygame.font.SysFont('Vivaldi', 25)
        self.wallsSurface = self.descFont.render('Walls', True, pygame.Color(0, 0, 0))
        self.playerSurface = self.descFont.render('Player Spawn', True, pygame.Color(0, 0, 0))
        self.spawnerSurface = self.descFont.render('Monsters', True, pygame.Color(0, 0, 0))
        self.itemsSurface = self.descFont.render('Items', True, pygame.Color(0, 0, 0))
        self.exitSurface = self.descFont.render('Exit', True, pygame.Color(0, 0, 0))

    def addButtons(self):
        self.buttons = {
            'player':   Button(235, 90, 40, 40, self.textures[1], hoverAction = 'mouseClick'),
            'stone':    Button(235, 150, 40, 40, self.textures[2], hoverAction = 'mouseClick'),
            'gate':     Button(185, 150, 40, 40, self.textures[3], hoverAction = 'mouseClick'),
            'goo':      Button(135, 150, 40, 40, self.textures[4], hoverAction = 'mouseClick'),
            'easy':     Button(185, 210, 40, 40, self.textures[5], hoverAction = 'mouseClick'),
            'hard':     Button(235, 210, 40, 40, self.textures[6], hoverAction = 'mouseClick'),
            'ammo':     Button(235, 270, 40, 40, self.textures[7], hoverAction = 'mouseClick'),
            'exit':     Button(235, 330, 40, 40, self.textures[8], hoverAction = 'mouseClick'),
            'create':   Button(self.width-self.createButton.get_width()/1.5,
                                self.height-self.createButton.get_height(),
                                *self.createButton.get_size(), self.createButton)
        }

    def keyReleased(self, key, mod):
        if key == pygame.K_c:
            self.tempName = 'mainMenu'

    def mouseMotion(self, x, y):
        for button in self.buttons:
            self.buttons[button].updateHover(x, y)
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                self.buttonBoard[i][j].updateHover(x, y)

    def mousePressed(self, x, y):
        print(x, y)
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                if self.buttonBoard[i][j].mouseOver(x, y):
                    if self.intBoard[i][j] != self.buttonSelect:
                        self.buttonBoard[i][j].surface = pygame.transform.scale(self.textures[self.buttonSelect], (self.size, self.size))
                        self.intBoard[i][j] = self.buttonSelect
                    else:
                        self.buttonBoard[i][j].surface = pygame.transform.scale(self.textures[0], (self.size, self.size))
                        self.intBoard[i][j] = 0
                    self.buttonBoard[i][j].click(x, y)
                    return
        for button in self.buttons:
            self.buttons[button].clicked = False
            self.buttons[button].click(x, y)
        self.updateButtonSelection()
        if self.buttons['create'].mouseOver(x, y):
            self.exportMap()
            self.tempName = 'campaign'

    def updateButtonSelection(self):
        if self.buttons['player'].clicked:  self.buttonSelect = 1; return
        elif self.buttons['stone'].clicked: self.buttonSelect = 2; return
        elif self.buttons['gate'].clicked:  self.buttonSelect = 3; return
        elif self.buttons['goo'].clicked:   self.buttonSelect = 4; return
        elif self.buttons['easy'].clicked:  self.buttonSelect = 5; return
        elif self.buttons['hard'].clicked:  self.buttonSelect = 6; return
        elif self.buttons['ammo'].clicked:  self.buttonSelect = 7; return
        elif self.buttons['exit'].clicked:  self.buttonSelect = 8; return

    def exportMap(self):
        mapString = ''
        for i in range(self.boardRows):
            for j in range(self.boardCols):
                value = self.intBoard[i][j]
                if value == 1:
                    playerPos = f"{i},{j}\n"
                    value -= 1
                elif value > 0:
                    value -= 1
                mapString += str(value)
            mapString += '\n'
        mapString = playerPos + mapString
        # From http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
        with open('Levels/userLevel1.txt', "w+") as f:
            f.write(mapString)
        self.tempName = 'campaign'

    def redrawAll(self, screen):
        screen.fill((145, 238, 255))
        screen.blit(self.titleSurface, (15, 10))
        pygame.draw.rect(screen, pygame.Color(252, 253, 222), (15, 10+self.titleSurface.get_height(), 30+self.titleSurface.get_width(), self.height-25-self.titleSurface.get_height()), 0)
        self.drawOptions(15, 10+self.titleSurface.get_height(), screen)
        self.drawBoard(200, 40, 20, screen)
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
