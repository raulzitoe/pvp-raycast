import pygame
import constants as c

class Minimap:

    def __init__(self, square_size):
        self.square_size = square_size
        self.surface = pygame.Surface((self.square_size*c.MAP_WIDTH, self.square_size*c.MAP_HEIGHT)).convert()
        self.x = c.SCREEN_WIDTH - self.square_size*c.MAP_WIDTH
        self.y = 0
    
    def draw(self, destination, world_map, player_x, player_y, sprites):
        self.surface.fill(c.GRAY)
        for i, row in enumerate(world_map):
            for j, elem in enumerate(row):
                if elem:
                    pygame.draw.rect(self.surface, c.BLACK, (j*self.square_size, i*self.square_size, self.square_size, self.square_size))
        # Draw Player
        dot_x = (player_x / c.MAP_WIDTH) * self.square_size*c.MAP_WIDTH
        dot_y = (player_y / c.MAP_HEIGHT) * self.square_size*c.MAP_HEIGHT
        pygame.draw.circle(self.surface, c.BLUE, (int(dot_y), int(dot_x)), self.square_size//2)
        # Draw Sprites
        for sprite in sprites:
            dot_x = (sprite.x / c.MAP_WIDTH) * self.square_size*c.MAP_WIDTH
            dot_y = (sprite.y / c.MAP_HEIGHT) * self.square_size*c.MAP_HEIGHT
            pygame.draw.circle(self.surface, c.RED, (int(dot_y), int(dot_x)), self.square_size//2)
        destination.blit(self.surface, (self.x, self.y))
