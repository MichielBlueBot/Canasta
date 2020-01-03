from typing import TYPE_CHECKING

from base.actions.action import Action
from base.actions.series_interaction_action import SeriesInteractionAction
from base.card import Card
from base.cards.card_series import CardSeries
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class AddFrontAction(SeriesInteractionAction):

    def __init__(self, card: Card, series: CardSeries):
        super().__init__(series)
        self.card = card

    def _key(self):
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
        if player.num_cards() <= 2 and not board.player_may_clear_hand(player, self):
            return False
        # Make sure the player is adding to its own teams series
        team_series = board.get_series_for_player(player)
        if self.series not in team_series:
            return False
        # Make sure the player has the card it wants to add in its hand
        if self.card not in player.hand:
            return False
        # Make sure the card is addable to the series
        add_front_options = self.series.get_add_front_options()
        if self.card not in add_front_options:
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        pre_execution_value = self.series.get_total_value()
        player.hand.pop(self.card)
        # Make sure to add the card to the series on the board (not self.series!)
        for series in board.get_series_for_player(player):
            if series == self.series:
                series.add_front(self.card)
                break
        self.score_value = self.series.get_total_value() - pre_execution_value

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        if player.hand.is_empty():
            return GamePhase.NO_CARDS_PHASE
        return GamePhase.ACTION_PHASE

    def will_create_pure(self, player: 'Player', board: 'Board') -> bool:
        """Return True if executing this action will create a pure canasta for the player."""
        if self.series.length == 6 and not self.card.is_joker_like():
            return True
        return False

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}AddFront {}  >>>  {}".format(execution_tag, self.card, self.series)
