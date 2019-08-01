from typing import List, TYPE_CHECKING

from base.enums.team_color import TeamColor

if TYPE_CHECKING:
    from base.player import Player


class Team:

    def __init__(self, players: List['Player'], color: TeamColor):
        self.players = players
        self.color = color
        self._pile_grabbed = False

    def set_pile_grabbed(self):
        self._pile_grabbed = True

    def has_grabbed_pile(self):
        return self._pile_grabbed
