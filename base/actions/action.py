from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.player import Player


class Action(metaclass=ABCMeta):

    @abstractmethod
    def validate(self, player: 'Player', board: 'Board'):
        raise NotImplementedError

    @abstractmethod
    def _execute(self, player: 'Player', board: 'Board'):
        raise NotImplementedError

    @abstractmethod
    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        raise NotImplementedError

    def execute(self, player: 'Player', board: 'Board') -> None:
        """
        Validate this action for the given player and board, execute the action and update the board phase.

        :param player: player performing the action
        :param board: board on which the action is performed
        """
        if not self.validate(player=player, board=board):
            raise Exception("Invalid action. \n {} \n {} \n {}".format(self, player, board))
        self._execute(player, board)
        board.set_phase(self._target_phase())
