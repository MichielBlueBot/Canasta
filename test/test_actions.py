from unittest import TestCase

from base.actions.action_list import ALL_ACTIONS
from base.actions.add_front_action import AddFrontAction
from base.actions.put_action import PutAction
from base.actions.swap_two_action import SwapTwoAction
from base.card import Card
from base.enums.game_phase import GamePhase
from base.enums.two_swap_direction import TwoSwapDirection
from base.game import Game


class TestGamePhase(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.initialize_game()

    def test_swap_two(self):
        # Execute a put action for the first player that includes a 2
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        target_player.hand.add(Card(10, "Hearts"))
        target_player.hand.add(Card(12, "Hearts"))
        target_player.hand.add(Card(2, "Spades"))
        put_action = PutAction([Card(10, "Hearts"), Card(2, 'Spades'), Card(12, "Hearts")])
        put_action.execute(target_player, self.game.board)
        # Give the player the proper swap card
        target_card = Card(11, "Hearts")
        target_player.hand.add(target_card)
        # Ensure the player can now perform the swap two actions
        validated_actions = [a for a in ALL_ACTIONS if a.validate(player=target_player,
                                                                  board=self.game.board)]
        target_series = self.game.board.get_series_for_player(target_player)[0]
        swap_two_front_action = SwapTwoAction(card=target_card,
                                              series=target_series,
                                              direction=TwoSwapDirection.FRONT)
        swap_two_back_action = SwapTwoAction(card=target_card,
                                             series=target_series,
                                             direction=TwoSwapDirection.BACK)
        self.assertIn(swap_two_front_action, validated_actions)
        self.assertIn(swap_two_back_action, validated_actions)
        # Execute the action
        swap_two_front_action.execute(target_player, self.game.board)
        # Ensure the card has been added
        self.assertIn(target_card, target_series)
        # Ensure the 2 is now at the front of the series
        self.assertEqual(Card(2, "Spades"), target_series.get_card(0))
        # Ensure the card has been removed from the players hand
        self.assertNotIn(target_card, target_player.hand)

    def test_add_front(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        target_player.hand.add(Card(10, "Hearts"))
        target_player.hand.add(Card(11, "Hearts"))
        target_player.hand.add(Card(12, "Hearts"))
        put_action = PutAction([Card(10, "Hearts"), Card(11, 'Hearts'), Card(12, "Hearts")])
        put_action.execute(target_player, self.game.board)
        # Give the player the proper add card
        target_player.hand.add(Card(9, "Hearts"))
        # Ensure the player can now perform the add front action
        validated_actions = [a for a in ALL_ACTIONS if a.validate(player=target_player,
                                                                  board=self.game.board)]
        target_series = self.game.board.get_series_for_player(target_player)[0]
        add_front_action = AddFrontAction(card=Card(9, "Hearts"),
                                          series=target_series)
        self.assertIn(add_front_action, validated_actions)
        # Execute the action
        add_front_action.execute(target_player, self.game.board)
        # Ensure the card has been added
        self.assertIn(Card(9, "Hearts"), target_series)
        # Ensure the card has been removed from the players hand
        self.assertNotIn(Card(9, "Hearts"), target_player.hand)

    def test_initial_phase(self):
        validated_actions = [a for a in ALL_ACTIONS if a.validate(player=self.game.players[self.game.current_player_idx],
                                                                  board=self.game.board)]
        self.assertEqual(2, len(validated_actions))  # initial possible actions are TakeCardAction and TakeStackAction
