import json

from flask import request
from flask_restful import Resource

from base.game import Game
from run.game_runner import GameRunner


class StateResource(Resource):

    def get(self):
        """Get the state (as JSON) of the game identified by the gameId parameter"""
        args = request.args
        game_id = args["gameId"]
        game = GameRunner().get_game(game_id)
        if game:
            return self.game_to_json(game)
        return "Game not found", 204

    @staticmethod
    def game_to_json(game: Game) -> str:
        return json.dumps(indent=2, obj={
            "isFinished": game.is_finished(),
            "phase": game.board.phase.name,
            "currentPlayerIndex": game.current_player_index,
            "players": [
                {"playerId": player.identifier,
                 "isCurrentPlayer": idx == game.current_player_index,
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
                for idx, player in enumerate(game.players)
            ],
            "deck": {"numCards": game.board.deck.num_cards()},
            "stack": {"numCards": game.board.stack.num_cards(),
                      "topCard": {"rank": game.board.stack.look().get_rank(),
                                  "suit": game.board.stack.look().get_suit()}
                      if game.board.stack.num_cards() > 0 else None
                      },
            "leftPile": {"active": game.board.left_pile_active(),
                         "numCards": game.board.left_pile.num_cards() if game.board.left_pile_active() else 0},

            "rightPile": {"active": game.board.right_pile_active(),
                          "numCards": game.board.right_pile.num_cards() if game.board.right_pile_active() else 0},
            "redTeamSeries": [
                {
                    "cards": [{"rank": card.get_rank(),
                               "suit": card.get_suit(),
                               "shortRank": card.translate_rank_short() if not card.is_joker() else "J",
                               "shortSuit": card.get_suit()[0].upper(),
                               "isJoker": card.is_joker()} for card in series.get_raw_cards()],
                    "isDirty": series.is_dirty(),
                    "isPure": series.is_pure(),
                    "isFiveHundred": series.is_five_hundred(),
                    "isThousand": series.is_thousand(),
                } for series in game.board.red_team_series
            ],
            "blueTeamSeries": [
                {
                    "cards": [{"rank": card.get_rank(),
                               "suit": card.get_suit(),
                               "shortRank": card.translate_rank_short() if not card.is_joker() else "J",
                               "shortSuit": card.get_suit()[0].upper(),
                               "isJoker": card.is_joker()} for card in series.get_raw_cards()],
                    "isDirty": series.is_dirty(),
                    "isPure": series.is_pure(),
                    "isFiveHundred": series.is_five_hundred(),
                    "isThousand": series.is_thousand(),
                } for series in game.board.blue_team_series
            ],
            "redTeamScore": game.get_red_team_score(),
            "blueTeamScore": game.get_red_team_score(),
        })
