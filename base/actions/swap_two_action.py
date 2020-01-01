from typing import TYPE_CHECKING

from base.actions.series_interaction_action import SeriesInteractionAction
from base.card import Card
from base.cards.card_series import CardSeries
from base.enums.game_phase import GamePhase
from base.enums.two_swap_direction import TwoSwapDirection

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class SwapTwoAction(SeriesInteractionAction):

    def __init__(self, card: Card, series: CardSeries, direction: TwoSwapDirection):
        super().__init__(series)
        self.card = card
        self.direction = direction

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return self.card, self.series, self.direction

    def validate(self, player: 'Player', board: 'Board'):
        # Check the board phase
        if board.phase != GamePhase.ACTION_PHASE:
            return False
        # Check if player is going to clear its hand and whether its allowed to do so
        if player.num_cards() <= 2 and not board.player_may_clear_hand(player):
            return False
        # Swapping to front is not allowed when there's an ace there
        if self.direction == TwoSwapDirection.FRONT and self.series.get_card(0).get_rank() == 1:
            return False
        # Swapping to back is not allowed when there's an ace there
        if self.direction == TwoSwapDirection.BACK and self.series.get_card(-1).get_rank() == 1:
            return False
        # Make sure the player is swapping a joker from a series its team owns
        team_series = board.get_series_for_player(player)
        if self.series not in team_series:
            return False
        # Make sure the player has the swap card in its hand
        if self.card not in player.hand:
            return False
        # Make sure the swap card is a valid option to swap for the joker
        swap_two_options = self.series.get_swap_two_options()
        if self.card not in swap_two_options:
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        # We keep track of the added value of executing this action to compute the reward
        pre_execution_value = self.series.get_total_value()
        player.hand.pop(self.card)
        # Make sure to swap the two in the series on the board (not self.series!)
        for series in board.get_series_for_player(player):
            if series == self.series:
                series.swap_two(self.card, self.direction)
                break
        self.score_value = self.series.get_total_value() - pre_execution_value

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        if player.hand.is_empty():
            return GamePhase.NO_CARDS_PHASE
        return GamePhase.ACTION_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}SwapTwo ({}) {}  >>>  {}".format(execution_tag, self.direction.value, self.card, self.series)
