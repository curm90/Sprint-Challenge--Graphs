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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# . Place to store reversed directions
reverse_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
# . Place to store travesed path
traversal_path = []
# . Place to store backtracked paths
backtracked_path = []
# . Place to store visited rooms
visited = {}

# . Add first room and exits to visited
visited[player.current_room.id] = player.current_room.get_exits()

# . While length of visited is less than length of the room_graph minus 1
while len(visited) < len(room_graph) - 1:
    # . Check if the current room has been visited
    if player.current_room.id not in visited:
        # . Set the last room to the last item in the backtracked path
        last_room = backtracked_path[-1]
        # . If not set the room id in visited to the list of exits
        visited[player.current_room.id] = player.current_room.get_exits()
        # . And remove the last room from the visited dictionary
        visited[player.current_room.id].remove(last_room)
    # . While there are no more room to traverse (Dead end)
    while len(visited[player.current_room.id]) < 1:
        # . Remove the last direction from the backtracked path
        prev_path = backtracked_path.pop()
        # . Move the player back in that direction
        traversal_path.append(prev_path)
        # . Check if there are unexplored rooms
        player.travel(prev_path)
        # . Append the last direction to the traversal path
    else:
        # . Set the last exit to last exit in the current room
        prev_exit = visited[player.current_room.id].pop()
        # . Append the backtracked reverse direction to backtracked path
        backtracked_path.append(reverse_directions[prev_exit])
        # . Append the exit to the traversal path
        traversal_path.append(prev_exit)
        # . Move to the next room
        player.travel(prev_exit)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
