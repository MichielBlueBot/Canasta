from unittest import TestCase

from base.action_service import ActionService
from base.actions.add_back_action import AddBackAction
from base.actions.discard_card_action import DiscardCardAction
from base.actions.put_action import PutAction
from base.actions.swap_joker_action import SwapJokerAction
from base.actions.take_card_action import TakeCardAction
from base.actions.take_pile_action import TakePileAction
from base.card import Card
from base.enums.game_phase import GamePhase
from base.enums.pile_side import PileSide
from base.game import Game
from base.utils.card_constants import JOKER_SUIT, JOKER_RANK, HEARTS, CLUBS


class TestGamePhase(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.initialize_game()
        self.board = self.game.board  # quick access

    def test_none_phase_simple(self):
        self.board.phase = None
        validated_actions = ActionService().get_valid_actions(self.game.current_player, self.board)
        self.assertEqual(0, len(validated_actions))

    def test_initial_phase_simple(self):
        self.assertEqual(self.board.phase, GamePhase.DRAW_PHASE)
        validated_actions = ActionService().get_valid_actions(self.game.current_player, self.board)
        self.assertEqual(2, len(validated_actions))  # initial possible actions are TakeCardAction and TakeStackAction

    def test_action_phase_simple(self):
        self.assertEqual(self.board.phase, GamePhase.DRAW_PHASE)
        TakeCardAction().execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.ACTION_PHASE)

    def test_play_joker_phase_simple(self):
        self.assertEqual(self.board.phase, GamePhase.DRAW_PHASE)
        TakeCardAction().execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.ACTION_PHASE)
        # Give the player a card to swap the joker with
        swap_card = Card(4, HEARTS)
        series_cards = [Card(3, HEARTS), Card(JOKER_RANK, JOKER_SUIT), Card(5, HEARTS)]
        self.game.current_player.hand.add(series_cards)
        self.game.current_player.hand.add(swap_card)
        # Play a series with a joker
        PutAction(series_cards).execute(self.game.current_player, self.board)
        series = self.board.get_series_for_player(self.game.current_player)[0]
        self.assertEqual(self.board.phase, GamePhase.ACTION_PHASE)
        # Swap the joker
        SwapJokerAction(swap_card, series).execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.PLAY_JOKER_PHASE)
        # Play the joker back
        AddBackAction(Card(JOKER_RANK, JOKER_SUIT), series).execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.ACTION_PHASE)

    def test_no_cards_phase_simple(self):
        self.assertEqual(self.board.phase, GamePhase.DRAW_PHASE)
        TakeCardAction().execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.ACTION_PHASE)
        # Fake the players hand into having only 3 cards that can be put on the board
        self.game.current_player.hand.clear()
        series_cards = [Card(3, HEARTS), Card(4, HEARTS), Card(5, HEARTS)]
        self.game.current_player.hand.add(series_cards)
        # Play the series
        PutAction(series_cards).execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.NO_CARDS_PHASE)
        validated_actions = ActionService().get_valid_actions(self.game.current_player, self.board)
        self.assertEqual(len(validated_actions), 2)
        self.assertIn(TakePileAction(PileSide.LEFT), validated_actions)
        self.assertIn(TakePileAction(PileSide.RIGHT), validated_actions)
        TakePileAction(PileSide.LEFT).execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.ACTION_PHASE)

    def test_no_cards_end_turn_phase_simple(self):
        self.assertEqual(self.board.phase, GamePhase.DRAW_PHASE)
        TakeCardAction().execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.ACTION_PHASE)
        # Fake the players hand into having only 1 card that can be discarded
        self.game.current_player.hand.clear()
        card = Card(3, HEARTS)
        self.game.current_player.hand.add(card)
        # Discard the card
        DiscardCardAction(card).execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.NO_CARDS_END_TURN_PHASE)
        validated_actions = ActionService().get_valid_actions(self.game.current_player, self.board)
        self.assertEqual(len(validated_actions), 2)
        self.assertIn(TakePileAction(PileSide.LEFT), validated_actions)
        self.assertIn(TakePileAction(PileSide.RIGHT), validated_actions)
        TakePileAction(PileSide.LEFT).execute(self.game.current_player, self.board)
        self.assertEqual(self.board.phase, GamePhase.END_TURN_PHASE)