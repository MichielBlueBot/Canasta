from typing import TYPE_CHECKING

from base.actions.action import Action
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class TakeCardAction(Action):
    """ Take a card from the deck and add it to the players hand. """

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return None

    def validate(self, player: 'Player', board: 'Board'):
        # Check the board phase
        return board.phase == GamePhase.DRAW_PHASE

    def _execute(self, player: 'Player', board: 'Board'):
        deck_card = board.deck.deal()
        player.hand.add(deck_card)

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        return GamePhase.ACTION_PHASE

    def __str__(self):
        return "TakeCard"
