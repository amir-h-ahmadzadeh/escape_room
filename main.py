import game_play

if __name__ == "__main__":
    
    game_play.game_state = game_play.INIT_GAME_STATE.copy()
    game_play.start_game(game_play.game_state)