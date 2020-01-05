import logging
from numbers import Number
from typing import TYPE_CHECKING

from base.actions.action import Action
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class TakeStackAction(Action):
    """ Take the stack and add the cards to the players hand. """

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return None

    def get_reward(self) -> Number:
        return 1  # Basic reward for not discouraging taking the stack

    def validate(self, player: 'Player', board: 'Board', verbose: bool = False):
        if board.phase != GamePhase.DRAW_PHASE:
            if verbose:
                logging.info("Invalid action {}. Reason: wrong phase - {}".format(self, board.phase))
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        stack_cards = board.stack.grab()
        player.hand.add(stack_cards)

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        return GamePhase.ACTION_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}TakeStack".format(execution_tag)
