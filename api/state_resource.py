import json

from flask import request
from flask_restful import Resource

from base.game_state import GameState
from run.game_runner import GameRunner


class StateResource(Resource):

    def get(self):
        args = request.args
        game_id = args["gameId"]
        game = GameRunner().get_game(game_id)
        if game:
            game_state = game.get_state()
            return self._game_state_to_json(game_state)
        return "Game not found", 204

    @staticmethod
    def _game_state_to_json(game_state: GameState) -> str:
        return json.dumps(indent=2, obj={
            "phase": game_state.board.phase.name,
            "currentPlayerIndex": game_state.current_player_index,
            "players": [
                {"playerId": player.identifier,
                 "isCurrentPlayer": idx == game_state.current_player_index,
                 "isHuman": player.is_human,
                 "teamColor": player.team_color.value,
                 "numCards": player.num_cards(),
                 "hasGrabbedPile": player.has_grabbed_pile(),
                 "cards": [{"rank": card.get_rank(),
                            "suit": card.get_suit(),
                            "shortRank": card.translate_rank_short() if not card.is_joker() else "J",
                            "shortSuit": card.get_suit()[0].upper(),
                            "isJoker": card.is_joker()
                            } for card in sorted(player.hand)],
                 }
                for idx, player in enumerate(game_state.players)
            ],
            "deck": {"numCards": game_state.board.deck.num_cards()},
            "stack": {"numCards": game_state.board.stack.num_cards(),
                      "topCard": {"rank": game_state.board.stack.look().get_rank(),
                                  "suit": game_state.board.stack.look().get_suit()}
                      },
            "leftPile": {"active": game_state.board.left_pile_active(),
                         "numCards": game_state.board.left_pile.num_cards()},

            "rightPile": {"active": game_state.board.right_pile_active(),
                          "numCards": game_state.board.right_pile.num_cards()}
        })
