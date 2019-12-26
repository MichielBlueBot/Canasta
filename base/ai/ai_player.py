from random import choice
from typing import TYPE_CHECKING

from base.actions.action_list import ALL_ACTIONS
from base.player import Player

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class AIPlayer(Player):

    @property
    def is_human(self):
        return False

    def _choose_action(self, game_state: 'GameState') -> 'Action':
        eligible_actions = [action for action in ALL_ACTIONS if action.validate(player=self, board=game_state.board)]
        for action in eligible_actions:
            print(action)
        action = choice(eligible_actions)
        return action
