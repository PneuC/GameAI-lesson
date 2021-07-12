import argparse
from game import Game
from agent import RandomAgent


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--use_agent', action='store_true', default=False)

    args = argparser.parse_args()

    if args.use_agent:
        Game(agent=RandomAgent()).run()
    else:
        Game().run()
