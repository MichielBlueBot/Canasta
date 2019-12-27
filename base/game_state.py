from typing import List

from base.board import Board
from base.cards.card_encoder import CardEncoder
from base.cards.card_series_encoder import CardSeriesEncoder
from base.enums.team_color import TeamColor
from base.player import Player


class GameState:
    """
    The full current state of the game.
    The game state contains all necessary information for a player to determine the next action.
    """

    def __init__(self, board: Board, players: List[Player]):
        self.board = board
        self.players = players

    def create_numeral_representation(self, player: Player) -> List[int]:
        """
        Create a numerical representation of (a subset of) the game state for the specified player.

        This representation only contains information that is accessible to the specified player.
        """
        representation = []
        representation.extend(self._own_player_index_representation(player=player))
        representation.extend(self._player_hand_representation(player=player))
        representation.extend(self._top_stack_card_representation())
        representation.extend(self._team_piles_taken_representation())
        representation.extend(self._player_piles_taken_representation())
        representation.extend(self._players_num_cards_representation())
        representation.extend(self._own_team_series_representation(player=player))
        representation.extend(self._other_team_series_representation(player=player))
        representation.extend(self._deck_num_cards_representation())
        return representation

    @staticmethod
    def _own_player_index_representation(player: Player):
        return [player.identifier]

    @staticmethod
    def _player_hand_representation(player: Player):
        return list(CardEncoder().encode(player.hand.get_raw_cards()))

    def _top_stack_card_representation(self):
        return list(CardEncoder().encode(self.board.stack.look()))

    def _team_piles_taken_representation(self):
        red_grabbed_pile = False
        blue_grabbed_pile = False
        for player in self.players:
            if player.has_grabbed_pile():
                if player.team_color == TeamColor.RED:
                    red_grabbed_pile = True
                else:
                    blue_grabbed_pile = True
        return [int(red_grabbed_pile), int(blue_grabbed_pile)]

    def _player_piles_taken_representation(self):
        representation = []
        for player in self.players:
            if player.has_grabbed_pile():
                representation.append(1)
            else:
                representation.append(0)
        return representation

    def _players_num_cards_representation(self):
        return [player.num_cards() for player in self.players]

    def _own_team_series_representation(self, player: Player):
        return list(CardSeriesEncoder().encode(self.board.get_series_for_player(player)))

    def _other_team_series_representation(self, player: Player):
        for other_player in self.players:
            if other_player.team_color != player.team_color:
                return list(CardSeriesEncoder().encode(self.board.get_series_for_player(other_player)))

    def _deck_num_cards_representation(self):
        return [self.board.deck.num_cards()]
