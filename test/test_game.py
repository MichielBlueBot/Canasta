from unittest import TestCase

from base.game import Game


class TestGame(TestCase):

    def test_game_initialization(self):
        game = Game()
        game.initialize_game()
        # CHECK PLAYERS AND TEAMS
        self.assertTrue(len(game.players), 4)
        self.assertTrue(len(game.teams) == 2)
        self.assertTrue(game.current_team_index == 0)
        self.assertTrue(game.current_player_index == 0)
        # CHECK PLAYER HANDS
        for player in game.players:
            self.assertTrue(player.num_cards() == 11)
            self.assertTrue(player.team_color is not None)
        # CHECK BOARD PILES
        self.assertTrue(game.board.num_piles_remaining() == 2)
        self.assertTrue(game.board.right_pile_active())
        self.assertTrue(game.board.right_pile.num_cards() == 11)
        self.assertTrue(game.board.left_pile_active())
        self.assertTrue(game.board.left_pile.num_cards() == 11)
        # CHECK BOARD DECK
        self.assertTrue(game.board.deck.num_cards() >= 0)
        self.assertFalse(game.board.deck.is_empty())
