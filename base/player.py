from random import choice
from typing import Optional, TYPE_CHECKING

from base.actions.action_list import ALL_ACTIONS
from base.cards.hand import Hand
from base.enums.game_phase import GamePhase
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
        while not game_state.board.phase == GamePhase.END_TURN_PHASE:
            action = self._choose_action(game_state)
            print("Executing {}".format(action))
            action.execute(self, game_state.board)

    def _choose_action(self, game_state: 'GameState') -> 'Action':
        eligible_actions = [action for action in ALL_ACTIONS if action.validate(player=self, board=game_state.board)]
        for action in eligible_actions:
            print(action)
        action = choice(eligible_actions)
        return action

    def deal(self, hand: Hand):
        self.hand = hand

    def num_cards(self) -> int:
        return self.hand.num_cards()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print_str = str(self.identifier) + " " + self.team_color.value + "\n"
        print_str += str(self.hand)
        return print_str

    def set_team(self, team: 'Team'):
        self.team = team
