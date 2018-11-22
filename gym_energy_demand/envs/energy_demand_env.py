import gym
from gym import error, spaces, util
import numpy as np

class EnergyDemandEnv(gym.Env):
    metadata = {}

    def __init__(self,
                 max_charge_rate=1.0,
                 max_discharge_rate=-1.0,
                 battery_capacity=5.0,
                 load_curve=np.random.normal(loc=10, scale=3, size=2880),
                 cost=1.0,
                 peak_cost=1500.0):
        # define state and action sets here
        assert max_charge_rate >= 0, "maximum charge rate should be non-negative"
        assert max_discharge_rate <= 0, "maximum charge rate should be non-positive"
        assert battery_capacity >= 0, "battery capacity should be non-negative"

        self.action_space = spaces.Box(low=max_discharge_rate, high=max_charge_rate, shape=(1,))

        self._usage_curve = np.clip(load_curve, 0, 2**32) # energy used at each t, non-negative, stays unmodified
        self._demand_curve = np.copy(self._usage_curve) # energy bought from the power plant at each t, modified by agent actions

        self.observation_space = spaces.Box(low=np.zeros(2), high=np.array([2**32, battery_capacity]))
        try:
            self._max_steps = self._usage_curve.shape[0]
        except:
            self._max_steps = len(self._usage_curve)
        self._peak_cost = peak_cost
        self._cost = cost
    
    def step(self, action):
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

        if action < 0: # discharge battery
            if self._battery_charge > 0: 
                discharge = min(abs(action), self._battery_charge)
                self._demand_curve[self._t + 1] -= discharge
                self._battery_charge -= discharge
        elif action > 0: # charge battery
            if self._battery_charge < self._battery_capacity:
                charge = min(action, self._battery_capacity - self._battery_charge)
                self._demand_curve[self._t + 1] += charge
                self._battery_charge += charge
        else: # do nothing
            pass

        reward = self._get_reward()
        self._t += 1
        episode_over = (self._t ==  (self._max_steps - 1))

        if not episode_over:
            ob = np.array([self._usage_curve[self._t], self._battery_charge])
        else:
            ob = np.array([self._usage_curve[self._t - 1], self._battery_charge])

        return ob, reward, episode_over, {}

    def _reset(self):
        self._t = 0
        self._battery_charge = 0
        # do something smarter with load curve here
        self._demand_curve = np.copy(self._usage_curve)
        return np.array([self._usage_curve[self._t], self._battery_charge])
        

    def _render(self, mode='human', close=False):
        raise NotImplementedError()

    def _get_reward(self):
        return -np.max(self._demand_curve[:self.t + 1]) * self.peak_cost # - np.trapz(self._demand_curve[:self.t + 1], dx=15) * self.cost

