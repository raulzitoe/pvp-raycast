import socket
import threading
import pickle
import time
import random
import constants as c
from sprite import Sprite
from collections import defaultdict

def spawn_random():
    x = random.randint(0, c.MAP_WIDTH-1) + 0.5
    y = random.randint(0, c.MAP_HEIGHT-1) + 0.5
    while c.game_map[int(x)][int(y)] != 0:
        x = random.randint(0, c.MAP_WIDTH-1) + 0.5
        y = random.randint(0, c.MAP_HEIGHT-1) + 0.5
    return x, y

def calculate_distance(a, b):
        return ((a.x - b.x)**2 + (a.y - b.y)**2)**(0.5)

def check_death(my_id, dict_sprites):
    my_sprite = None
    for player_id, sprites_list in dict_sprites.items():
        if int(player_id) == my_id:
            for sprite in sprites_list:
                if sprite.is_player:
                    my_sprite = sprite
    
    for player_id, sprites_list in dict_sprites.items():
        if int(player_id) != my_id:
            for sprite in sprites_list:
                if not sprite.is_player:
                    if calculate_distance(my_sprite, sprite) < 0.4:
                        #print("Death distance: {}".format(calculate_distance(my_sprite, sprite)))
                        return player_id
    return False

def threaded_client(conn, _id):
    global sprites_dict, connections, message

    current_id = _id

    # Receive player name from client
    data = conn.recv(16)
    name = data.decode("utf-8")
    print("[SERVER]", name, "connected to the server.")

    # Send id to client and create a new player instance with that id
    conn.send(str.encode(str(current_id)))
    sprites_dict[current_id].append(Sprite(1, 1, 1, 1, None, 0, True, 2, 1, 0, name))
    message[current_id] = ""
    scoreboard[current_id] = [0, 0]
    for key in message.keys():
        message[key] = "{} connected to the server".format(name).upper()

    # Main loop for in/outbound data handling
    while True:
        for player_id, sprites in sprites_dict.items():
            for sprite in sprites:
                sprite.move()
                if c.game_map[int(sprite.x)][int(sprite.y)] and not sprite.is_player:
                    sprites_dict[player_id].remove(sprite)

        # If player got killed, change death info to new spawn point
        death_info = [0, 0]
        killer = check_death(current_id, sprites_dict)
        if killer:
            death_info = spawn_random()
            for player_id, sprites in sprites_dict.items():
                for sprite in sprites:
                    if sprite.is_player and player_id == killer:
                        name1 = sprite.name
                        scoreboard[int(player_id)][0] += 1
                    if sprite.is_player and int(player_id) == current_id:
                        name2 = sprite.name
                        scoreboard[int(player_id)][1] += 1
            for key in message.keys():
                message[key] = "{} killed {}".format(name1, name2).upper()

        try:    
            # Keep sending position data to client
            send_data = pickle.dumps((sprites_dict, death_info, message[current_id], scoreboard))
            message[current_id] = ""
            conn.send(send_data)
            
        except Exception as e:
            print(e)
        
        try:
            # Receive data from client
            data = conn.recv(2048)
            if not data:
                break
            x, y, projectile_data = pickle.loads(data)

            # Update player position
            if data:
                for player_id, sprites in sprites_dict.items():
                    if int(player_id) == current_id:
                        for sprite in sprites:
                            if sprite.is_player:
                                sprite.x = x
                                sprite.y = y
                if projectile_data:
                    sprites_dict[current_id].append(projectile_data)
        except Exception as e:
            break  # if an exception has been reached disconnect client       
        time.sleep(0.001)

    # When user disconnects	
    print("[SERVER] Name:", name, ", Client Id:", current_id, "disconnected")
    for key in message.keys():
        message[key] = "{} disconnected".format(name).upper()
    connections -= 1 
    del sprites_dict[current_id]  # remove client information from players list
    conn.close()  # close connection

# Setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 5000

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

# Try to connect to server
try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen()  # Listen for connections

print("[SERVER] Server Started with local ip {} on port {}".format(SERVER_IP, PORT))

# Dynamic variables
sprites_dict = defaultdict(list)
connections = 0
_id = 1
threads = []
message = {}
scoreboard = {}

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