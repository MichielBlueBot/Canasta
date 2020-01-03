from typing import TYPE_CHECKING

from base.actions.series_interaction_action import SeriesInteractionAction
from base.card import Card
from base.cards.card_series import CardSeries
from base.constants import Constants
from base.enums.game_phase import GamePhase
from base.utils.card_constants import JOKER_SUIT, JOKER_RANK

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class SwapJokerAction(SeriesInteractionAction):

    def __init__(self, card: Card, series: CardSeries):
        super().__init__(series)
        self.card = card

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return self.card, self.series

    def validate(self, player: 'Player', board: 'Board'):
        # Check the board phase
        if board.phase != GamePhase.ACTION_PHASE:
            return False
        # Check if player is going to clear its hand and whether its allowed to do so
        if player.num_cards() <= 2 and not board.player_may_clear_hand(player, self):
            return False
        # Make sure the player is swapping a joker from a series its team owns
        team_series = board.get_series_for_player(player)
        if self.series not in team_series:
            return False
        # Make sure the player has the swap card in its hand
        if self.card not in player.hand:
            return False
        # Make sure the swap card is a valid option to swap for the joker
        swap_joker_options = self.series.get_swap_joker_options()
        if self.card not in swap_joker_options:
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        pre_execution_value = self.series.get_total_value()
        player.hand.pop(self.card)
        # Make sure to swap the joker in the series on the board (not self.series!)
        for series in board.get_series_for_player(player):
            if series == self.series:
                joker = series.swap_joker(self.card)
                player.hand.add(joker)
                break
        self.score_value = self.series.get_total_value() - pre_execution_value + Constants.JOKER_SWAP_EXTRA_SCORE

    def will_create_pure(self, player: 'Player', board: 'Board') -> bool:
        """
        Return True if executing this action will create a pure canasta for the player.

        For this specific action, a pure is created if swapping the joker in the series creates a pure,
        AND the swapped joker can be added elsewhere on the board (hence not destroying the pure).
        """
        def _player_can_play_joker_elsewhere():
            """Return True if the player has any option on the board to add a joker, besides this actions series."""
            for series in board.get_series_for_player(player):
                all_add_card_action_options = series.get_add_back_options() + series.get_add_front_options()
                if series != self.series and Card(JOKER_RANK, JOKER_SUIT) in all_add_card_action_options:
                    return True
            return False

        if self.series.length >= 7 and _player_can_play_joker_elsewhere():
            return True
        return False

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        return GamePhase.PLAY_JOKER_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}SwapJoker {}  >>>  {}".format(execution_tag, self.card, self.series)
