from unittest import TestCase

from base.action_service import ActionService
from base.actions.add_back_action import AddBackAction
from base.actions.add_front_action import AddFrontAction
from base.actions.discard_card_action import DiscardCardAction
from base.actions.put_action import PutAction
from base.actions.swap_joker_action import SwapJokerAction
from base.actions.swap_two_action import SwapTwoAction
from base.actions.take_card_action import TakeCardAction
from base.actions.take_pile_action import TakePileAction
from base.actions.take_stack_action import TakeStackAction
from base.card import Card
from base.enums.game_phase import GamePhase
from base.enums.pile_side import PileSide
from base.enums.two_swap_direction import TwoSwapDirection
from base.game import Game
from base.utils.card_constants import JOKER_RANK, JOKER_SUIT


class TestGamePhase(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.initialize_game()

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
        target_card = Card(9, "Hearts")
        target_player.hand.add(target_card)
        # Ensure the player can now perform the add front action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        target_series = self.game.board.get_series_for_player(target_player)[0]
        add_front_action = AddFrontAction(card=target_card,
                                          series=target_series)
        self.assertIn(add_front_action, validated_actions)
        # Execute the action
        add_front_action.execute(target_player, self.game.board)
        # Ensure the card has been added
        self.assertIn(target_card, target_series)
        # Ensure the card has been removed from the players hand
        self.assertNotIn(target_card, target_player.hand)

    def test_add_back(self):
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
        target_card = Card(13, "Hearts")
        target_player.hand.add(target_card)
        # Ensure the player can now perform the add back action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        target_series = self.game.board.get_series_for_player(target_player)[0]
        add_back_action = AddBackAction(card=target_card,
                                        series=target_series)
        self.assertIn(add_back_action, validated_actions)
        # Execute the action
        add_back_action.execute(target_player, self.game.board)
        # Ensure the card has been added
        self.assertIn(target_card, target_series)
        # Ensure the card has been removed from the players hand
        self.assertNotIn(target_card, target_player.hand)

    def test_discard_card(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        # Give the player the proper add card
        target_card = Card(10, "Hearts")
        target_player.hand.add(target_card)
        # Ensure the player can now perform the discard card action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        discard_card_action = DiscardCardAction(card=target_card)
        self.assertIn(discard_card_action, validated_actions)
        # Execute the action
        discard_card_action.execute(target_player, self.game.board)
        # Ensure the card has been discarded to the stack
        self.assertEqual(target_card, self.game.board.stack.look())
        # Ensure the card has been removed from the players hand
        self.assertNotIn(target_card, target_player.hand)
        # Check the game phase
        self.assertEqual(GamePhase.END_TURN_PHASE, self.game.board.phase)

    def test_put_action(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        target_cards = [Card(10, "Hearts"), Card(11, 'Hearts'), Card(12, "Hearts")]
        for card in target_cards:
            target_player.hand.add(card)
        put_action = PutAction(target_cards)
        # Ensure the player can now perform the put action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        self.assertIn(put_action, validated_actions)
        # Execute the action
        put_action.execute(target_player, self.game.board)
        target_series = self.game.board.get_series_for_player(target_player)[0]
        # Ensure the series has been added
        self.assertEqual(target_cards, target_series.get_raw_cards())
        # Ensure the cards have been removed from the players hand
        for card in target_cards:
            self.assertNotIn(card, target_player.hand)

    def test_swap_joker(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        cards = [Card(10, "Hearts"), Card(JOKER_RANK, JOKER_SUIT), Card(12, "Hearts")]
        for card in cards:
            target_player.hand.add(card)
        put_action = PutAction(cards)
        put_action.execute(target_player, self.game.board)
        # Give the player the proper swap card
        target_card = Card(11, "Hearts")
        target_player.hand.add(target_card)
        # Ensure the player can now perform the add back action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        target_series = self.game.board.get_series_for_player(target_player)[0]
        swap_joker_action = SwapJokerAction(card=target_card,
                                            series=target_series)
        self.assertIn(swap_joker_action, validated_actions)
        # Execute the action
        swap_joker_action.execute(target_player, self.game.board)
        # Ensure the card has been added
        self.assertIn(target_card, target_series)
        # Ensure the card has been removed from the players hand
        self.assertNotIn(target_card, target_player.hand)
        # Ensure the joker is now in the players hand
        self.assertIn(Card(JOKER_RANK, JOKER_SUIT), target_player.hand)
        # Ensure the game now forces the player to play the joker
        self.assertEqual(GamePhase.PLAY_JOKER_PHASE, self.game.board.phase)

    def test_swap_two_front(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        target_two = Card(2, "Diamonds")
        cards = [Card(10, "Hearts"), target_two, Card(12, "Hearts")]
        for card in cards:
            target_player.hand.add(card)
        put_action = PutAction(cards)
        put_action.execute(target_player, self.game.board)
        # Give the player the proper swap card
        target_card = Card(11, "Hearts")
        target_player.hand.add(target_card)
        # Ensure the player can now perform the swap two action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        target_series = self.game.board.get_series_for_player(target_player)[0]
        swap_two_action = SwapTwoAction(card=target_card,
                                        series=target_series,
                                        direction=TwoSwapDirection.FRONT)
        self.assertIn(swap_two_action, validated_actions)
        # Execute the action
        swap_two_action.execute(target_player, self.game.board)
        # Ensure the card has been added
        self.assertIn(target_card, target_series)
        # Ensure the card has been removed from the players hand
        self.assertNotIn(target_card, target_player.hand)
        # Ensure the two is still in the series
        self.assertEqual(target_two, target_series.get_card(0))

    def test_swap_two_back(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        target_two = Card(2, "Diamonds")
        cards = [Card(10, "Hearts"), target_two, Card(12, "Hearts")]
        for card in cards:
            target_player.hand.add(card)
        put_action = PutAction(cards)
        put_action.execute(target_player, self.game.board)
        # Give the player the proper swap card
        target_card = Card(11, "Hearts")
        target_player.hand.add(target_card)
        # Ensure the player can now perform the swap two action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        target_series = self.game.board.get_series_for_player(target_player)[0]
        swap_two_action = SwapTwoAction(card=target_card,
                                        series=target_series,
                                        direction=TwoSwapDirection.BACK)
        self.assertIn(swap_two_action, validated_actions)
        # Execute the action
        swap_two_action.execute(target_player, self.game.board)
        # Ensure the card has been added
        self.assertIn(target_card, target_series)
        # Ensure the card has been removed from the players hand
        self.assertNotIn(target_card, target_player.hand)
        # Ensure the two is still in the series
        self.assertEqual(target_two, target_series.get_card(-1))

    def test_take_card(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.DRAW_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        take_card_action = TakeCardAction()
        # Ensure the player can now perform the add back action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        self.assertIn(take_card_action, validated_actions)
        num_cards_in_deck_before_action = self.game.board.deck.num_cards()
        num_cards_in_hand_before_action = target_player.hand.num_cards()
        # Execute the action
        take_card_action.execute(target_player, self.game.board)
        self.assertEqual(self.game.board.deck.num_cards(), num_cards_in_deck_before_action - 1)
        self.assertEqual(target_player.hand.num_cards(), num_cards_in_hand_before_action + 1)

    def test_take_pile(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        # We're going to let the player put down it's last 3 cards to be eligible to grab a pile
        target_player.hand.clear()
        cards = [Card(10, "Hearts"), Card(11, "Hearts"), Card(12, "Hearts")]
        for card in cards:
            target_player.hand.add(card)
        put_action = PutAction(cards)
        put_action.execute(target_player, self.game.board)
        # Make sure we're now in the correct phase to grab the pile
        self.assertEqual(GamePhase.NO_CARDS_PHASE, self.game.board.phase)
        take_pile_action = TakePileAction(side=PileSide.LEFT)
        # Ensure the player can now perform the take pile action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        self.assertIn(take_pile_action, validated_actions)
        self.assertFalse(target_player.has_grabbed_pile())
        self.assertFalse(target_player.team.has_grabbed_pile())
        self.assertTrue(self.game.board.left_pile_active())
        cards_in_pile = self.game.board.left_pile.get_raw_cards()
        # Execute the action
        take_pile_action.execute(target_player, self.game.board)
        self.assertTrue(target_player.has_grabbed_pile())
        self.assertTrue(target_player.team.has_grabbed_pile())
        self.assertFalse(self.game.board.left_pile_active())
        self.assertGreater(target_player.num_cards(), 0)
        for card in cards_in_pile:
            self.assertIn(card, target_player.hand)

    def test_take_stack(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        self.game.board.set_phase(GamePhase.DRAW_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, "Hearts"))  # random card so hand isn't empty or game will complain
        self.game.board.stack.put(Card(11, "Hearts"))
        self.game.board.stack.put(Card(12, "Hearts"))
        cards_in_stack = self.game.board.stack.get_raw_cards()
        take_stack_action = TakeStackAction()
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        self.assertIn(take_stack_action, validated_actions)
        # Execute the action
        take_stack_action.execute(target_player, self.game.board)
        for card in cards_in_stack:
            self.assertIn(card, target_player.hand)
            self.assertNotIn(card, self.game.board.stack)
        # Make sure we've moved to the action phase
        self.assertEqual(GamePhase.ACTION_PHASE, self.game.board.phase)

    def test_initial_phase(self):
        validated_actions = ActionService().get_valid_actions(self.game.current_player, self.game.board)
        self.assertEqual(2, len(validated_actions))  # initial possible actions are TakeCardAction and TakeStackAction
