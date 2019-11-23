############################
##     Keltin Grimes      ##
## kgrimes@andrew.cmu.edu ##
##                        ##
##     Term Project:      ##
##       Salvation        ##
##           -            ##
##       Main File        ##
############################

import pygame
from Mode import *

class Salvation(object):
    # Initalize the games and game modes
    def __init__(self, width = 960, height = 540, res = 1, fps = 60):
        self.width = width
        self.height = height
        self.resolution = res
        self.fps = fps
        self.title = "Salvation"
        self.textureWidth = self.textureHeight = 64
        # Start pygame
        pygame.init()

    def run(self):
        # pygame setup
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        # store keys being held down
        self._keys = dict()
        # Create Modes
        self.mainMenuMode = MainMenuMode(self.width, self.height,
                                    self.resolution, self.fps,
                                    self.textureWidth, self.textureHeight)
        self.campaignMode = CampaignMode(self.width, self.height,
                                    self.resolution, self.fps,
                                    self.textureWidth, self.textureHeight)
        self.levelEditorMode = LevelEditorMode(self.width, self.height,
                                    self.resolution, self.fps,
                                    self.textureWidth, self.textureHeight)
        self.gameMode = 'campaign'
        # Begin game loop
        playing = True
        while playing:
            self.time = clock.tick(self.fps)    # limit framerate
            print(clock.get_fps())
            screen.fill((0, 0, 0))
            # Check gameMode
            if self.gameMode == 'mainMenu':
                playing = self.mainMenuMode.eventWrapper(pygame.event.get(), self._keys)
                self.mainMenuMode.redrawAll(screen)
                self.gameMode = self.mainMenuMode.checkModeSwitch(self.gameMode)
            elif self.gameMode == 'campaign':
                self.campaignMode.time = self.time
                playing = self.campaignMode.eventWrapper(pygame.event.get(), self._keys)
                self.campaignMode.redrawAll(screen)
                self.gameMode = self.campaignMode.checkModeSwitch(self.gameMode)
            elif self.gameMode == 'levelEditor':
                playing = self.levelEditorMode.eventWrapper(pygame.event.get(), self._keys)
                self.levelEditorMode.redrawAll(screen)
                self.gameMode = self.levelEditorMode.checkModeSwitch(self.gameMode)
            # Render changes to screen
            pygame.display.flip()

        pygame.quit()

if (__name__ == '__main__'):
    Salvation().run()
