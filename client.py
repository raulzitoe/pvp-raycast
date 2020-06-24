import pygame
from game import Game
import constants as c
import socket
import time
import pickle
from player import Player
from sprites import Sprites
import threading


def network_data_handle():
    global client, game
    while not game.done:
        try:
            data = client.recv(1024)
            players, sprites_data = pickle.loads(data)
            for key, sprites in sprites_data.items():
                for sprite in sprites:
                    sprite.image = game.projectile_image
            game.sprites = sprites_data.copy()
            for player in players.values():
                player.image = game.player_image
            game.players = players.copy()  
        except Exception as e:
            print(e)
        try:
            projectile_data = 0
            if game.shoot:
                game.shoot = False
                projectile_data = Sprites(game.posX, game.posY, game.dirX, game.dirY, 0)
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

f = open("ip_port_to_connect.txt", "r")
CONDITION, PLAYER_NAME, IP, PORT = f.read().splitlines()
print("1: {} 2: {} 3: {} 4: {}".format(CONDITION, PLAYER_NAME, IP, PORT))
if CONDITION == "YES" or CONDITION == "Yes" or CONDITION == "yes":
    game.is_connected = True
print("Connected? {}".format(game.is_connected))
PORT = int(PORT)
f.close()

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