from flask_restful import Resource

from run.game_runner import GameRunner


class GameResource(Resource):

    @staticmethod
    def get():
        game_runner = GameRunner()
        game_id, _ = game_runner.start_game()
        return game_id
