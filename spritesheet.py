import pygame
import constants as c


class SpriteSheet(object):
    """ Class used to grab images out of a large image or sprite sheet """
 
    def __init__(self, file_name):
        """Constructor

        Args:
            file_name (string): String containing the path to the file
        """

        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
 
    def get_image(self, x, y, width, height):
        """Method to get an image out of a larger one

        Args:
            x (int): X position of the image requested starting from left side
            y (int): Y position of the image requested staring from top side
            width (int): the width of the image requested
            height (int): the height of the image requested

        Returns:
            image: returns an image containing only the part requested
        """        

        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return image
    
    def get_width(self):
        return self.sprite_sheet.get_width()

    def get_height(self):
        return self.sprite_sheet.get_height()