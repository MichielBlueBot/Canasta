import random
import string
from typing import Optional, Tuple

from base.actions.put_action import PutAction
from base.card import Card
from base.constants import Constants
from base.game import Game
from base.utils.card_constants import HEARTS
from base.utils.singleton import Singleton


class GameRunner(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.running_games = {}

    def start_game(self) -> Tuple[str, Game]:
        game_id = self.generate_new_game_id()
        game = Game()
        game.initialize_game()
        cards = [Card(3, HEARTS), Card(4, HEARTS), Card(5, HEARTS)]
        game.current_player.hand.add(cards)
        PutAction(cards=cards).execute(game.current_player, game.board)
        self.running_games[game_id] = game
        return game_id, game

    def end_game(self, game_id: str) -> None:
        if game_id in self.running_games:
            del self.running_games[game_id]

    def get_game(self, game_id: str) -> Optional[Game]:
        return self.running_games.get(game_id)

    @staticmethod
    def generate_new_game_id() -> str:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(Constants.GAME_ID_LENGTH))
