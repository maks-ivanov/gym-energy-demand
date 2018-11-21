# OpenAI Gym Environment for Energy Demand Management
This environment is for training agents to manage given energy demand by charging/discharging a battery.

A building at any given point in time has a some load in kW. The way a utility bill is calculated for industrial buildings (Factory, Office, Grocery Store, etc.) is they take the integral of that load curve - how much energy you used. The other portion of the bill comes from taking the peak load over any 15 minute period over an entire month and multiplying that by a very expensive rate in excess of $1000/kW. While we cannot change the integral of the curve - without using less energy - we can however smooth out the curve and shave off the peak with the use of a battery
that we can discharge from during periods of peak demand.