from random_agent import RandomAgent
from myAgent22501734 import myAgent
from game import Game
allData =[]
for i in range(100):
        agents = [myAgent(name='r1'), 
                myAgent(name='r2'),  
                myAgent(name='r3'),  
                myAgent(name='r4'),  
                myAgent(name='r5'),  
                ]
        
        game = Game(agents)
        game.play()
        index = 0
        resistanceData = []
        whoWonValue = 0
        for agent in agents:
                # resistance player
                
                if(agent.returnValues(index)[0] == 1):
                        resistanceData.append((agent.returnValues(index)[1]))
                        
                else:
                        spy_list = (agent.returnValues(index)[1])
                if(agent.whoWon()!=-1):
                        whoWonValue = agent.whoWon()
                
                index +=1

        
        index = 0
        for findNoData in resistanceData[0]:
                if findNoData[0] == 'MyAgent':
                        count = 0
                        for agents in resistanceData[1]:
                                if count == index:
                                        resistanceData[0][index] = resistanceData[1][count]
                                count +=1
                index+=1        

        i = 0
        for agents in resistanceData:
                if (i in spy_list):
                        resistanceData[0][i][5] = 1
                i+=1

        for agents in resistanceData[0]:
                allData.append(agents)


print(allData)
#print(game)


