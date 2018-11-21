import gym
from gym import error, spaces, util
import numpy as np

class EnergyDemandEnv(gym.Env):
    metadata = {}

    def __init__(self,
                 max_charge_rate=1.0,
                 max_discharge_rate=-1.0,
                 battery_capacity=5,
                 load_curve=np.random.normal(loc=10, scale=3, size=30)):
        # define state and action sets here
        self.action_space = spaces.Box(low=max_discharge_rate, high=max_charge_rate, shape=(1,))
        self.load_curve = np.clip(load_curve, 0, 2**32) # load is non-negative
        self.observation_space = spaces.Box(low=np.zeros(2), high=np.array([2**32, battery_capacity]), shape=(1,))
    
    def _step(self, action):
        """

        Parameters
        ----------
        action :

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        self._take_action(action)
        self.status = self.env.step()
        reward = self._get_reward()
        ob = self.env.getState()
        episode_over = self.status != hfo_py.IN_GAME
        return ob, reward, episode_over, {}

    def _reset(self):
        pass

    def _render(self, mode='human', close=False):
        raise NotImplementedError()

    def _take_action(self, action):
        pass

    def _get_reward(self):
        """ Reward is given for XY. """
        if self.status == FOOBAR:
            return 1
        elif self.status == ABC:
            return self.somestate ** 2
        else:
            return 0