from gym.envs.registration import register

register(
    id='energy-demand-v0',
    entry_point='gym_energy_demand.envs:EnergyDemandEnv',
    timestep_limit=1000,
)
