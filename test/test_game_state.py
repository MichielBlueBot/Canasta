from unittest import TestCase

from base.actions.action_service import ActionService
from base.game import Game


class TestGamePhase(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.initialize_game()

    def test_none_phase(self):
        self.game.board.phase = None
        validated_actions = ActionService().get_valid_actions(self.game.current_player, self.game.board)
        self.assertEqual(0, len(validated_actions))

    def test_initial_phase(self):
        validated_actions = ActionService().get_valid_actions(self.game.current_player, self.game.board)
        self.assertEqual(2, len(validated_actions))  # initial possible actions are TakeCardAction and TakeStackAction
