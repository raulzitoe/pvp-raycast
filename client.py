import pygame
from game import Game
import constants as c
import socket
import time
import pickle
from sprite import Sprite
import threading
import sys


def network_data_handle():
    """ The method handles the in/out data when playing over a network or internet

        It is used as a thread to decouple the pygame loop from the data handling 
        so the conection won't affect the fps of the game
    """    
    global client, game
    while not game.done:
        try:
            data = client.recv(2048)
            print(sys.getsizeof(data))
            sprites_dict_data, death_info, message, scoreboard_data = pickle.loads(data)
            if message:
                game.message = message
            
            for key, sprites in sprites_dict_data.items():
                for sprite in sprites:
                    if sprite.is_player:
                        sprite.image = game.player_image
                    else:
                        sprite.image = game.projectile_image
            if death_info[0] and death_info[1]:
                game.posX, game.posY = death_info
            game.sprites = sprites_dict_data.copy()
            game.scoreboard_data = scoreboard_data.copy()

        except Exception as e:
            print(e)
        try:
            projectile_data = 0
            if game.shoot:
                game.shoot = False
                projectile_data = Sprite(game.posX, game.posY, game.dirX, game.dirY, 0, 0.2)
            send_data = pickle.dumps((game.posX, game.posY, projectile_data))
            client.send(send_data)
        except Exception as e:
            print(e)
        time.sleep(0.001)
    client.close()

pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
clock = pygame.time.Clock()
game = Game()

# Hide mouse pointer and set grab as True
# This enables pygame relative virtual mouse movement used on mouse input camera movement
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Read txt config file to check if game is local or over network/internet
f = open("ip_port_to_connect.txt", "r")
CONDITION, PLAYER_NAME, IP, PORT = f.read().splitlines()
print("1: {} 2: {} 3: {} 4: {}".format(CONDITION, PLAYER_NAME, IP, PORT))
if CONDITION == "YES" or CONDITION == "Yes" or CONDITION == "yes":
    game.is_connected = True
print("Connected? {}".format(game.is_connected))
PORT = int(PORT)
f.close()

# Case connected, create conection with server, send name and receive client ID 
if game.is_connected:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (IP, PORT)
    client.connect(addr)
    client.send(str.encode(PLAYER_NAME))
    val = client.recv(8)
    print("Received id: {}".format(val.decode()))
    game.my_id = int(val)
    t = threading.Thread(target=network_data_handle)
    t.start()

# Main loop
while not game.done:
    events = pygame.event.get()
    game.draw(screen)
    game.input_handle()
    pygame.display.flip()
    clock.tick()
pygame.quit()