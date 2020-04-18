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
traversal_path = []

"""
 
- Add room visited (map dictionary)
- Get exits for the room.
- Navigate towards one direction, then add to traversal path
- then remove directions linked to the room
- Find opposite direction, then add to reverse path for backtracking
- Get exits for next room, track in map dictionary
- Keep moving player, add direction to traversal path and remove from possible directions
- Move til dead-end reached
- backtrack along last direction and add to the traversal path, and check room for unexplored directions
- Repeat til number of rooms visited matches length of the rooms graph

"""

visited = {}  # track visited rooms in a map dictionary
reverse_path = []  # store reverse navigation for backtracking
reverse_nav = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}  # directions for backtrack navigation


room_id = player.current_room.id
# first room to be visited & its exits - add to visited map dictionary
visited[room_id] = player.current_room.get_exits()


while len(visited) < len(room_graph):  # While visited is less than rooms in graph
    if player.current_room.id not in visited:  # if not visited
        # add to visited & get exits
        visited[player.current_room.id] = player.current_room.get_exits()

        # once room is visited, remove from unexplored paths since player came from that direction
        previous_direction = reverse_path[-1]
        visited[player.current_room.id].remove(previous_direction)

    if len(visited[player.current_room.id]) is 0:  # when all rooms have been explored
        # backtrack to prev room til unexplored room is found
        # get prev direction from reverse_path (last added direction)
        previous_direction = reverse_path[-1]
        reverse_path.pop()  # remove from reverse_path
        # add the previous direction to the traversal_path
        traversal_path.append(previous_direction)
        # move the player in that direction
        player.travel(previous_direction)

    else:  # if directions left unexplored
        # get 1st available direction in the room
        direction = visited[player.current_room.id][-1]
        visited[player.current_room.id].pop()  # remove from visited
        # add direction to traversal_path
        traversal_path.append(direction)
        # add opposite direction to reverse_path
        reverse_path.append(reverse_nav[direction])
        # move player to explore new room
        player.travel(direction)


# TRAVERSAL TEST - DO NOT MODIFY
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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
