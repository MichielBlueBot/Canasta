from typing import List, Optional

from base.board import Board
from base.cards.deck import Deck
from base.cards.double_deck import DoubleDeck
from base.cards.hand import Hand
from base.cards.stack import Stack
from base.enums.game_phase import GamePhase
from base.game_state import GameState
from base.player import Player
from base.team import Team
from base.enums.team_color import TeamColor


class Game:

    def __init__(self):
        self.players = None  # type: Optional[List[Player]]
        self.teams = None  # type: Optional[List[Team]]
        self.current_player = 0
        self.current_team = 0
        self.board = None  # type: Optional[Board]

    def initialize_game(self):
        # Initialize players
        self._initialize_players()
        # Create new deck
        deck = self._create_deck()
        # Deal player hands
        self._deal_hands(deck)
        # Set up board (deck and piles)
        self._initialize_board(deck)
        # Set up the initial stack (one card from deck)
        self._initialize_board_stack()
        # Set up game phase
        self._initialize_game_phase()

    def play(self):
        while not self._is_finished():
            self.print()
            print("Current player: {}".format(self.current_player))
            self.players[self.current_player].play(GameState(self.board, self.players))
            self._next_player_turn()

    def _next_player_turn(self):
        self.current_player += 1
        self.current_player %= 4
        self.current_team += 1
        self.current_team %= 2
        self.board.set_phase(GamePhase.DRAW_PHASE)

    def _is_finished(self):
        if self.board.deck.is_empty() and self.board.num_piles_remaining() == 0:
            # No cards left to play
            return True
        for player in self.players:
            if player.hand.is_empty() and player.team.has_grabbed_pile() and self.board.team_has_pure(player.team):
                # Player finished the game
                return True
        return False

    def _initialize_players(self):
        player_0 = Player(identifier=0)
        player_1 = Player(identifier=1)
        player_2 = Player(identifier=2)
        player_3 = Player(identifier=3)
        self.players = [player_0, player_1, player_2, player_3]
        team_red = Team(players=[player_0, player_2], color=TeamColor.RED)
        player_0.set_team(team_red)
        player_2.set_team(team_red)
        team_blue = Team(players=[player_1, player_3], color=TeamColor.BLUE)
        player_1.set_team(team_blue)
        player_3.set_team(team_blue)
        self.teams = [team_red, team_blue]
        self.current_player = 0

    @staticmethod
    def _create_deck() -> Deck:
        deck = DoubleDeck(with_jokers=True)
        deck.shuffle()
        return deck

    def _deal_hands(self, deck: Deck):
        hands = [Hand(deck.deal_n(11)) for _ in range(len(self.players))]
        for i, player in enumerate(self.players):
            player.deal(hands[i])

    def _initialize_board(self, deck):
        left_pile_cards = Stack(deck.deal_n(11))
        right_pile_cards = Stack(deck.deal_n(11))
        self.board = Board(deck=deck, left_pile=left_pile_cards, right_pile=right_pile_cards)

    def _initialize_board_stack(self):
        # Deal 1 card onto the stack
        card = self.board.deck.deal()
        self.board.stack.put(card)

    def _initialize_game_phase(self):
        self.board.phase = GamePhase.DRAW_PHASE

    def print(self):
        if self.players is not None:
            for player in self.players:
                print(player)
        else:
            print("No players.")
        if self.board is not None:
            print(self.board)
        else:
            print("No board.")
