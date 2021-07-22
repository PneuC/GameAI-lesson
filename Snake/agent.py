"""
@DATE: 2021/7/10
@Author: Ziqi Wang & Keyuan Zhang
@File: agent.py
"""
import random
import time
import numpy as np

from abc import abstractmethod
from copy import deepcopy

from typing import List, Dict

from Snake.logic import GameWorld
from common import Directions


def simulate(world, action_seq: List[int]) -> Dict:
    """
    simulate the action sequence and get the state of the game
    """
    result = {
        'distance to bean': 0,
        'dead': False,
        'got bean': False
    }
    game_map = world.game_map.copy()
    snake = deepcopy(world.snake)
    for idx, action in enumerate(action_seq):
        snake.direction = Directions(action)
        res = snake.update(game_map, simulation=True)
        if res == 'got bean':
            result['got bean'] = True
        if snake.dead:
            result['dead'] = True
    result['distance to bean'] = abs(snake.head_pos - world.bean_pos).sum()
    return result

class Agent:
    @abstractmethod
    def make_decision(self, observation: GameWorld, timeBudget: int) -> int:
        pass


class RandomAgent(Agent):
    def __init__(self, action_itv=4):
        self.action_itv = action_itv
        self.action = 0
        self.step_count = 0

    def make_decision(self, observation: GameWorld, timeBudget: int) -> int:
        if self.step_count % self.action_itv == 0:
            self.action = random.randrange(4)
        self.step_count += 1
        return self.action


# =============================================================

# Constants
POPULATION_SIZE = 10
INDIVIDUAL_LENGTH = 5
ELITISM = 1


class EvolutionAgent(Agent):

    def __init__(self):

        self.population, self.next_population = [], []


    def make_decision(self, observation: GameWorld, time_budget: int) -> int:
        """
        Note: the Agent shouldn't use GameWorld.update() during evaluation.
        """
        start = time.time()
        remaining = time_budget - 20

        self.init_pop(observation)

        while (1000 * (time.time() - start)) < remaining:
            self.runIteration(observation)

        return self.get_best_action()

    def runIteration(self, observation: GameWorld):
        """
        evolve one generation
        :param observation: the current game state
        :return:
        """

        for i in range(ELITISM, POPULATION_SIZE):
            newind = self.crossover()  # crossover
            newind = self.mutate(newind)  # mutation

            self.next_population[i] = newind
            self.next_population[i] = self.evaluate(self.next_population[i], observation)

        self.next_population.sort(key=lambda x: x[-1])
        # selection
        self.population = deepcopy(self.next_population)

    def init_pop(self, observation: GameWorld):
        """
        initialize the population
        :param observation: current state for evaluation
        :return:
        """
        self.population, self.next_population = [], []
        for i in range(POPULATION_SIZE):
            self.population.append(np.random.randint(4, size=INDIVIDUAL_LENGTH + 1))
            self.population[i] = self.evaluate(self.population[i], observation)
            self.next_population.append(deepcopy(self.population[i]))
        self.population.sort(key=lambda x: x[-1])

    @staticmethod
    def evaluate(individual, observation):
        """
        evaluates an individual by rolling the current state with the actions in the individual
        :param individual: individual to be evaluated
        :param observation: current state, root of rollouts
        :return: fitness value of last state reached
        """
        indiv = deepcopy(individual)
        result = simulate(observation, indiv[:-1])

        # 问题1：为什么贪吃蛇吃不到豆子？
        # 问题2：怎样让贪吃蛇减少转弯的次数？（提示：惩罚需要转弯的动作序列）
        indiv[-1] = 10 * result['distance to bean'] + 1000 * result['dead'] - 100 * (result['got bean'])

        return indiv

    def crossover(self):
        """
        select parents and crossover to produce new individual
        :return: the new individual after crossover
        """
        newind = np.random.randint(4, size=INDIVIDUAL_LENGTH + 1)
        parents_ids = random.sample(range(1, POPULATION_SIZE), 2)

        parent1 = self.population[parents_ids[0]]
        parent2 = self.population[parents_ids[1]]

        for i in range(INDIVIDUAL_LENGTH):
            if random.random() >= 0.5:
                newind[i] = parent1[i]
            else:
                newind[i] = parent2[i]

        return newind

    @staticmethod
    def mutate(individual):
        """
        mutate the individual
        :param individual: the individual to be mutated
        :return: the new individual after mutation
        """
        ind = deepcopy(individual)
        for i in range(INDIVIDUAL_LENGTH):
            if random.random() >= 0.1:
                ind[i] = np.random.randint(4)

        return ind

    def get_best_action(self) -> int:
        """
        select the next action from the population
        :return: first action of best individual in the population
        """
        bestAction = self.population[0][0]
        return bestAction
