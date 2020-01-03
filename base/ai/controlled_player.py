from base.actions.action import Action
from base.game_state import GameState
from base.player import Player


class ControlledPlayer(Player):

    @property
    def is_human(self):
        return False

    def _choose_action(self, game_state: 'GameState') -> 'Action':
        raise NotImplemented("Controlled players need action determination from the outside.")

    def play(self, game_state: 'GameState'):
        raise NotImplemented("Controlled players can only play through the play_action() function.")

    def play_action(self, game_state: 'GameState', action: Action):
        print("Executing {}".format(action))
        action.execute(self, game_state.board)