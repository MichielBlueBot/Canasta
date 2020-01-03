from abc import ABCMeta, abstractmethod
from typing import Optional, TYPE_CHECKING

from base.cards.hand import Hand
from base.enums.game_phase import GamePhase
from base.team import Team

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class Player(metaclass=ABCMeta):

    def __init__(self, identifier: int):
        self.hand = None  # type: Optional[Hand]
        self.identifier = identifier
        self.team = None
        self._pile_grabbed = False

    @property
    @abstractmethod
    def is_human(self):
        raise NotImplementedError

    @abstractmethod
    def _choose_action(self, game_state: 'GameState') -> 'Action':
        """
        Return an action to take given the current GameState.

        The chosen action must be an eligible one given the current state, invalid actions will result in an Exception.
        A valid series of actions will always result in a END_TURN_PHASE game phase which ends the players turn.
        """
        raise NotImplementedError

    @property
    def team_color(self):
        return self.team.color

    def set_pile_grabbed(self):
        self.team.set_pile_grabbed()
        self._pile_grabbed = True

    def has_grabbed_pile(self):
        return self._pile_grabbed

    def play(self, game_state: 'GameState', verbose: bool = False):
        """Play a set of moves while it is this players turn based on the given GameState."""
        while game_state.board.phase not in [GamePhase.END_TURN_PHASE, GamePhase.EMPTY_DECK_GAME_END_PHASE]:
            action = self._choose_action(game_state)
            if verbose:
                print("Executing {}".format(action))
            action.execute(self, game_state.board)

    def deal(self, hand: Hand):
        self.hand = hand

    def num_cards(self) -> int:
        return self.hand.num_cards()

    def set_team(self, team: 'Team'):
        self.team = team

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print_str = str(self.identifier) + " " + self.team_color.value + "\n"
        print_str += str(self.hand)
        return print_str
