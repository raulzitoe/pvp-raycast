import socket
import threading
import pickle
import time
import random
import constants as c
from player import Player
from sprites import Sprites
from collections import defaultdict

def spawn_random():
    x = random.randint(0, c.MAP_WIDTH-1)
    y = random.randint(0, c.MAP_HEIGHT-1)
    while c.game_map[y][x] != 0:
        x = random.randint(0, c.MAP_WIDTH-1)
        y = random.randint(0, c.MAP_HEIGHT-1)
    return x + 0.5, y + 0.5

def threaded_client(conn, _id):
    global players, sprites_dict, connections

    current_id = _id

    # Recieve player name from client
    data = conn.recv(16)
    name = data.decode("utf-8")
    print("[SERVER]", name, "connected to the server.")

    # Send id to client and create a new player instance with that id
    conn.send(str.encode(str(current_id)))
    players[current_id] = Player()

    # Main loop for in/outbound data handling
    while True:
        for key, sprites in sprites_dict.items():
            for sprite in sprites:
                sprite.move()
                if c.game_map[int(sprite.x)][int(sprite.y)]:
                    sprites_dict[key].remove(sprite)

        try:    
            # Keep sending position data to client
            send_data = pickle.dumps((players, sprites_dict))
            conn.send(send_data)
        except Exception as e:
            print(e)

        try:
            # Receive data from client
            data = conn.recv(1024)
            if not data:
                break
            x, y, projectile_data = pickle.loads(data)

            # Update player position
            if data:
                players[current_id].x = x
                players[current_id].y = y
                if projectile_data:
                    sprites_dict[current_id].append(projectile_data)
        except Exception as e:
            break  # if an exception has been reached disconnect client       
        time.sleep(0.001)

    # When user disconnects	
    print("[SERVER] Name:", name, ", Client Id:", current_id, "disconnected")
    connections -= 1 
    del players[current_id]  # remove client information from players list
    conn.close()  # close connection



# Setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 5000

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

# try to connect to server
try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen()  # Listen for connections

print("[SERVER] Server Started with local ip {} on port {}".format(SERVER_IP, PORT))

# Dynamic variables
players = {}
sprites_dict = defaultdict(list)
connections = 0
_id = 0
threads = []

print("[SERVER] Waiting for connections")

# Keep looping to accept new connections
while True:
    host, addr = S.accept()
    print("[SERVER] Connected to: {}".format(addr))
    connections += 1
    # Create new thread with individual id
    t = threading.Thread(target=threaded_client,args=(host,_id))
    t.start()
    _id += 1

print("[SERVER] Server offline")




