from numbers import Number
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

    def get_reward(self) -> Number:
        return 1  # Basic reward to not discourage taking cards

    def validate(self, player: 'Player', board: 'Board'):
        # Check the board phase
        return board.phase == GamePhase.DRAW_PHASE

    def _execute(self, player: 'Player', board: 'Board'):
        deck_card = board.deck.deal()
        player.hand.add(deck_card)
        if board.deck.is_empty():
            if board.left_pile_active():
                cards = board.grab_left_pile()
                board.deck.add_cards(cards)
            elif board.right_pile_active():
                # Move the pile to the deck
                cards = board.grab_right_pile()
                board.deck.add_cards(cards)

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        if board.deck.is_empty():
            return GamePhase.EMPTY_DECK_GAME_END_PHASE
        return GamePhase.ACTION_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}TakeCard".format(execution_tag)
