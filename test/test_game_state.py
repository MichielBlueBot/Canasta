from unittest import TestCase

from base.actions.action_list import ALL_ACTIONS
from base.game import Game


class TestGamePhase(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.initialize_game()

    def test_none_phase(self):
        self.game.phase = None
        validated_actions = [a for a in ALL_ACTIONS if a.validate(player=self.game.players[self.game.current_player],
                                                                  board=self.game.board)]
        self.assertEqual(0, len(validated_actions))

    def test_initial_phase(self):
        validated_actions = [a for a in ALL_ACTIONS if a.validate(player=self.game.players[self.game.current_player],
                                                                  board=self.game.board)]
        self.assertEqual(2, len(validated_actions))  # initial possible actions are TakeCardAction and TakeStackAction
