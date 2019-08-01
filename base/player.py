from random import choice
from typing import Optional, TYPE_CHECKING

from base.actions.action_list import ALL_ACTIONS
from base.actions.discard_card_action import DiscardCardAction
from base.cards.hand import Hand
from base.team import Team

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class Player:

    def __init__(self, identifier: int):
        self.hand = None  # type: Optional[Hand]
        self.identifier = identifier
        self.team = None

    @property
    def team_color(self):
        return self.team.color

    def play(self, game_state: 'GameState'):
        action = None
        while not isinstance(action, DiscardCardAction):
            action = self._choose_action(game_state)
            action.execute(self, game_state.board)

    def _choose_action(self, game_state: 'GameState') -> 'Action':
        action = choice(ALL_ACTIONS)
        #TODO
        return action

    def deal(self, hand: Hand):
        self.hand = hand

    def num_cards(self) -> int:
        return self.hand.num_cards()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print_str = str(self.identifier) + " " + self.team_color + "\n"
        print_str += str(self.hand)
        return print_str

    def set_team(self, team: 'Team'):
        self.team = team
