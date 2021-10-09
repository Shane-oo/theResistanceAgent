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
allData =[]
game = Game(agents)
game.play()
index = 0
resistanceData = []
for agent in agents:
        # resistance player
        
        if(agent.returnValues(index)[0] == 1):
                resistanceData.append((agent.returnValues(index)[1]))
        else:
                spy_list = (agent.returnValues(index)[1])
                
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
print("hi",resistanceData[0])
for agents in resistanceData[0]:
        allData.append(agents)
print(allData)
'''
myAgentIndex = 0



index -=1
for data in resistanceData:

        if data[0] == 'MyAgent':
                
                        while index not in spy_list:
                                index-=1
                        print("yo2",agents[index].returnMyAgentInfo(myAgentIndex))   
                        resistanceData[myAgentIndex] = agents[index-1].returnMyAgentInfo(myAgentIndex)
                
        myAgentIndex+=1
i = 0
for agents in resistanceData:
        if (i in spy_list):
                resistanceData[i][5] = 1
        i+=1
for agents in resistanceData:
        allData.append(agents)
print("all data",allData)
#print(game)

'''
