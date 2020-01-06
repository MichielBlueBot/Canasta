from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.game_resource import GameResource
from api.games_resource import GamesResource
from api.state_resource import StateResource


class CanastaAPI:

    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        CORS(self.app, resources={r"/api/*": {"origins": "*"}})
        self._add_resources()

    def _add_resources(self):
        self.api.add_resource(StateResource, '/api/state')
        self.api.add_resource(GameResource, '/api/game')
        self.api.add_resource(GamesResource, '/api/games')

    def run(self):
        self.app.run(host="localhost", port=4800)


if __name__ == '__main__':
    CanastaAPI().run()
