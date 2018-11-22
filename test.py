import gym
import gym_energy_demand
import numpy as np

env = gym.make('energy-demand-v0')
ob = env.reset()
print(ob)

for _ in range(20):
	print('obs:', ob)
	ac = np.random.uniform(-1., 1., size=(1,))
	ob, rew, done, info = env.step(ac)
	print('ac:', ac)
	print('rew', rew)
	print('done', done)
	print('usage', info['usage curve'])
	print('demand', info['demand curve'])
	print('actions taken', info['demand curve'] - info['usage curve'])
	print('\n')

