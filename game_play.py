class item:
    object_relations = []
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def examine(self, game_state):
        if self in game_state['current_room'].object_relations:
            return True    



class furniture(item):
    def __init__(self, name, type):
        super().__init__(name, type = 'furniture')
    def hidden_items(self, key=[]):
        self.object_relations = [key]
    def examine(self, game_state):
        output = str()
        if super().examine(game_state):
            output = f'You examined {self.name} '
            if len(self.object_relations) > 0:
                found_key= self.object_relations.pop()
                output += f'and found {found_key.name}'
                game_state['keys_collected'].append(found_key)
            else:
                output += 'and found nothing interesting.'
        else:
            print("This item is not in the room")
        print(output)
        return game_state


        

class door(item):
    def __init__(self, name, type):
        super().__init__(name, type = 'door')

    def connected_rooms(self, rooms):
        self.object_relations = [i for i in rooms]

    def examine(self, game_state):
        if super().examine(game_state):
            output = f'You examined {self.name} '
            have_key = False
            for collected_key in game_state["keys_collected"]:
                if(collected_key.targeted_door.name == self.name):
                    have_key = True
            if(have_key):
                output += "and you unlocked it with a key you have."
                game_state = self.get_to_the_next_room(game_state)
            else:
                 output += "and it is locked and you don't have the key."
        else:
            print("This item is not in the room")   
        
        print(output)
        return game_state 
    
    def get_to_the_next_room(self, game_state):
         next_room = [room for room in self.object_relations if room != game_state['current_room']]
         proceed = input(f'you can enter {next_room[0].name}. Do you want to proceed?(yes/no) ')
         if proceed.lower() == 'yes':
            print(f'Now you are in the {next_room[0].name}')
            game_state["current_room"] = next_room[0]
         return game_state



class key(item):
    def __init__(self, name, type, target):
        super().__init__(name, type = 'key')
        self.targeted_door = target
        self.object_relations =  target


class room(item):
    def __init__(self, name, type):
        super().__init__(name, type = 'room')
    def items_inside(self, item):
        self.object_relations = [i for i in item] 
    def explore(self):
         #items = [item["name"] for item in self.object_relations[room["name"]]]
        print(f"You explored the {self.name}. You've found {', '.join(thing.name for thing in self.object_relations)}")

       
outside = room('ouside', 'room')
living_room = room('living room', 'room')
game_room = room('game room', 'room')
bedroom_1 = room('bedroom 1', 'room')
bedroom_2 = room('bedroom 2', 'room')

dining_table = furniture('dining table', 'furniture')
couch = furniture('couch', 'furniture')
piano = furniture('piano', 'furniture')
queen_bed = furniture('queen bed', 'furniture')
double_bed = furniture('double bed', 'furniture')
dresser = furniture('dresser', 'furniture')

door_a = door('door a', 'door')
door_b = door('door b', 'door')
door_c = door('door c', 'door')
door_d = door('door d', 'door')

key_a = key('key a', 'key', door_a)
key_b = key('key b', 'key', door_b)
key_c = key('key c', 'key', door_c)
key_d = key('key d', 'key', door_d)

living_room.items_inside([dining_table, door_d])
game_room.items_inside([couch, piano, door_a])
bedroom_1.items_inside([queen_bed, door_a, door_b, door_c])
bedroom_2.items_inside([double_bed, dresser, door_b])

piano.hidden_items(key_a)
queen_bed.hidden_items(key_b)
double_bed.hidden_items(key_c)
dresser.hidden_items(key_d)

door_a.connected_rooms([game_room, bedroom_1])
door_b.connected_rooms([bedroom_1, bedroom_2])
door_c.connected_rooms([bedroom_1, living_room])
door_d.connected_rooms([living_room, outside])



INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
    }

def start_game(game_state):
    print("You wake up on a couch and find yourself in a strange house with no windows\nwhich you have never been to before. You don't remember why you are here and\nwhat had happened before. You feel some unknown danger is approaching\nand you must get out of the house, NOW!")
    play_room(game_state["current_room"])


def play_room(room):

    global game_state
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room.name)
        intended_action = input("What would you like to do?'explore' or 'examine'?").strip()
        if intended_action.lower() == "explore":
            room.explore()
            play_room(room)
        elif intended_action.lower() == "examine": 
            examine_item = input('what would you like to examine?')
            examine_obj = [obj for obj in game_state['current_room'].object_relations if obj.name == examine_item]
            try:
                game_state = examine_obj[0].examine(game_state)
            except:
                print("Not sure what you mean. try again.\n 'explore' or 'examine'.")
            play_room(game_state["current_room"])
        else:
            print("Not sure what you mean. try again.\n 'explore' or 'examine'.")
            play_room(room)
        #linebreak()
game_state = INIT_GAME_STATE.copy()
start_game(game_state)