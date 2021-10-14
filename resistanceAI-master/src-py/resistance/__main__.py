from random_agent import RandomAgent
from myAgent22501734 import logicalAgent,logicalAgentNoBayes
from game import Game
allData =[]
resistanceWins = 0
spyWins = 0
for i in range(200):
        agents = [logicalAgentNoBayes(name='r1'), 
                logicalAgentNoBayes(name='r2'),  
                logicalAgentNoBayes(name='r3'),  
               logicalAgentNoBayes(name='r4'),  
               logicalAgentNoBayes(name='r5'),  
                 logicalAgentNoBayes(name='r6'),  
                  logicalAgentNoBayes(name='r7'),  
                   logicalAgentNoBayes(name='r8'),  
                  logicalAgentNoBayes(name='r9'),  
                   logicalAgentNoBayes(name='r10'),  
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

        if(whoWonValue == True):
                resistanceWins+=1
                
        else:
                spyWins+=1
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
                        resistanceData[0][i][10] = 1
                i+=1

        for agents in resistanceData[0]:
                allData.append(agents)


print(allData)
print("Resistance Wins Spy Wins Vs Spy Wins",resistanceWins,",",spyWins)
#print(game)


