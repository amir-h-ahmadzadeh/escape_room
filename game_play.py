#Living_room:
living_room = {
    "name": "living room",
    "type": "room",
}
Dining_table = {
    "name": "Dining_table",
    "type": "furniture",
}
door_d = {
    "name": "door_d",
    "type": "door",
}

#Game Room
game_room = {
    "name": "game room",
    "type": "room",
}

couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door_a",
    "type": "door",
}

piano = {
    "name": "piano",
    "type": "furniture",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

#Bedroom 1
bedroom1 = {
    "name": "bedroom1",
    "type": "room",
}

queen_bed = {
    "name": "queen_bed",
    "type": "furniture",
}

door_b = {
    "name": "door_b",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

door_c = {
    "name": "door_c",
    "type": "door",
}

#bedroom 2
bedroom2 = {
    "name": "bedroom2",
    "type": "room",
}

double_bed = {
    "name": "double_bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}


outside = {
  "name": "outside"
}

all_rooms = [game_room, bedroom1, bedroom2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]


object_relations = {
    "game room" : [couch, piano, door_a],
    "piano" : [key_a],
    "door_a" : [game_room, bedroom1],
    "bedroom1" : [queen_bed, door_a, door_b, door_c],
    "queen_bed" : [key_b],
    "door_b" : [bedroom1, bedroom2],
    "door_c" : [bedroom1, living_room],
    "bedroom2" : [double_bed, dresser, door_b],
    "double_bed" : [key_c],
    "dresser" : [key_d],
    "living room" : [Dining_table, door_d],
    "door_d" : [living_room, outside],
    "outside" : [door_d],
}
INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
    }
game_state = {}

def start_game(game_state):
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows\nwhich you have never been to before. You don't remember why you are here and\nwhat had happened before. You feel some unknown danger is approaching\nand you must get out of the house, NOW!")
    play_room(game_state["current_room"])


def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do?'explore' or 'examine'?").strip()
        if intended_action.lower() == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action.lower() == "examine":
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. try again.\n 'explore' or 'examine'.")
            play_room(room)
        #linebreak()


def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [item["name"] for item in object_relations[room["name"]]]
    print(f"You explored the {room['name']}. You've found {', '.join(i for i in items)}")

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(current_room != room):
            return room
def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]: # what if instead of an item user ask to examine a room?
        if(item["name"] == item_name):
            output = "You examined " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlocked it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked and you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None): # give a better response based on the non existance or being already examined
        print("The item you requested is not found in the current room.")

    if(next_room and input("Do you want to go to the next room? Ener 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)

