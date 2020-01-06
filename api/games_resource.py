from flask import request
from flask_restful import Resource

from run.game_runner import GameRunner


class GamesResource(Resource):

    @staticmethod
    def get():
        """Get a list of IDs for all running games."""
        game_runner = GameRunner()
        return game_runner.get_running_games()

