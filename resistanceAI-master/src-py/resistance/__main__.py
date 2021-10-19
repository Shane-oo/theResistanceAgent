from stupidAgents import StupidAgent
from myAgent22501734 import bayesAgent
from game import Game
allData =[]
spyWinCount = 0
resitanceWinCount=0
for i in range(15000):
        agents = [bayesAgent(name='r1'), 
                bayesAgent(name='r2'),  
                bayesAgent(name='r3'),  
                bayesAgent(name='r4'),  
                bayesAgent(name='r5'),  
                bayesAgent(name='r6'),  
                StupidAgent(name='r7'),  
                StupidAgent(name='r8'),  
                StupidAgent(name='r9'),  
                StupidAgent(name='r10'),  ]
        
        game = Game(agents)
        game.play()
        index = 0
        resistanceData = []
        whoWonValue = 0
        spy_list = []
        for agent in agents:
                # resistance player
                if(index == 0 or index==1 or index==2 or index==3 or index ==4 or index ==5 ) :
                        if(agent.returnValues(index)[0] == 1):
                                resistanceData.append((agent.returnValues(index)[1]))
                        if(agent.whoWon()!=-1):
                                whoWonValue = agent.whoWon()
                else:
                        spy_list = (agent.returnValues(index)[1])
                        print("THE SPY LIST",spy_list)
                        if(spy_list!=-1):
                                spy_list.sort()
                        
                                
               
                
                index +=1
        if (spy_list != [6,7,8,9]):
                print(resistanceData)
                print("OH NO")
                continue
        resistanceData[0][6][10] = 1
        resistanceData[0][7][10] = 1
        resistanceData[0][8][10] = 1
        resistanceData[0][9][10] = 1

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


