from room import Room
from player import Player
from world import World
import random
from ast import literal_eval

from collections import deque

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
"""
every time you a room is entered you get a list of exits, the coordinates of the room, and the room number
the list of exits tells us the directions we can move in
if we keep a variable as the current room, and the direction we head as the new room, we can add a graph edge connecting the two rooms
ex: curr_room = 0 and has exits [n,s,e], and we move 'e' to new_room, new_room 'w' will be curr_room (0), and curr_room 'e' will be new_room (7)
we know how many total rooms there will be in the test, so that way we can have a set/dictionary logging all of the visited rooms

how to take care of backtracking? backtracking will need to be accounted for in the path list
keep track of how far since a branch, then append the number of rooms traveled in a straight line from that branch back to the branch, but the opposire direction?
use the room coordinates to map a path backwards?
"""
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# set up visited set and start by adding player starting room
visited = set()
visited.add(player.current_room)
# queue for BFS
queue = deque()

# iterate while visited rooms are less than total rooms
while len(visited) < len(room_graph):
    # set current room to the player's room, and use a tuple to append the current room and the path
    # initialize variable for the closest unvisited rooms, and variables for the BFS
    curr_room = player.current_room
    queue.append((curr_room, []))
    closest_unvisited = None
    search_visited = set()
    search_visited.add(curr_room)

    while not closest_unvisited:
        room_path = queue.popleft()
        # add room to the search_visited set
        search_visited.add(room_path[0])
        if room_path[0] not in visited:
            closest_unvisited = room_path
            queue.clear()
        else:
            # get exits for the current room
            exits = room_path[0].get_exits()
            # create list of rooms from the exits found from the get exits function
            rooms = [(room_path[0].get_room_in_direction(exit), exit) for exit in exits]
            # check room list against visited set, and use that list to move
            unvisited = [room for room in rooms if room[0] not in search_visited]
            for room in unvisited:
                # copy room path and append the exits
                new_path = list(room_path[1])
                new_path.append(room[1])
                queue.append((room[0], new_path))
    # add move to the traversal path
    traversal_path.extend(closest_unvisited[1])
    # move the player
    for path in closest_unvisited[1]:
        player.travel(path)
    # add room to visited array
    visited.add(closest_unvisited[0])


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
