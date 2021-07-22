import sys
import argparse

sys.path.append('../')

from Snake.game import Game
from Snake.agent import RandomAgent, EvolutionAgent

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--use_agent', action='store_true', default=True)

    args = argparser.parse_args()

    if args.use_agent:
        Game(agent=EvolutionAgent()).run()
    else:
        Game().run()
