import game_play
global game_state
game_state =  {
    "current_room": game_play.game_room,
    "keys_collected": [],
    "target_room": game_play.outside
    }
if __name__ == "__main__":
    
    
    game_play.start_game(game_state)