from typing import TYPE_CHECKING

from base.actions.action import Action
from base.card import Card
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class DiscardCardAction(Action):

    def __init__(self, card: Card):
        self.card = card

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return self.card

    def validate(self, player: 'Player', board: 'Board'):
        # Check the board phase
        if board.phase != GamePhase.ACTION_PHASE:
            return False
        # Make sure the player discard a card it currently holds in its hand
        if self.card not in player.hand:
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        card = player.hand.pop(self.card)
        board.stack.put(card)

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        if player.hand.is_empty():
            return GamePhase.NO_CARDS_END_TURN_PHASE
        return GamePhase.END_TURN_PHASE

    def __str__(self):
        return "Discard {}".format(self.card)
