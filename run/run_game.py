from base.actions.action_list import ALL_ACTIONS
from base.game import Game

if __name__ == '__main__':
    game = Game()
    game.initialize_game()
    # game.play()
    state = game.get_state()
    print(len(state.create_numeral_representation(game.players[0])))
    print(len(ALL_ACTIONS))
