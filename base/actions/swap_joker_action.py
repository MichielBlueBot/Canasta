from typing import TYPE_CHECKING

from base.actions.action import Action
from base.card import Card
from base.cards.card_series import CardSeries
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class SwapJokerAction(Action):

    def __init__(self, card: Card, series: CardSeries):
        self.card = card
        self.series = series

    def validate(self, player: 'Player', board: 'Board'):
        # Check the board phase
        if board.phase != GamePhase.ACTION_PHASE:
            return False
        # Check if player is going to clear its hand and whether its allowed to do so
        if player.num_cards() <= 2 and not board.player_may_clear_hand(player):
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
        joker = self.series.swap_joker(self.card)
        player.hand.add(joker)

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        return GamePhase.PLAY_JOKER_PHASE
