from random_agent import RandomAgent
from myAgent22501734 import logicalAgent
from game import Game
allData =[]
spyWinCount = 0
resitanceWinCount=0
for i in range(10000):
        agents = [logicalAgent(name='r1'), 
                logicalAgent(name='r2'),  
                logicalAgent(name='r3'),  
                RandomAgent(name='r4'),  
                RandomAgent(name='r5'),  ]
        
        game = Game(agents)
        game.play()
        index = 0
        resistanceData = []
        whoWonValue = 0
        spy_list = []
        for agent in agents:
                # resistance player
                if(index == 0 or index==1 or index==2):
                        if(agent.returnValues(index)[0] == 1):
                                resistanceData.append((agent.returnValues(index)[1]))
                        if(agent.whoWon()!=-1):
                                whoWonValue = agent.whoWon()
                else:

                        spy_list = (agent.returnValues(index)[1])
                        print("THE SPY LIST",spy_list)
                                
               
                
                index +=1
        if (spy_list != [3,4]):
                print(resistanceData)
                print("OH NO")
                continue
        resistanceData[0][3][10] = 1
        resistanceData[0][4][10] = 1
        if(whoWonValue == True ):
                resitanceWinCount+=1
        else:
                spyWinCount +=1
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
        for  i in range(len(resistanceData)+1):
                if (i in spy_list):
                        resistanceData[0][i][10] = 1

        for agents in resistanceData[0]:
                allData.append(agents)


print(allData)
print( "Resistance Wins Spy Wins Vs Spy Wins",resitanceWinCount,", ",spyWinCount )
#print(game)


