from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
from stack import Stack

class Graph():
    def __init__(self, player):
        self.player = player
        self.traversed = Stack()
        self.directions = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }
        self.rooms = {}
        self.path = []

    def dft(self):
        self.rooms[self.player.current_room.id] = {}
        exits = self.player.current_room.get_exits()
        
        for direction in exits:
            self.rooms[self.player.current_room.id][direction] = '?'


        while True:
            not_visited = []

            for room in self.rooms[self.player.current_room.id]:
                if self.rooms[self.player.current_room.id] == '?':
                    not_visited.append(room)

            if len(not_visited):
                new_direction = not_visited.pop()
                self.traversed.push(self.directions[new_direction])
                self.rooms[self.player.current_room.id][new_direction] = True
                self.player.travel(new_direction)
                self.path.append(new_direction)

                if self.player.current_room.id not in self.rooms:
                    self.rooms[self.player.current_room.id] = {}
            
                    for direction in exits:
                        self.rooms[self.player.current_room.id][direction] = '?'
                    self.rooms[self.player.current_room.id][self.directions[new_direction]] = True

            else:
                if self.traversed.size():
                    direction = self.traversed.pop()
                    self.player.travel(direction)
                    self.path.append(direction)
                else:
                    return self.path



player = Player(world.starting_room)
graph = Graph(player)
traversal_path = graph.dft()



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
