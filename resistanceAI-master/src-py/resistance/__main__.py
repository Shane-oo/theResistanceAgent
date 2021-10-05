from random_agent import RandomAgent
from myAgent22501734 import myAgent
from game import Game

agents = [myAgent(name='r1'), 
        myAgent(name='r2'),  
        myAgent(name='r3'),  
        myAgent(name='r4'),  
        myAgent(name='r5'),  
        myAgent(name='r6'),  
        myAgent(name='r7'),
        myAgent(name='r8'),
        myAgent(name='r9'),
        myAgent(name='r10'),
        ]

game = Game(agents)
game.play()
print(game)


