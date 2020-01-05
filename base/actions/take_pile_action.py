import logging
from numbers import Number
from typing import TYPE_CHECKING

from base.actions.action import Action
from base.constants import Constants
from base.enums.game_phase import GamePhase
from base.enums.pile_side import PileSide

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class TakePileAction(Action):
    """ Take one of the piles on the board. """

    def __init__(self, side: PileSide):
        super().__init__()
        self.side = side

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return self.side

    def get_reward(self) -> Number:
        return Constants.TAKE_PILE_VALUE

    def validate(self, player: 'Player', board: 'Board', verbose: bool = False):
        # Check the board phase
        if board.phase not in [GamePhase.NO_CARDS_PHASE, GamePhase.NO_CARDS_END_TURN_PHASE]:
            if verbose:
                logging.info("Invalid action {}. Reason: wrong phase - {}".format(self, board.phase))
            return False
        # Make sure that player has no cards left
        if player.hand.num_cards() != 0:
            return False
        # Make sure that the players team hasn't taken a pile yet
        if player.team.has_grabbed_pile():
            return False
        # Make sure that the pile is still available
        if self.side == PileSide.LEFT and not board.left_pile_active():
            return False
        if self.side == PileSide.RIGHT and not board.right_pile_active():
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        pile_cards = board.grab_pile(self.side)
        player.hand.add(pile_cards)
        player.set_pile_grabbed()

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        if board.phase == GamePhase.NO_CARDS_END_TURN_PHASE:
            return GamePhase.END_TURN_PHASE
        else:
            return GamePhase.ACTION_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}TakePile {}".format(execution_tag, self.side.value)
