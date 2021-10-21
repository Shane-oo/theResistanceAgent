from random_agent import RandomAgent
from myAgent22501734 import bayesAgent
from generalAgent import generalAgent
from game import Game
allData =[]
allPredPercents = []
resistanceWins = 0
spyWins = 0
for i in range(10000):
        agents = [bayesAgent(name='r1'), 
                bayesAgent(name='r2'), 
                bayesAgent(name='r3'), 
                bayesAgent(name='r4'), 
                bayesAgent(name='r5'),
                bayesAgent(name='r6'),
                bayesAgent(name='r7'),
                bayesAgent(name='r8'),
                bayesAgent(name='r9'),
                bayesAgent(name='r10')
                ]
        
        game = Game(agents)
        game.play()
        index = 0
        resistanceData = []
        whoWonValue = 0
        allPredictions = []
        for agent in agents:
                # resistance player
                
                if(agent.returnValues(index)[0] == 1):
                        resistanceData.append((agent.returnValues(index)[1]))
                        allPredictions.append((agent.returnValues(index)[2]))
                else:
                        spy_list = (agent.returnValues(index)[1])

                if(agent.whoWon()!=-1):
                        whoWonValue = agent.whoWon()
                
                index +=1
        print("THE SPYLIST",spy_list)
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

        
        for  i in range(len(resistanceData)+1):
                if (i in spy_list):
                        resistanceData[0][i][10] = 1
                

        for agents in resistanceData[0]:
                allData.append(agents)
        
        wholeMission = []
        for  i in range(len(agents)-1):
                if(i in spy_list):
                        wholeMission.append(1)
                else:
                        wholeMission.append(0)

        right = 0
        wrong = 0
        for agentsPredictions in allPredictions:
                missionNumber = 0
                for missionPrediction in agentsPredictions:
                        missionNumber+=1
                        if(missionPrediction ==[0]):
                                continue
                        index = 0
                        for prediction in missionPrediction:
                                value = prediction
                                if value == 'MyAgent':
                                        value = 0
                                if(value == wholeMission[index]):
                                        right+=1
                                else:
                                        wrong +=1
                                index+=1
        #print((right/(right+wrong))*100,"%")                        
        allPredPercents.append((right/(right+wrong))*100)




#print(game)

                
print("average for the predictions",sum(allPredPercents) / len(allPredPercents))
#print("allData",allData)
print("Resistance Wins  Vs Spy Wins")
print(resistanceWins,"Vs",spyWins)

