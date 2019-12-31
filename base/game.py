from typing import List, Optional

from base.ai.ai_player import AIPlayer
from base.board import Board
from base.cards.deck import Deck
from base.cards.double_deck import DoubleDeck
from base.cards.hand import Hand
from base.cards.stack import Stack
from base.constants import Constants
from base.enums.game_phase import GamePhase
from base.enums.team_color import TeamColor
from base.game_state import GameState
from base.human_player import HumanPlayer
from base.player import Player
from base.team import Team


class Game:

    def __init__(self):
        self.players = None  # type: Optional[List[Player]]
        self.teams = None  # type: Optional[List[Team]]
        self.current_player_idx = None
        self.current_team_idx = None
        self.board = None  # type: Optional[Board]
        self.initialized = False

    def reset_game(self, initialize: bool = True):
        self.players = None  # type: Optional[List[Player]]
        self.teams = None  # type: Optional[List[Team]]
        self.current_player_idx = None
        self.current_team_idx = None
        self.board = None  # type: Optional[Board]
        self.initialized = False
        if initialize:
            self.initialize_game()

    def initialize_game(self):
        if not self.initialized:
            self.current_player_idx = 0
            self.current_team_idx = 0
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
            self.board.set_phase(GamePhase.DRAW_PHASE)
            self.initialized = True

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_idx]

    @property
    def current_team(self) -> Team:
        return self.teams[self.current_team_idx]

    def play(self):
        if not self.initialized:
            raise Exception("Game not initialized")
        while not self.is_finished():
            self.print()
            print("Current player: {}".format(self.current_player_idx))
            self.players[self.current_player_idx].play(self.get_state())
            self._next_player_turn()

    def get_state(self) -> GameState:
        """Return the current GameState of this Board."""
        return GameState(self.board, self.players, self.current_player_idx)

    def is_finished(self) -> bool:
        """
        Return True if the game is finished.

        The game can finish in the following ways:
            - The deck is empty and there are no piles remaining to serve as the new deck.
            - A player has no cards left while having already picked their teams pile and having a pure on the board.
        """
        if self.board.deck.is_empty() and self.board.num_piles_remaining() == 0:
            # No cards left to play
            return True
        for player in self.players:
            if player.hand.is_empty() and player.team.has_grabbed_pile() and self.board.team_has_pure(player.team):
                # Player finished the game
                return True
        return False

    def _next_player_turn(self) -> None:
        """Increment the player and team counters to indicate it's now the next players turn."""
        self.current_player_idx += 1
        self.current_player_idx %= Constants.NUM_PLAYERS
        self.current_team_idx += 1
        self.current_team_idx %= Constants.NUM_TEAMS
        self.board.set_phase(GamePhase.DRAW_PHASE)

    def _initialize_players(self) -> None:
        self.players = [AIPlayer(i) if i in Constants.AI_PLAYER_INDEXES else HumanPlayer(i)
                        for i in range(Constants.NUM_PLAYERS)]
        team_red = Team(players=[self.players[0], self.players[2]], color=TeamColor.RED)
        self.players[0].set_team(team_red)
        self.players[2].set_team(team_red)
        team_blue = Team(players=[self.players[1], self.players[3]], color=TeamColor.BLUE)
        self.players[1].set_team(team_blue)
        self.players[3].set_team(team_blue)
        self.teams = [team_red, team_blue]

    @staticmethod
    def _create_deck() -> Deck:
        deck = DoubleDeck(with_jokers=True)
        deck.shuffle()
        return deck

    def _deal_hands(self, deck: Deck):
        """Deal cards from the deck to each player to create a their starting hands."""
        # Draw cards from the deck
        hands = [Hand(deck.deal_n(Constants.NUM_CARDS_IN_STARTING_HAND)) for _ in range(len(self.players))]
        # Hand the cards to each player
        for i, player in enumerate(self.players):
            player.deal(hands[i])

    def _initialize_board(self, deck):
        left_pile_cards = Stack(deck.deal_n(Constants.NUM_CARDS_IN_PILE))
        right_pile_cards = Stack(deck.deal_n(Constants.NUM_CARDS_IN_PILE))
        self.board = Board(deck=deck, left_pile=left_pile_cards, right_pile=right_pile_cards)

    def _initialize_board_stack(self):
        """Deal 1 card onto the stack."""
        card = self.board.deck.deal()
        self.board.stack.put(card)

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
