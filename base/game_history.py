from copy import deepcopy
from typing import Tuple, Optional, TYPE_CHECKING

from base.actions.action import Action

if TYPE_CHECKING:
    from base.game import Game


class GameHistory:
    """Class that represents the full history (actions taken and corresponding game state) of a game."""

    def __init__(self):
        self.history = []

    def add(self, game: 'Game', action: Optional[Action]):
        action = deepcopy(action)
        game = deepcopy(game)
        game.history = None  # avoid recursive reference
        self.history.append((game, action))

    def get(self, i: int) -> Optional[Tuple['Game', Action]]:
        try:
            return self.history[i]
        except IndexError:
            return None

    def get_state_at(self, i: int) -> Optional['Game']:
        try:
            return self.history[i][0]
        except IndexError:
            return None

    def get_last_state(self) -> Optional['Game']:
        return self.get_state_at(-1)

    def get_action_at(self, i: int) -> Optional[Action]:
        try:
            return self.history[i][1]
        except IndexError:
            return None

    def get_last_action(self) -> Optional[Action]:
        return self.get_action_at(-1)

    def clear(self):
        self.history = []
