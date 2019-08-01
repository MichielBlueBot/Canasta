from typing import List

from base.board import Board
from base.player import Player


class GameState:
    """
    The full game state that is visible to each player.
    The game state contains all necessary information for a player to choose the next action,
    and provides access to the board to execute that action.
    """

    def __init__(self, board: Board, players: List[Player]):
        self.board = board
        self.player_num_cards = [player.num_cards() for player in players]
