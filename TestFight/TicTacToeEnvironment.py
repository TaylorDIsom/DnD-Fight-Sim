
import numpy as np
import tensorflow as tf
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.environments import utils


'''
This environment is for the game TicTacToe
It starts with an empty 3x3 grid
There are nine actions (1 for each position on the 3x3 grid)
The goal is to get 3 in a row. Observations could be:
    the game grid, the current player's turn
The rewards could be:
    1 for going in a free space
    15 for winning
The reward for draws/cat games could be increased for an agent training for O's
The agent is punished for trying to got in a place that has already been taken:
    -25 for invalid move
I could make 2 agents, train 1 for X's and another one for O's

start off training it to pick a place that hasn't been picked (then go for 3 in a row)
'''
class TicTacToeEnv(py_environment.PyEnvironment):
    def __init__(self):
        # super().__init__()
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=8, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(9,), dtype=np.int32, minimum=-1, maximum=1, name='observation')
        self._reward_spec = array_spec.BoundedArraySpec(
            shape=(1,), dtype=np.int32, minimum=-100, maximum=100, name='reward')
        self._grid = np.array([0,0,0, 0,0,0, 0,0,0])
        self._episode_ended = False
        self.mark = 1
        self.opp_mark = -1
        print("poop")

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def reward_spec(self):
        return self._reward_spec

    def _reset(self):
        self._grid = np.empty(9)
        self._episode_ended = False
        return ts.restart(self._grid)

    def isSpotEmpty(self, spot):
        return self._grid[spot] == 0

    def isGridFull(self):
        return not 0 in self._grid

    def takeOppTurn(self):
        if self.isGridFull():
            return -1
        place = -1
        while place == -1:
            rand = np.random.randint(0, 9)
            if self.isSpotEmpty(rand):
                place = rand
                self._grid[place] = self.opp_mark
                print("opp goes in ", place)
                return place

    def calcReward(self):
        reward = np.count_nonzero(self._grid == self.mark)
        return reward

    def _step(self, action):

        if self._episode_ended:
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()

        #check if the move is valid and reward accordingly
        if 0 <= action <= 8:
            if self.isSpotEmpty(action):
                self._grid = self.mark
                reward = self.calcReward()
                print("agent goes in spot {} for reward {}", action, reward)
            else:       #punish for picking a spot that has been picked
                reward = -10
            self._episode_ended = True
        else:
            raise ValueError('`action` should be 0 - 8.')

        if not self.isGridFull():
            self.takeOppTurn()
        else:
            self._episode_ended = True

        if self._episode_ended:
            return ts.termination(self._grid, reward)
        else:
            return ts.transition(
                self._grid, reward=2, discount=1.0)



print("poop")
env = TicTacToeEnv()
print(env._grid)
utils.validate_py_environment(env, episodes=1)
