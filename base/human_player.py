from typing import TYPE_CHECKING

from base.actions.action_list import ALL_ACTIONS
from base.player import Player

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class HumanPlayer(Player):

    @property
    def is_human(self):
        return True

    def _choose_action(self, game_state: 'GameState') -> 'Action':
        eligible_actions = [action for action in ALL_ACTIONS if action.validate(player=self, board=game_state.board)]
        for i, action in enumerate(eligible_actions):
            print("{}: {}".format(i, action))
        action_index = None
        while action_index is None:
            try:
                action_index = input("Type the number of the action you wish to execute:")
                action_index = int(action_index)
            except ValueError:
                print("Invalid action number '{}', please enter a number!".format(action_index))
                action_index = None
        return eligible_actions[action_index]
