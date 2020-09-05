import argparse
from src import Game

p = argparse.ArgumentParser(description="TickTacToe Game")

p.add_argument("skip",
                metavar="skip",
                type=bool,
                default=False,
                help="Human Player Name")

a = p.parse_args()

g = Game()
# Skip intro screen
if a.skip:
    g.update_settings({
        "state": 1,
        "human_name": "James",
        "human_figure": "X",
        "computer_name": "Tom",
        "computer_figure": "0",
        "board_size": 3
    })
g.play_game_main()
