from run.game_runner import GameRunner

if __name__ == '__main__':
    game_runner = GameRunner()
    game_id, game = game_runner.start_game()
    game.play()
