from random import choice
from typing import TYPE_CHECKING

from base.action_service import ActionService
from base.player import Player

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class AIPlayer(Player):

    @property
    def is_human(self):
        return False

    def _choose_action(self, game_state: 'GameState') -> 'Action':
        eligible_actions = ActionService().get_valid_actions(self, game_state.board)
        for action in eligible_actions:
            print(action)
        action = choice(eligible_actions)
        return action
