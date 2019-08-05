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

    def validate(self, player: 'Player', board: 'Board'):
        # Check the board phase
        return board.phase == GamePhase.DRAW_PHASE

    def _execute(self, player: 'Player', board: 'Board'):
        stack_cards = board.stack.grab()
        player.hand.add(stack_cards)

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        return GamePhase.ACTION_PHASE

    def __str__(self):
        return "TakeStack"
