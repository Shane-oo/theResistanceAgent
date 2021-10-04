from random_agent import RandomAgent
from myAgent22501734 import myAgent
from game import Game

agents = [myAgent(name='r1'), 
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        RandomAgent(name='r4'),  
        RandomAgent(name='r5'),  
        RandomAgent(name='r6'),  
        RandomAgent(name='r7'),
        ]

game = Game(agents)
game.play()
print(game)


