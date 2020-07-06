import pygame
import constants as c


class Scoreboard:

    def __init__(self):
        self.width = 400
        self.height = 400
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.font = pygame.font.Font('freesansbold.ttf', 16)

    def draw(self, screen, sprites_dict, scoreboard_data):
        """ Method to draw the socreboard on a surface

        Args:
            screen (surface): The surface to draw the scoreboard on
            sprites_dict (dict): Dictionary conatining player and projectiles info
            scoreboard_data (dict): dictionary contaning kill and death info
        """ 
               
        pygame.draw.rect(self.surface, (0, 0, 0, 127), (0, 0, self.width, self.height))
        pygame.draw.rect(self.surface, (168, 111, 50, 255), (0, 0, self.width, self.height), 1)
        text = self.font.render("Name", True, c.WHITE)
        self.surface.blit(text, (10, 10))
        text = self.font.render("Kills", True, c.WHITE)
        self.surface.blit(text, (240, 10))
        text = self.font.render("Deaths", True, c.WHITE)
        self.surface.blit(text, (300, 10))
        pygame.draw.line(self.surface, (168, 111, 50, 255), (10, 34), (self.width - 10, 34), 1)
        x, y = 10, 50
        for key, sprites_list in sprites_dict.items():
            for sprite in sprites_list:
                if sprite.is_player:
                    text = self.font.render("{}".format(sprite.name), True, c.WHITE)
                    self.surface.blit(text, (x, y))
                    text = self.font.render("{}".format(scoreboard_data[key][0]), True, c.WHITE)
                    self.surface.blit(text, (x + 240, y))
                    text = self.font.render("{}".format(scoreboard_data[key][1]), True, c.WHITE)
                    self.surface.blit(text, (x + 300, y))
                    y += 30
        screen.blit(self.surface, (c.SCREEN_WIDTH//2 - self.width//2, 100))
