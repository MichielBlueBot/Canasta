from typing import List

from base.card import Card
from base.cards.card_series import CardSeries
from base.cards.deck import Deck
from base.cards.stack import Stack
from base.enums.game_phase import GamePhase
from base.enums.pile_side import PileSide
from base.player import Player
from base.team import Team
from base.enums.team_color import TeamColor


class Board:

    def __init__(self, deck: Deck, left_pile: Stack, right_pile):
        self.phase = None
        self.deck = deck
        self.left_pile = left_pile
        self.right_pile = right_pile
        self.stack = Stack()
        self.red_team_series = []  # type: List[CardSeries]
        self.blue_team_series = []  # type: List[CardSeries]

    def set_phase(self, phase: GamePhase):
        self.phase = phase

    def get_series_for_player(self, player: Player) -> List[CardSeries]:
        """Return the BLUE or RED series on the board depending on the given player."""
        return self.get_series_for_team(player.team)

    def get_series_for_team(self, team: Team) -> List[CardSeries]:
        """Return the BLUE or RED series on the board depending on the given team."""
        if team.color == TeamColor.BLUE:
            return self.blue_team_series
        else:
            return self.red_team_series

    def num_piles_remaining(self) -> int:
        num_piles = 0
        if self.left_pile_active:
            num_piles += 1
        if self.right_pile_active:
            num_piles += 1
        return num_piles

    def left_pile_active(self) -> bool:
        return self.left_pile is not None

    def right_pile_active(self) -> bool:
        return self.right_pile is not None

    def grab_pile(self, side: PileSide) -> List[Card]:
        if side == PileSide.LEFT:
            return self.grab_left_pile()
        elif side == PileSide.RIGHT:
            return self.grab_right_pile()
        else:
            raise Exception("Unknown pile side {}. Use PileSide enum!".format(side))

    def grab_left_pile(self) -> List[Card]:
        cards = self.left_pile.grab()
        self.left_pile = None
        return cards

    def grab_right_pile(self) -> List[Card]:
        cards = self.right_pile.grab()
        self.right_pile = None
        return cards

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print_str = ""
        print_str += "-------------------- BOARD ----------------------" + "\n"
        print_str += "Left pile: {}".format(self.left_pile_active()) + "\n"
        print_str += "Right pile: {}".format(self.right_pile_active()) + "\n"
        print_str += "Deck: {} cards left".format(self.deck.num_cards()) + "\n"
        print_str += "{}".format(self.stack) + "\n"
        print_str += "------------------------------------------------" + "\n"
        print_str += "RED TEAM:" + "\n"
        for card_set in self.red_team_series:
            print_str += "\t" + str(card_set) + "\n"
        print_str += "------------------------------------------------" + "\n"
        print_str += "BLUE TEAM:" + "\n"
        for card_set in self.blue_team_series:
            print_str += "\t" + str(card_set) + "\n"
        print_str += "------------------------------------------------" + "\n"
        return print_str

    def player_may_clear_hand(self, player: 'Player') -> bool:
        if not player.team.has_grabbed_pile():
            return True
        else:
            return self.team_has_pure(player.team)

    def team_has_pure(self, team: 'Team') -> bool:
        for series in self.get_series_for_team(team):
            if series.is_pure():
                return True
        return False

