from typing import TYPE_CHECKING

from base.actions.action import Action
from base.card import Card
from base.cards.card_series import CardSeries
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class AddBackAction(Action):

    def __init__(self, card: Card, series: CardSeries):
        self.card = card
        self.series = series

    def __key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return self.card, self.series

    def validate(self, player: 'Player', board: 'Board'):
        # Check the board phase
        if board.phase not in [GamePhase.ACTION_PHASE, GamePhase.PLAY_JOKER_PHASE]:
            return False
        # Make sure we add a joker if we're in play joker phase
        if board.phase == GamePhase.PLAY_JOKER_PHASE:
            if not self.card.is_joker():
                return False
        # Check if player is going to clear its hand and whether its allowed to do so
        if player.num_cards() <= 2 and not board.player_may_clear_hand(player):
            return False
        # Make sure the player is adding to its own teams series
        team_series = board.get_series_for_player(player)
        if self.series not in team_series:
            return False
        # Make sure the player has the card it wants to add in its hand
        if self.card not in player.hand:
            return False
        # Make sure the card is addable to the series
        add_back_options = self.series.get_add_back_options()
        if self.card not in add_back_options:
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        self.series.add_back(self.card)

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        if player.hand.is_empty():
            return GamePhase.NO_CARDS_PHASE
        return GamePhase.ACTION_PHASE

    def __str__(self):
        return "AddBack {}  <<<  {}".format(self.series, self.card)
