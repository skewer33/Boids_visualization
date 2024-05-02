# Boids_visualization
Visualization of the algorithm for describing the behavior of a flock of birds, developed by Craig Reynolds in 1986. One of the basic algorithms of swarm intellegence.
The peculiarity is that by setting the behavior of each member of the swarm separately, we obtain a new property for the entire system.

The algorithm of each birds is based on 4 steps:
1) define your neighbours (function 'neighbours' in 'Rainolds main.py')
2) don't collide (function '_dont_crush' in 'birds.py')
3) fly in the same direction as your neighbors (function '_average_neighbour_speed' in 'birds.py')
4) stay close to your neighbors (function '_geometric_mass_center' in 'birds.py')

The "birds.py" file contains a description of the bird class. The "constants.py" file contains all the modifiable simulation parameters. 
For a quick start, run the file "Raiynolds main.py"
