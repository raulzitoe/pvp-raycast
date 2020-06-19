import pygame
from math import sin, cos, degrees, pi, floor
from spritesheet import SpriteSheet
from sprites import Sprites
from minimap import Minimap
import constants as c

worldMap = (
  (8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8),
  (8,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,8),
  (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
  (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,7,7,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,7,7,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,2,0,0,2,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,8),
  (8,7,7,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,7,7,8),
  (8,0,0,0,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,2,0,0,2,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,7,7,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,7,7,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8),
  (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
  (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
  (8,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,8),
  (8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8)
)

posX, posY = 3.0, 10.0 # x and y start position
dirX, dirY = -1.0, 0.0 # initial direction vector
planeX, planeY = 0.0, 0.66 # the 2d raycaster version of camera plane

time = 0 # time of current frame
oldTime = 0 #time of previous frame

textures = []
sprites = []

pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 10)
minimap = Minimap(5)

# Generate some textures
textures.append(SpriteSheet("assets/eagle.png")) #1
textures.append(SpriteSheet("assets/redbrick.png")) #2
textures.append(SpriteSheet("assets/purplestone.png")) #3
textures.append(SpriteSheet("assets/greystone.png")) #4
textures.append(SpriteSheet("assets/bluestone.png")) #5
textures.append(SpriteSheet("assets/mossy.png")) #6
textures.append(SpriteSheet("assets/wood.png")) #7
textures.append(SpriteSheet("assets/colorstone.png")) #8

projectile_image = pygame.image.load("assets/projectile.png").convert_alpha()
floor_img = pygame.image.load("assets/floor.png").convert_alpha()


# Start the main loop
while True:
    events = pygame.event.get()
    pygame.draw.rect(screen, c.BLACK, (0, 0, c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))
    floor_size = floor_img.get_size()
    if floor_size[0] != c.SCREEN_WIDTH or floor_size[1] != c.SCREEN_HEIGHT//2:
        floor_img = pygame.transform.scale(floor_img, (c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))
    screen.blit(floor_img, (0, c.SCREEN_HEIGHT//2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))

    for x in range(0, c.SCREEN_WIDTH):

        # Calculate ray position and direction
        cameraX = 2 * x / c.SCREEN_WIDTH - 1 # x-coordinate in camera space
        rayDirX = dirX + planeX*cameraX
        rayDirY = dirY + planeY*cameraX

        # Which box of the map we're in
        mapX = int(posX)
        mapY = int(posY)

        # Length of ray from current position to next x or y-side
        sideDistX = 0.0
        sideDistY = 0.0

        # Length of ray from one x or y-side to next x or y-side
        if rayDirX == 0:
            rayDirX = 0.001
        if rayDirY == 0:
            rayDirY = 0.001
        
        deltaDistX = abs(1 / rayDirX)
        deltaDistY = abs(1 / rayDirY)
        perpWallDist = 0.0

        # What direction to step in x or y-direction (either +1 or -1)
        stepX = -1
        stepY = -1

        hit = 0 # was there a wall hit?
        side = 0 # was a NS or a EW wall hit?

        # Calculate step and initial sideDist
        if rayDirX < 0:
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * deltaDistX
        if rayDirY < 0:
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * deltaDistY

        # Perform DDA
        while hit == 0:
            # jump to next map square, OR in x-direction, OR in y-direction
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1
            # Check if ray has hit a wall
            if(worldMap[mapX][mapY] > 0): 
                hit = 1

        # Calculate distance of perpendicular ray (Euclidean distance will give fisheye effect!)
        if side == 0:
            perpWallDist = (mapX - posX + (1 - stepX) / 2) / rayDirX
        else:
            perpWallDist = (mapY - posY + (1 - stepY) / 2) / rayDirY

        # Calculate height of line to draw on screen
        lineHeight = int(c.SCREEN_HEIGHT / perpWallDist)

        # Calculate lowest and highest pixel to fill in current stripe
        drawStart = -lineHeight / 2 + c.SCREEN_HEIGHT / 2
        if drawStart < 0:
            drawStart = 0
        drawEnd = lineHeight / 2 + c.SCREEN_HEIGHT / 2
        if drawEnd >= c.SCREEN_HEIGHT:
            drawEnd = c.SCREEN_HEIGHT - 1

        # Texturing calculations
        texNum = worldMap[mapX][mapY] - 1  # 1 subtracted from it so that texture 0 can be used!

        # Calculate value of wallX
        wallX = 0.0 # Where exactly the wall was hit
        if side == 0:
            wallX = posY + perpWallDist * rayDirY
        else:
            wallX = posX + perpWallDist * rayDirX
        wallX -= floor((wallX))

        # X coordinate on the texture
        texX = int(wallX * c.TEX_WIDTH)
        if(side == 0 and rayDirX > 0):
            texX = c.TEX_WIDTH - texX - 1
        if(side == 1 and rayDirY < 0):
            texX = c.TEX_WIDTH - texX - 1

        # TODO: an integer-only bresenham or DDA like algorithm could make the texture coordinate stepping faster
        # How much to increase the texture coordinate per screen pixel
        step = 1.0 * c.TEX_HEIGHT / lineHeight
        # Starting texture coordinate
        texPos = (drawStart - c.SCREEN_HEIGHT / 2 + lineHeight / 2) * step

        image1 = textures[texNum].get_image(int(round(texX)), 0, 1, 64 )
        image2 = pygame.transform.scale(image1, (1, lineHeight))
        darken_percent = (1 - (lineHeight*5/c.SCREEN_HEIGHT))
        dark = pygame.Surface(image2.get_size()).convert_alpha()
        darkness = (darken_percent*255)
        if darkness > 255:
            darkness = 255
        elif darkness < 0:
            darkness = 0
        dark.fill((0, 0, 0, darkness))
        
        screen.blit(image2, ((x * 1), c.SCREEN_HEIGHT // 2 - lineHeight // 2))
        screen.blit(dark, ((x * 1), c.SCREEN_HEIGHT // 2 - lineHeight // 2))

    # SPRITE CASTING
    # TODO: Sort sprites from far to close

    # After sorting the sprites, do the projection and draw them
    for sprite in sprites:
        # Translate sprite position to relative to camera
        spriteX = sprite.x - posX
        spriteY = sprite.y - posY

        # Transform sprite with the inverse camera matrix
        # [ planeX   dirX ] -1                                       [ dirY      -dirX ]
        # [               ]       =  1/(planeX*dirY-dirX*planeY) *   [                 ]
        # [ planeY   dirY ]                                          [ -planeY  planeX ]

        invDet = 1.0 / (planeX * dirY - dirX * planeY) # Required for correct matrix multiplication

        transformX = invDet * (dirY * spriteX - dirX * spriteY)
        transformY = invDet * (-planeY * spriteX + planeX * spriteY) # This is actually the depth inside the screen, that what Z is in 3D, the distance of sprite to player, matching sqrt(spriteDistance[i])

        if transformY == 0:
            transformY = 0.001
        spriteScreenX = int((c.SCREEN_WIDTH / 2) * (1 + transformX / transformY))

      # Parameters for scaling and moving the sprites
        uDiv = 10
        vDiv = 10
        vMove = 60.0
        vMoveScreen = int(vMove / transformY)

        # Calculate height of the sprite on screen
        spriteHeight = abs(int(c.SCREEN_HEIGHT / (transformY))) / vDiv # Using "transformY" instead of the real distance prevents fisheye
        # Calculate lowest and highest pixel to fill in current stripe
        drawStartY = -spriteHeight / 2 + c.SCREEN_HEIGHT / 2 + vMoveScreen
        if drawStartY < 0:
            drawStartY = 0
        drawEndY = spriteHeight / 2 + c.SCREEN_HEIGHT / 2 + vMoveScreen
        if drawEndY >= c.SCREEN_HEIGHT:
            drawEndY = c.SCREEN_HEIGHT - 1

        # Calculate width of the sprite
        spriteWidth = abs( int (c.SCREEN_HEIGHT / (transformY))) / uDiv
        drawStartX = -spriteWidth / 2 + spriteScreenX
        drawEndX = spriteWidth / 2 + spriteScreenX
        if drawEndX >= c.SCREEN_WIDTH:
            drawEndX = c.SCREEN_WIDTH - 1
        if transformY > 0 and drawStartX >= 0 and drawEndX < c.SCREEN_WIDTH:
            tmp_image = pygame.transform.scale(sprite.image, (int(spriteWidth), int(spriteHeight)))
            # Darken sprites that are far from the player
            darken_percent = (1 - (spriteHeight*30/c.SCREEN_HEIGHT))
            dark = pygame.Surface(tmp_image.get_size(), pygame.SRCALPHA).convert_alpha()
            darkness = (darken_percent*255)
            if darkness > 255:
                darkness = 255
            elif darkness < 0:
                darkness = 0
            dark.blit(tmp_image, (0 , 0))
            dark.fill((darkness, darkness, darkness, 0), None, pygame.BLEND_RGBA_SUB)
            screen.blit(dark, (drawStartX , drawStartY))

        sprite.move()
        if worldMap[int(sprite.x)][int(sprite.y)]:
            sprites.remove(sprite)

    # Draw Minimap
    minimap.draw(screen, worldMap, posX, posY, sprites)

    # Timing for input and FPS counter
    oldTime = time
    time = pygame.time.get_ticks()
    frameTime = (time - oldTime) / 1000.0 # Frametime is the time this frame has taken, in seconds
    fps = 1.0 / frameTime
    text = font.render("FPS: {:.2f}".format(fps), True, c.WHITE)
    screen.blit(text, (30, 30))

    # speed modifiers
    moveSpeed = frameTime * 5.0 # The constant value is in squares/second
    rotSpeed = frameTime * 3.0 # The constant value is in radians/second

    key = pygame.key.get_pressed()
    # Move forward if no wall in front of you
    if key[pygame.K_w]:
        if(worldMap[int(posX + dirX * moveSpeed)][int(posY)] == False):
            posX += dirX * moveSpeed
        if(worldMap[int(posX)][int(posY + dirY * moveSpeed)] == False):
            posY += dirY * moveSpeed

    # Move backwards if no wall behind you
    if key[pygame.K_s]:
        if(worldMap[int(posX - dirX * moveSpeed)][int(posY)] == False):
            posX -= dirX * moveSpeed
        if(worldMap[int(posX)][int(posY - dirY * moveSpeed)] == False):
            posY -= dirY * moveSpeed
    
    if key[pygame.K_d]:
        oldDirX = dirX
        dirX = dirX * cos(-pi/2) - dirY * sin(-pi/2)
        dirY = oldDirX * sin(-pi/2) + dirY * cos(-pi/2)
        oldPlaneX = planeX
        planeX = planeX * cos(-pi/2) - planeY * sin(-pi/2)
        planeY = oldPlaneX * sin(-pi/2) + planeY * cos(-pi/2)

        posX += dirX * (moveSpeed/2)
        posY += dirY * (moveSpeed/2)

        oldDirX = dirX
        dirX = dirX * cos(pi/2) - dirY * sin(pi/2)
        dirY = oldDirX * sin(pi/2) + dirY * cos(pi/2)
        oldPlaneX = planeX
        planeX = planeX * cos(pi/2) - planeY * sin(pi/2)
        planeY = oldPlaneX * sin(pi/2) + planeY * cos(pi/2)
    
    if key[pygame.K_a]:
        oldDirX = dirX
        dirX = dirX * cos(-pi/2) - dirY * sin(-pi/2)
        dirY = oldDirX * sin(-pi/2) + dirY * cos(-pi/2)
        oldPlaneX = planeX
        planeX = planeX * cos(-pi/2) - planeY * sin(-pi/2)
        planeY = oldPlaneX * sin(-pi/2) + planeY * cos(-pi/2)

        posX -= dirX * (moveSpeed/2)
        posY -= dirY * (moveSpeed/2)

        oldDirX = dirX
        dirX = dirX * cos(pi/2) - dirY * sin(pi/2)
        dirY = oldDirX * sin(pi/2) + dirY * cos(pi/2)
        oldPlaneX = planeX
        planeX = planeX * cos(pi/2) - planeY * sin(pi/2)
        planeY = oldPlaneX * sin(pi/2) + planeY * cos(pi/2)

    # Rotate to the right
    if key[pygame.K_RIGHT]:
        # Both camera direction and camera plane must be rotated
        oldDirX = dirX
        dirX = dirX * cos(-rotSpeed) - dirY * sin(-rotSpeed)
        dirY = oldDirX * sin(-rotSpeed) + dirY * cos(-rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * cos(-rotSpeed) - planeY * sin(-rotSpeed)
        planeY = oldPlaneX * sin(-rotSpeed) + planeY * cos(-rotSpeed)

    # Rotate to the left
    if key[pygame.K_LEFT]:
        # Both camera direction and camera plane must be rotated
        oldDirX = dirX
        dirX = dirX * cos(rotSpeed) - dirY * sin(rotSpeed)
        dirY = oldDirX * sin(rotSpeed) + dirY * cos(rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * cos(rotSpeed) - planeY * sin(rotSpeed)
        planeY = oldPlaneX * sin(rotSpeed) + planeY * cos(rotSpeed)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if key[pygame.K_SPACE]:
                sprites.append(Sprites(posX, posY, dirX, dirY, projectile_image))
        if event.type == pygame.QUIT:  
            pygame.quit()
    
    if key[pygame.K_ESCAPE]:
        break

    pygame.display.flip()
    clock.tick()

pygame.quit()
