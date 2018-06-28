# Plants-Kinematics
Python software to model the growth of plants


import plantsKin as pk
from math import pi

A tilted virtual plant is created with the following command

plant = pk.Plant(x0 = [0,0,0],theta0 = pi/2,N = 100,dt=.1,growth = 'no')
plant = pk.Plant(x0 = [0,0,0],theta0 = pi/2,N = 100,dt=.1,growth = 'Apical',growthZone = 1,growthRate = 1)

then a few interaction should be added

plant.addInteractions(name = 'Proprioception' ,intensity=1)
plant.addInteractions(name = 'Tropism' ,intensity=1,direction = 0)