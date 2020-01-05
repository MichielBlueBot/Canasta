from flask import request
from flask_restful import Resource

from run.game_runner import GameRunner


class GameResource(Resource):

    @staticmethod
    def get():
        """Start a new game and return the gameId"""
        game_runner = GameRunner()
        game_id, _ = game_runner.start_game()
        return game_id

    @staticmethod
    def post():
        """Play a single step in the game specified by the gameId parameter"""
        args = request.args
        game_id = args["gameId"]
        game = GameRunner().get_game(game_id)
        if game:
            game.play_single_step()
        return "Game not found", 204
