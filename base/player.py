from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Optional, TYPE_CHECKING

import pygame

from base.cards.hand import Hand
from base.constants import Constants
from base.drawable import Drawable
from base.enums.game_phase import GamePhase
from base.enums.team_color import TeamColor
from base.team import Team

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class Player(Drawable, metaclass=ABCMeta):

    def __init__(self, identifier: int):
        self.hand = None  # type: Optional[Hand]
        self.identifier = identifier
        self.team = None
        self._pile_grabbed = False

    @property
    @abstractmethod
    def is_human(self):
        raise NotImplementedError

    @abstractmethod
    def _choose_action(self, game_state: 'GameState') -> 'Action':
        """
        Return an action to take given the current GameState.

        The chosen action must be an eligible one given the current state, invalid actions will result in an Exception.
        A valid series of actions will always result in a END_TURN_PHASE game phase which ends the players turn.
        """
        raise NotImplementedError

    def draw(self, screen) -> None:
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('freesansbold.ttf', Constants.DEFAULT_FONT_SIZE)
        # create a text suface object,
        # on which text is drawn on it.
        text = font.render('{} {} {}'.format("HUMAN" if self.is_human else "AI", self.identifier, self.team.color),
                           True, (0, 0, 0), (255, 255, 255))
        # create a rectangular object for the
        # text surface object
        text_rect = text.get_rect()
        # set the center of the rectangular object.
        if self.team_color == TeamColor.BLUE:
            width_offset = (Constants.SCREEN_WIDTH // 2) * 0.8
            x_offset = width_offset if self.identifier == 1 else -width_offset
            y_offset = -Constants.SCREEN_WIDTH * 0.1
        else:
            height_offset = (Constants.SCREEN_HEIGHT // 2) * 0.9
            x_offset = 0
            y_offset = height_offset if self.identifier == 2 else -height_offset
        text_rect.center = (x_offset + (Constants.SCREEN_WIDTH // 2), y_offset + (Constants.SCREEN_HEIGHT // 2))
        # draw the text
        screen.blit(text, text_rect)

    @property
    def team_color(self):
        return self.team.color

    def set_pile_grabbed(self):
        self.team.set_pile_grabbed()
        self._pile_grabbed = True

    def has_grabbed_pile(self):
        return self._pile_grabbed

    def play(self, game_state: 'GameState'):
        """Play a set of moves while it is this players turn based on the given GameState."""
        while not game_state.board.phase == GamePhase.END_TURN_PHASE:
            action = self._choose_action(game_state)
            print("Executing {}".format(action))
            action.execute(self, game_state.board)

    def deal(self, hand: Hand):
        self.hand = hand

    def num_cards(self) -> int:
        return self.hand.num_cards()

    def set_team(self, team: 'Team'):
        self.team = team

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print_str = str(self.identifier) + " " + self.team_color.value + "\n"
        print_str += str(self.hand)
        return print_str
