from typing import List

from base.actions.action import Action
from base.action_service import ActionService
from base.ai.controlled_player import ControlledPlayer
from base.constants import Constants
from base.enums.team_color import TeamColor
from base.game import Game
from base.team import Team


class ControlledGame(Game):

    def __init__(self):
        super().__init__()

    def play(self, verbose: bool = False):
        raise NotImplemented("The training game can only be played through the play_action() function.")

    def play_action(self, action: Action):
        if not self.initialized:
            raise Exception("Game not initialized")
        print("Current player: {}".format(self.current_player_idx))
        self.players[self.current_player_idx].play_action(game_state=self.get_state(), action=action)

    def switch_player_turns(self):
        self._next_player_turn()

    def get_current_actions_mask(self) -> List[bool]:
        """Return a boolean mask representing the current valid actions."""
        return ActionService().get_valid_actions_mask(self.current_player, self.board)

    def _initialize_players(self) -> None:
        self.players = [ControlledPlayer(i) for i in range(Constants.NUM_PLAYERS)]
        team_red = Team(players=[self.players[0], self.players[2]], color=TeamColor.RED)
        self.players[0].set_team(team_red)
        self.players[2].set_team(team_red)
        team_blue = Team(players=[self.players[1], self.players[3]], color=TeamColor.BLUE)
        self.players[1].set_team(team_blue)
        self.players[3].set_team(team_blue)
        self.teams = [team_red, team_blue]
