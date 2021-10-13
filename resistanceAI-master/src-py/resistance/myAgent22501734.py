from agent import Agent
import random


# Global variables
#indexs of varibales in dataset
# Variables after missions
VOTED_FOR_FAILED_MISSION = 0#
WENT_ON_FAILED_MISSION = 1#
PROP_TEAM_FAILED_MISSION = 2#
REJECTED_TEAM_SUCCESFUL_MISSION = 3 #

# Voting variables
VOTED_AGAINST_TEAM_PROPOSAL = 4
VOTED_NO_TEAM_HAS_SUCCESSFUL_MEMBERS = 5
VOTED_FOR_TEAM_HAS_UNSUCCESSFUL_MEMBERS = 6
VOTED_FOR_MISION_NOT_ON = 7

#Proposed team variables
PROPOSED_TEAM_HAS_UNSUCCESSFUL_MEMBERS = 8
PROPOSED_TEAM_THAT_HAVENT_BEEN_ON_MISSIONS = 9

IS_SPY = 10

# Logical playing Agent
class logicalAgent(Agent):        


    '''My agent in the game The Resistance'''
    def __init__(self, name='Rando'):
        '''
        Initialises the agent.
        Nothing to do here.
        '''
        #initialise class attributes
        self.name = name
        self.missionNum = 1
        self.spyWins = 0
        self.resistanceWins = 0
        self.roundCount = 1
        
       #Resistance Agent variables
        self.resistanceData = []
        self.failedMissions = []
        self.propFailedMissions = []
        self.wentOnSuccessfulMissions = []
        self.wentOnFailedMissions = []
        self.outedSpies = []
        self.predictedSpies = []

        
        

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        self.number_of_players = number_of_players
        self.player_number = player_number
        
        self.spy_list = spy_list
        print("MyAgent playernum",self.player_number)
        if(not self.is_spy()):
            resistanceTable = []
            for i in range(number_of_players):
                
                if i == player_number:
                    resistanceTable.append(["MyAgent"])
                else:
                    resistanceTable.append([0,0,0,0,0,0,0,0,0,0,0])
                    
            self.resistanceData = resistanceTable


            print(self.resistanceData)
        else:
            print("Im a spy")

    def is_spy(self):
       
        '''
        returns True iff the agent is a spy
        '''
        return self.player_number in self.spy_list

    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        team = []
        if(not self.is_spy()):
            # For the first mission as resistance
            # I want my agent to pick itself and pick at random the team members for mission
            if(self.missionNum ==1):
                team.append(self.player_number)
                while len(team)<team_size:
                    agent = random.randrange(self.number_of_players)
                    if agent not in team:
                        team.append(agent)
            else:
                team.append(self.player_number)
                # pick members that are the most trusting
                for trustingAgents in self.wentOnSuccessfulMissions:
                    if(len(team)<team_size):
                        agent = random.choice(self.wentOnSuccessfulMissions)
                        if agent not in team and agent not in self.outedSpies :
                            if(len(self.predictedSpies)!=0):
                                print("agent",agent,"predictedspies",self.predictedSpies)
                                if(self.predictedSpies[agent]!=1):
                                    team.append(agent)
                            else:
                                team.append(agent)
                            
                # if still need team members
                if(len(team)<team_size):
                    # pick members that have not failed any missions yet
                    for i in range(self.number_of_players):
                        if((len(team)<team_size) and i not in self.wentOnFailedMissions):
                            if i not in team and i not in self.outedSpies:
                                
                                if(len(self.predictedSpies)!=0):
                                    
                                    if(self.predictedSpies[i]!=1):
                                        team.append(i)
                                else:
                                    team.append(i)
                        

                    
                    # pick the members not predicted to be spies
                    for i in range(self.number_of_players):
                        if len(team)<team_size:
                            if i not in team:
                                if(len(self.predictedSpies)!=0):
                                    if(self.predictedSpies[i]!=1):
                                        team.append(i)

                    # last resort is to pick from random potentially picking member that potentially went on failed mission
                    # but do not pick any agents that have been found to be spies
                    while len(team)<team_size:
                        agent = random.randrange(self.number_of_players)
                        print("stuck")
                        print("the team",team,"the agent",agent,"the outed spies",self.outedSpies,"the predicted spies",self.predictedSpies)
                        if agent not in team and agent not in self.outedSpies:
                            continue
                        else:
                            team.append(agent)

        ##################### Spy Moves ###############################
        else:
            if(self.missionNum ==1 and self.missionNum !=4):
                team.append(self.player_number)
                # put self on team with only other reistance members
                while len(team)<team_size:
                    agent = random.randrange(self.number_of_players)
                    if ((agent not in team) and agent not in self.spy_list):
                        team.append(agent)
            else:# mission 4
                team.append(self.player_number)
                # need to win mission 4 and 5 to win game
                if(self.spyWins == 1):
                   
                    # add just 1 more spy to team spy to team
                    if(betrayals_required == 2):
                        while len(team)<team_size:
                            spy_count = sum(el in self.spy_list for el in mission)
                            if(spy_count==1):
                                agent = random.choice(self.spy_list)
                            else:
                                
                                agent = random.randrange(self.number_of_players)
                            if (agent not in team):
                                
                                team.append(agent)
                    
                else:
                    while len(team)<team_size:
                        
                        agent = random.randrange(self.number_of_players)
                        if ((agent not in team) and agent not in self.spy_list):
                        
                            team.append(agent)
                
        return team        

    def vote(self, mission, proposer):
        print("ROUND COUNT",self.roundCount)
        print("The proposer = ",proposer)
        
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        #always return True if agent is the proposer
        if(proposer == self.player_number):
            print("agent is proposer return True")
            return True

        ##################### Spy Moves ###############################
        if(self.is_spy()):
            if(self.missionNum ==1 ):
                # Spies will never sabotage first mission so does not matter who goes
                return True
            elif(self.missionNum != 1 and self.missionNum !=4):
                    # count amount of spies in mission
                    spy_count = sum(el in self.spy_list for el in mission)
                    # approve missions that has spies on it but not if mission is full of spies
                    if(len(mission) != spy_count and spy_count!=0):
                        return True
                    else:   
                        return False
            else:# mission 4
                # need to win mission 4 and 5 to win game
                if(self.spyWins == 1 ):
                    spy_count = sum(el in self.spy_list for el in mission)
                    if(self.number_of_players>=7 and spy_count<2):
                        # need a mission with more than 2 spies
                        return False
                    elif(self.number_of_players<7 and spy_count ==1):
                        return True
                    else:
                        # Too many spies in team or no spies at all
                        return False
                else:
                    # dont care about mission 4 will go for mission 5 win
                    return True
        else:
            if(self.missionNum ==1 ):
                # no info to go off of for mission 1
                return True
            # should vote yes if in last round to avoid a mission fail     
            if(self.roundCount == 5):
                return True
            outedSpiesCount = sum(el in self.outedSpies for el in mission)
            
            if(outedSpiesCount!=0):
                return False
            # Dont vote for mission if contains a predicted spy
            index = 0
            sussSpiesArr = []
            for sussSpies in self.predictedSpies:
                if sussSpies == 1:
                    sussSpiesArr.append(index)
                index+=1

            predictedSpiesCount = sum(el in  sussSpiesArr for el in mission)
            print("1 ",self.predictedSpies," ", predictedSpiesCount)
            if(predictedSpiesCount!=0):
                return False
            trustedAgentsCount = sum(el in self.wentOnSuccessfulMissions for el in mission)
            # All trustworthy members on team
            if(trustedAgentsCount == len(mission)):
                return True
            failedAgentsCount = sum(el in self.wentOnFailedMissions for el in mission)

            if(failedAgentsCount >0):
               
                return False

                
            # If there are some trust worthy members and members yet to be on mission return True
            if(trustedAgentsCount>0 and failedAgentsCount ==0):
                return True
            # No info about anyone on the team
            if(trustedAgentsCount == 0 and failedAgentsCount == 0): 
                # return true as at least you know there is one resistance member
                if(self.player_number in mission):
                    return True
                else:
                    return False

    def vote_outcome(self, mission, proposer, votes):
        self.agentsWhoVoted = []
        self.agentsWhoVoted = votes
        self.roundCount +=1
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        '''
        "votes just returns a list of players that voted for the mission to go ahead
        it just a list of positive voters"
        '''
        if(not self.is_spy()):
            if(proposer != self.player_number):
                # if proposer proposed a mission that contains no succesful mission members
                if(len(self.wentOnSuccessfulMissions)!=0):
                    trustingMembersCount = sum(el in self.wentOnSuccessfulMissions for el in mission)
                    if(trustingMembersCount == 0):
                        self.resistanceData[proposer][PROPOSED_TEAM_THAT_HAVENT_BEEN_ON_MISSIONS] += 2*(self.missionNum)
                # if proposer proposed a mission that contains failed mission members
                if(len(self.wentOnFailedMissions)!=0):
                    unTrustingMembersCount = sum(el in self.wentOnFailedMissions for el in mission)
                    if(unTrustingMembersCount != 0):
                        self.resistanceData[proposer][PROPOSED_TEAM_HAS_UNSUCCESSFUL_MEMBERS] += 4*(self.missionNum*unTrustingMembersCount)
                        
            
            for i in range(self.number_of_players):
                # if agent votes no for mission its suss
                if i == self.player_number:
                        continue
                if i not in votes:
                    self.resistanceData[i][VOTED_AGAINST_TEAM_PROPOSAL] += self.missionNum
                    # If they say not to teams that contatin successful mission members its suss
                    SuccessfulMissionsMembers = sum(el in self.wentOnSuccessfulMissions for el in mission)
                    self.resistanceData[i][VOTED_NO_TEAM_HAS_SUCCESSFUL_MEMBERS] += 3*(self.missionNum*SuccessfulMissionsMembers)

                if i in votes:
                    # If they vote yes for a mission that contains members that prevousily failed missions its suss
                    failedPriorMissionsMembers = sum(el in self.wentOnFailedMissions for el in mission)
                    self.resistanceData[i][VOTED_FOR_TEAM_HAS_UNSUCCESSFUL_MEMBERS ] += 4*(self.missionNum*failedPriorMissionsMembers)
                
                if (i in votes and i not in mission):
                    # voted for a mission they are not on
                    self.resistanceData[i][VOTED_FOR_MISION_NOT_ON] += self.missionNum
            if(self.spyWins >= 2 or self.missionNum>=3):
                self.predictedSpies = naiveBayesClassifier(self.resistanceData)
                print("2 ",self.predictedSpies)
        pass

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        if(self.missionNum ==1):
            return False
        elif(self.missionNum == 5):
            return True
        elif(self.missionNum != 1 and self.missionNum !=4):
            spy_count = sum(el in self.spy_list for el in mission)
            # Agent is the only spy
            if(spy_count ==1):
                return True
            elif(spy_count>1):
                # 75 chance of betrayal
                probability = 0.75
                return random.random() <= probability
            else:
                # 50% chance of betrayal
                probability = 0.50
                return random.random() <= probability
        else:
            if(self.spyWins ==1):
                spy_count = sum(el in self.spy_list for el in mission)
                if(self.number_of_players>=7 and spy_count<2):
                        # need a mission with more than 2 spies
                    return False
                elif(self.number_of_players<7 and spy_count == 1):
                        # only need 1 betray
                    return True
                elif(self.number_of_players>=7 and spy_count ==2):
                        # need both spies to betray
                    return True
                elif(self.number_of_players>=7 and spy_count >2):
                    #Hope that random choices you get at least 2 spies fail but also not exposing themself
                    # This situation is difficult since the spies can not communicate
                    # assume spies do a 50/50 
                    probability = 0.5
                    return random.random() <= probability
            else:
                    # dont care about mission 4 will go for mission 5 win
                    return False

        #if self.is_spy():
         #   return random.random()<0.3

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        self.roundCount = 1
        '''
        mission is a list of agents that were sent on the mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        if(not self.is_spy()):
            if(mission_success):
                self.resistanceWins += 1
                for agents in mission:
                    if agents == self.player_number:
                        continue
                    self.wentOnSuccessfulMissions.append(agents)
                for i in range(self.number_of_players):
    
                    if i not in self.agentsWhoVoted:
                        if(i ==self.player_number):
                            continue
                        # Increases sussness if agent did not want a successful mission to happen
                        self.resistanceData[i][REJECTED_TEAM_SUCCESFUL_MISSION] += 2*(self.missionNum)
           
            # failed mission
            else:
                self.spyWins += 1
                for agent in self.agentsWhoVoted:
                    if(agent is not self.player_number):
                        # Increase sussness if agent most liekly voted knowing mission would fail
                        self.resistanceData[agent][VOTED_FOR_FAILED_MISSION]+= 2*(self.missionNum)
                # Increment the amounts that add to untrustworthyness
                if(proposer is not self.player_number):

                    self.propFailedMissions.append(proposer)
                    propFailedMissionsCount = self.propFailedMissions.count(proposer)
                    if(propFailedMissionsCount == 0):
                        propFailedMissionsCount = 1
                    # increment by one or by how many times agent has proposed failed mission    
                    self.resistanceData[proposer][PROP_TEAM_FAILED_MISSION] += 3*propFailedMissionsCount*self.missionNum
                    # If proposer was in the mission that failed
                    if(proposer in mission):
                        self.resistanceData[proposer][PROP_TEAM_FAILED_MISSION] += 3*self.missionNum

                for agent in mission:
                    # check for outed spies
                    self.stupid_spies_check(agent,proposer,mission,betrayals)
                    if(agent is not self.player_number):
                        self.wentOnFailedMissions.append(agent)
                        # remove agents from wentOnSuccessfulMissions if exist in wentOnFailedMissions
                        # as they are now untrustworthy
                        if (agent in self.wentOnSuccessfulMissions):
                            self.wentOnSuccessfulMissions.remove(agent)
                        self.failedMissions.append(agent)
                        failedMissionsCount = self.failedMissions.count(agent)
                        if(failedMissionsCount == 0):
                            failedMissionsCount = 1
                        self.resistanceData[agent][WENT_ON_FAILED_MISSION] += failedMissionsCount*self.missionNum*(betrayals/len(mission))

            # Bayes Classifier 
            # Gather what the predicted spies could be (For effiency Im only going get predicted spies when spyWins ==2)
            if(self.spyWins >= 2 or self.missionNum>=3):
                self.predictedSpies = naiveBayesClassifier(self.resistanceData)
                print("3 ",self.predictedSpies)
            #naiveBayesClassifier(self.resistanceData)
        

        self.missionNum +=1
        pass

    def round_outcome(self, rounds_complete, missions_failed):
        self.roundCount = 1
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the number of missions (0-3) that have failed.
        '''
        #nothing to do here
        
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        #nothing to do here
        pass

    
    def stupid_spies_check(self,agent,proposer,mission,betrayals):
        '''
        Check for spies that have completely outed themselves on failed missions to The Resistance
        '''

        # spy stupidly outed themself on mission with me
        if(self.player_number in mission):

            for stupidSpies in mission:

                if stupidSpies == self.player_number:
                    continue
                if stupidSpies in self.outedSpies:
                    continue
                
                if(len(mission)== 2 and betrayals == 1):
                    
                    self.outedSpies.append(stupidSpies)
                if(len(mission)== 3 and betrayals ==2 ):
                    
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 4 and betrayals == 3):
                    
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 5 and betrayals ==4):
                    
                    self.outedSpies.append(stupidSpies)
        # spies outed eachother
        else:
            for stupidSpies in mission:
                if(len(mission) == 2 and betrayals ==2 ):
                    
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 3 and betrayals ==3 ):
                    
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 4 and betrayals ==4 ):
                    
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 5 and betrayals ==5 ):
                    
                    self.outedSpies.append(stupidSpies)



    # Helper functions for data collection
    def returnValues(self,agentIndex):
        if(self.is_spy()):
            return (-1,self.spy_list)
        else:
            return (1,self.resistanceData)
    def returnMyAgentInfo(self,myAgentIndex):
        
        
        return self.resistanceData[myAgentIndex]
    def whoWon(self):
        
        if(self.spyWins > self.resistanceWins):
            return False
        elif(self.resistanceWins >self.spyWins):
            return True
        else:
            return -1


################### Naive Bayes Classifier ####################


# Make Predictions with Naive Bayes On The Iris Dataset

from math import sqrt
from math import exp
from math import pi
trainingDataRandomSpy = [[0, 1.6666666666666665, 0, 14, 12, 48, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 6, 3, 12, 0, 12, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 16, 10, 27, 0, 0, 0, 0, 0], [0, 0, 0, 16, 10, 42, 0, 7, 0, 0, 1], [0, 0, 0, 20, 12, 51, 0, 1, 0, 0, 1], [2, 3.833333333333333, 6, 0, 24, 75, 40, 0, 32, 0, 0], [22, 0.6666666666666666, 0, 8, 16, 60, 84, 9, 48, 0, 0], [6, 8.666666666666666, 12, 8, 23, 45, 40, 1, 40, 0, 0], [22, 8.666666666666666, 63, 0, 12, 60, 116, 9, 52, 0, 1], [18, 0.5, 0, 0, 6, 0, 172, 24, 32, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 4, 0, 0, 0], [10, 1.6666666666666665, 0, 4, 5, 15, 0, 1, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 16, 16, 72, 0, 2, 0, 0, 1], [10, 1.6666666666666665, 0, 10, 8, 24, 0, 1, 0, 0, 1], [10, 0, 0, 10, 5, 24, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 6, 3, 9, 0, 12, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [0, 0, 0, 18, 12, 51, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 12, 9, 39, 0, 9, 0, 0, 1], [0, 0, 0, 20, 13, 69, 0, 1, 0, 0, 1], [6, 0, 0, 8, 4, 12, 20, 3, 20, 0, 0], [6, 0, 0, 8, 9, 42, 0, 3, 0, 0, 0], [0, 1.5, 0, 10, 16, 63, 16, 1, 0, 0, 0], [6, 1.5, 18, 4, 10, 45, 16, 10, 0, 0, 1], [6, 0, 0, 16, 11, 30, 36, 12, 16, 0, 1], [6, 0, 0, 8, 8, 36, 0, 3, 0, 0, 0], [0, 0, 0, 2, 4, 9, 16, 0, 0, 0, 0], [6, 1.5, 18, 0, 4, 12, 36, 1, 0, 0, 0], [6, 1.5, 0, 14, 7, 36, 16, 4, 16, 0, 1], [6, 0, 0, 16, 12, 48, 0, 7, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 0, 0, 0, 1], [0, 0, 0, 12, 6, 15, 0, 9, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 18, 9, 39, 0, 6, 0, 0, 1], [0, 0, 0, 20, 10, 51, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 22, 11, 60, 0, 4, 0, 0, 1], [0, 0, 0, 10, 5, 24, 0, 10, 0, 0, 1], [2, 3.833333333333333, 6, 8, 29, 69, 84, 0, 64, 0, 0], [0, 0.6666666666666666, 0, 0, 36, 75, 44, 3, 52, 0, 0], [16, 3.9999999999999996, 57, 8, 32, 72, 52, 1, 52, 0, 0], [16, 3.9999999999999996, 0, 6, 24, 60, 128, 5, 56, 8, 1], [16, 0.5, 0, 0, 15, 30, 148, 27, 44, 0, 1], [8, 3.5, 33, 8, 30, 75, 104, 0, 64, 0, 0], [6, 0.6666666666666666, 12, 0, 32, 105, 72, 1, 72, 0, 0], [12, 0.6666666666666666, 0, 0, 21, 75, 148, 7, 52, 0, 0], [0, 0.5, 0, 0, 17, 30, 204, 27, 52, 0, 1], [12, 3.6666666666666665, 0, 10, 26, 120, 120, 5, 64, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 4, 7, 36, 0, 3, 0, 0, 0], [0, 0, 0, 20, 15, 75, 0, 1, 0, 0, 1], [0, 0, 0, 18, 14, 69, 0, 6, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 16, 8, 33, 0, 7, 0, 0, 1], [0, 0, 0, 2, 1, 0, 0, 14, 0, 0, 1], [12, 3.833333333333333, 51, 0, 39, 99, 104, 0, 84, 0, 0], [12, 0.6666666666666666, 0, 6, 32, 60, 168, 10, 52, 0, 0], [16, 3.9999999999999996, 12, 8, 41, 84, 92, 1, 52, 0, 0], [16, 3.9999999999999996, 0, 6, 29, 45, 200, 5, 96, 8, 1], [16, 0.5, 0, 8, 31, 39, 172, 25, 84, 0, 1], [0, 0, 0, 2, 6, 30, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 15, 81, 0, 1, 0, 0, 1], [0, 0, 0, 28, 19, 93, 0, 1, 0, 0, 1], [0, 0, 0, 10, 10, 42, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 20, 15, 75, 0, 1, 0, 0, 1], [0, 0, 0, 20, 15, 57, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 0, 0, 6, 3, 12, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 16, 13, 48, 0, 2, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [4, 0.6666666666666666, 0, 18, 28, 102, 32, 3, 32, 0, 0], [4, 0.6666666666666666, 12, 8, 31, 99, 32, 1, 32, 0, 0], [0, 0, 0, 6, 22, 42, 76, 1, 28, 0, 0], [4, 0, 0, 2, 19, 90, 72, 23, 32, 0, 1], [4, 0.6666666666666666, 0, 16, 27, 90, 80, 4, 64, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 14, 0, 0, 1], [0, 0, 0, 22, 11, 54, 0, 4, 0, 0, 1], [10, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [10, 1.6666666666666665, 0, 14, 7, 30, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 10, 5, 24, 0, 10, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 16, 13, 48, 0, 0, 0, 0, 0], [10, 0, 0, 6, 3, 12, 0, 12, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [6, 1.5, 0, 0, 0, 0, 68, 0, 16, 0, 0], [6, 0, 0, 10, 13, 78, 0, 4, 0, 4, 0], [6, 0, 0, 10, 16, 81, 20, 3, 20, 0, 0], [6, 1.5, 18, 14, 10, 45, 48, 12, 0, 0, 1], [6, 0, 0, 4, 13, 63, 36, 13, 16, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 22, 11, 60, 0, 4, 0, 0, 1], [0, 0, 0, 10, 5, 15, 0, 10, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 14, 0, 0, 1], [0, 0, 0, 18, 9, 54, 0, 6, 0, 0, 1], [6, 1.5, 0, 20, 30, 174, 40, 5, 36, 0, 0], [6, 0, 0, 0, 28, 153, 36, 3, 36, 0, 0], [6, 0, 0, 8, 27, 147, 40, 4, 20, 0, 0], [6, 1.5, 18, 14, 24, 144, 68, 13, 20, 0, 1], [6, 0, 0, 0, 26, 141, 52, 19, 36, 0, 1], [6, 0, 0, 8, 8, 24, 20, 3, 20, 0, 0], [6, 0, 0, 18, 13, 78, 0, 4, 0, 0, 0], [6, 1.5, 18, 0, 0, 0, 52, 3, 0, 0, 0], [6, 0, 0, 2, 5, 12, 36, 14, 16, 0, 1], [0, 1.5, 0, 2, 4, 9, 52, 13, 16, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 10, 5, 30, 0, 10, 0, 0, 1], [0, 0, 0, 18, 9, 39, 0, 6, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 12, 6, 30, 0, 9, 0, 0, 1], [0, 0, 0, 12, 6, 21, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 20, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 20, 10, 54, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 0, 20, 10, 39, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [0, 0, 0, 2, 6, 15, 0, 9, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [6, 1.5, 0, 0, 0, 0, 36, 0, 20, 0, 0], [6, 0, 0, 18, 9, 54, 0, 3, 0, 0, 0], [6, 0, 0, 8, 6, 30, 20, 4, 0, 0, 0], [6, 1.5, 18, 14, 9, 42, 16, 5, 0, 0, 1], [0, 0, 0, 6, 8, 21, 36, 9, 16, 0, 1], [6, 0, 0, 2, 13, 51, 36, 3, 16, 0, 0], [6, 0, 0, 18, 13, 78, 0, 3, 0, 0, 0], [6, 1.5, 0, 0, 0, 0, 72, 1, 20, 0, 0], [6, 1.5, 18, 14, 15, 75, 32, 9, 0, 0, 1], [6, 0, 0, 10, 17, 63, 20, 10, 16, 0, 1], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 14, 7, 33, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 2, 6, 15, 0, 9, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [2, 0.5, 6, 0, 38, 150, 172, 0, 116, 0, 0], [6, 0.6666666666666666, 12, 10, 48, 153, 44, 1, 44, 0, 0], [6, 0.6666666666666666, 0, 10, 36, 111, 156, 4, 112, 0, 0], [6, 0.5, 0, 8, 27, 84, 228, 30, 84, 0, 1], [0, 0.6666666666666666, 0, 14, 29, 66, 208, 21, 84, 0, 1], [4, 0.6666666666666666, 0, 0, 45, 204, 48, 0, 48, 0, 0], [4, 0.6666666666666666, 12, 6, 39, 69, 36, 10, 36, 0, 0], [0, 0, 0, 12, 37, 201, 112, 6, 48, 0, 0], [0, 0, 0, 8, 32, 174, 124, 23, 48, 0, 1], [4, 0.6666666666666666, 0, 6, 24, 90, 180, 21, 96, 0, 1], [0, 0, 0, 14, 7, 18, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 6, 3, 9, 0, 12, 0, 0, 1], [12, 1.8333333333333333, 6, 0, 29, 105, 148, 3, 84, 0, 0], [8, 0, 0, 8, 36, 90, 76, 4, 32, 0, 0], [10, 3.6666666666666665, 0, 10, 26, 90, 200, 6, 60, 0, 0], [12, 3.6666666666666665, 39, 10, 31, 120, 148, 12, 72, 0, 1], [10, 0.5, 0, 8, 32, 45, 164, 23, 84, 0, 1], [14, 0.6666666666666666, 0, 0, 21, 36, 28, 8, 28, 0, 0], [14, 3.9999999999999996, 57, 8, 21, 60, 60, 1, 32, 0, 0], [10, 1.6666666666666665, 0, 2, 21, 48, 40, 3, 28, 0, 0], [14, 1.6666666666666665, 0, 6, 12, 0, 48, 11, 0, 0, 1], [14, 0.6666666666666666, 0, 14, 27, 36, 16, 9, 28, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 1.6666666666666665, 0, 16, 13, 63, 0, 0, 0, 0, 0], [0, 0, 0, 10, 10, 54, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [0, 0, 0, 18, 12, 60, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 16, 11, 39, 0, 7, 0, 0, 1], [0, 0, 0, 20, 13, 63, 0, 1, 0, 0, 1], [10, 0.6666666666666666, 0, 8, 12, 0, 84, 3, 72, 0, 0], [10, 1.5, 18, 18, 23, 33, 0, 2, 0, 0, 0], [10, 0.6666666666666666, 0, 2, 12, 21, 104, 6, 32, 0, 0], [10, 0.6666666666666666, 12, 0, 10, 30, 136, 17, 32, 4, 1], [0, 1.5, 0, 0, 19, 39, 104, 9, 32, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 14, 7, 42, 0, 8, 0, 0, 1], [0, 0, 0, 28, 14, 78, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0], [0, 0, 0, 8, 4, 36, 0, 4, 0, 0, 0], [0, 0, 0, 20, 10, 39, 0, 0, 0, 0, 1], [0, 0, 0, 20, 10, 66, 0, 5, 0, 0, 1], [6, 0, 0, 8, 9, 39, 0, 3, 0, 0, 0], [0, 1.6666666666666665, 0, 2, 9, 24, 0, 0, 0, 0, 0], [16, 4.833333333333333, 18, 0, 0, 0, 36, 1, 0, 0, 0], [16, 1.5, 0, 4, 2, 6, 0, 9, 0, 0, 1], [16, 1.6666666666666665, 30, 4, 2, 6, 0, 8, 0, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 0, 10, 60, 0, 12, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 15, 81, 0, 1, 0, 0, 1], [0, 0, 0, 10, 20, 102, 0, 5, 0, 0, 1], [14, 0.6666666666666666, 0, 8, 22, 42, 52, 8, 32, 0, 0], [14, 3.9999999999999996, 57, 8, 30, 96, 52, 1, 52, 0, 0], [4, 1.6666666666666665, 0, 0, 11, 30, 112, 10, 28, 0, 0], [14, 3.9999999999999996, 0, 6, 22, 60, 80, 4, 44, 8, 1], [14, 0, 0, 0, 17, 72, 88, 24, 32, 0, 1], [6, 0, 0, 8, 9, 39, 0, 3, 0, 0, 0], [6, 0, 0, 2, 6, 30, 36, 3, 0, 4, 0], [6, 1.5, 18, 0, 5, 30, 36, 1, 0, 0, 0], [6, 0, 0, 10, 10, 60, 16, 10, 16, 0, 1], [6, 1.5, 0, 14, 7, 30, 56, 4, 40, 0, 1], [0, 0, 0, 6, 8, 21, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 16, 13, 48, 0, 2, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [0, 0, 0, 10, 10, 39, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 16, 8, 33, 0, 7, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [10, 3.1666666666666665, 42, 0, 43, 72, 144, 0, 120, 0, 0], [6, 3.333333333333333, 12, 0, 43, 48, 92, 1, 52, 0, 0], [6, 0.6666666666666666, 0, 0, 36, 36, 156, 9, 104, 0, 0], [10, 3.333333333333333, 0, 0, 29, 24, 228, 21, 84, 0, 1], [12, 0.5, 0, 6, 28, 24, 208, 26, 84, 0, 1], [4, 0, 0, 2, 22, 78, 20, 2, 20, 0, 0], [4, 0.6666666666666666, 0, 0, 20, 120, 48, 0, 36, 0, 0], [4, 0.6666666666666666, 0, 14, 22, 66, 20, 6, 20, 0, 0], [4, 0, 0, 12, 17, 78, 60, 20, 20, 0, 1], [4, 0.6666666666666666, 12, 6, 19, 57, 40, 15, 20, 4, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 14, 0, 0, 1], [0, 0, 0, 6, 3, 6, 0, 12, 0, 0, 1], [6, 0, 0, 8, 4, 24, 0, 3, 0, 0, 0], [0, 0, 0, 14, 13, 36, 20, 0, 0, 0, 0], [6, 1.5, 0, 0, 0, 0, 36, 1, 0, 0, 0], [6, 1.5, 18, 14, 10, 45, 16, 5, 0, 0, 1], [6, 0, 0, 10, 8, 39, 16, 10, 16, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 6, 3, 12, 0, 3, 0, 0, 0], [0, 0, 0, 16, 8, 39, 0, 3, 0, 8, 1], [0, 0, 0, 16, 8, 9, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 4, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 8, 7, 18, 0, 5, 0, 0, 0], [10, 0, 0, 2, 4, 9, 0, 14, 0, 0, 1], [10, 1.6666666666666665, 0, 10, 8, 24, 0, 1, 0, 0, 1], [10, 1.6666666666666665, 0, 8, 4, 24, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 0, 0, 8, 4, 24, 0, 11, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 24, 0, 5, 0, 0, 1], [6, 0, 0, 8, 8, 36, 0, 3, 0, 0, 0], [6, 0, 0, 16, 12, 42, 32, 3, 0, 4, 0], [6, 1.5, 18, 8, 4, 12, 36, 1, 0, 0, 0], [6, 0, 0, 0, 4, 12, 52, 15, 16, 0, 1], [6, 1.5, 0, 14, 7, 30, 48, 4, 32, 0, 1], [0, 0, 0, 2, 11, 42, 0, 0, 0, 0, 0], [6, 0, 0, 8, 9, 54, 0, 3, 0, 0, 0], [6, 1.5, 0, 0, 0, 0, 36, 6, 0, 0, 0], [6, 1.5, 18, 4, 9, 54, 0, 10, 0, 6, 1], [6, 0, 0, 6, 10, 54, 0, 7, 0, 0, 1], [6, 1.5, 0, 0, 0, 0, 56, 0, 16, 0, 0], [0, 0, 0, 0, 7, 9, 0, 1, 0, 4, 0], [6, 0, 0, 8, 9, 54, 0, 4, 0, 4, 0], [6, 0, 0, 20, 19, 84, 0, 5, 0, 4, 1], [6, 1.5, 18, 14, 16, 60, 0, 4, 0, 0, 1], [8, 2.5, 33, 8, 25, 0, 56, 0, 36, 0, 0], [10, 0.6666666666666666, 0, 0, 13, 0, 168, 3, 64, 0, 0], [6, 2.6666666666666665, 12, 0, 27, 0, 60, 1, 60, 0, 0], [6, 0.5, 0, 8, 28, 0, 48, 8, 48, 0, 1], [12, 2.6666666666666665, 0, 0, 17, 0, 124, 9, 36, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 4, 0], [0, 0, 0, 12, 11, 45, 0, 4, 0, 0, 0], [10, 0, 0, 8, 4, 9, 0, 11, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 18, 12, 72, 0, 1, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 10, 8, 42, 0, 10, 0, 0, 1], [0, 0, 0, 20, 13, 57, 0, 0, 0, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 4, 0, 0, 0], [10, 0, 0, 12, 6, 15, 0, 9, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 12, 6, 24, 0, 9, 0, 0, 1], [0, 0, 0, 6, 3, 6, 0, 12, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 20, 12, 60, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 8, 6, 15, 0, 11, 0, 0, 1], [0, 0, 0, 20, 12, 51, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 6, 3, 12, 0, 7, 0, 0, 0], [0, 0, 0, 20, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 14, 7, 21, 0, 8, 0, 0, 1], [0, 0, 0, 20, 10, 33, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 10, 5, 12, 0, 10, 0, 0, 1], [10, 1.6666666666666665, 0, 4, 2, 12, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 14, 12, 48, 0, 3, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [6, 0, 0, 8, 8, 48, 0, 3, 0, 0, 0], [6, 0, 0, 18, 13, 54, 0, 4, 0, 4, 0], [6, 1.5, 18, 0, 0, 0, 52, 1, 0, 0, 0], [0, 1.5, 0, 0, 3, 18, 52, 15, 16, 0, 1], [0, 0, 0, 12, 13, 60, 16, 6, 16, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 6, 0], [0, 0, 0, 26, 13, 54, 0, 0, 0, 0, 1], [0, 0, 0, 8, 4, 0, 0, 11, 0, 0, 1], [12, 6.333333333333333, 6, 0, 31, 120, 96, 0, 48, 0, 0], [8, 0.6666666666666666, 0, 8, 34, 75, 64, 4, 32, 0, 0], [10, 0, 0, 18, 40, 120, 64, 8, 40, 0, 0], [12, 0.5, 0, 0, 28, 90, 108, 24, 40, 0, 1], [12, 3.6666666666666665, 39, 10, 36, 120, 88, 5, 72, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 8, 9, 42, 0, 3, 0, 0, 0], [0, 0, 0, 20, 15, 81, 0, 1, 0, 0, 1], [0, 0, 0, 2, 6, 30, 0, 14, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 10, 5, 24, 0, 10, 0, 0, 1], [6, 0, 0, 0, 4, 24, 0, 3, 0, 0, 0], [6, 0, 0, 0, 4, 24, 0, 4, 0, 0, 0], [6, 1.5, 0, 20, 17, 75, 0, 0, 0, 0, 0], [6, 1.5, 18, 4, 5, 21, 16, 14, 0, 0, 1], [0, 0, 0, 10, 15, 54, 0, 2, 16, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 14, 7, 21, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 24, 12, 48, 0, 3, 0, 0, 1], [0, 1.6666666666666665, 0, 0, 5, 15, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [0, 0, 0, 18, 14, 63, 0, 1, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 24, 0, 5, 0, 0, 1], [0, 0, 0, 0, 25, 117, 0, 0, 0, 0, 0], [6, 0, 0, 8, 19, 99, 0, 3, 0, 0, 0], [6, 1.5, 0, 0, 5, 15, 96, 1, 20, 0, 0], [6, 1.5, 18, 4, 24, 144, 20, 5, 20, 6, 1], [0, 0, 0, 14, 32, 168, 20, 5, 0, 0, 1], [6, 1.5, 0, 0, 0, 0, 36, 0, 20, 0, 0], [6, 0, 0, 18, 9, 54, 0, 4, 0, 4, 0], [6, 0, 0, 2, 3, 0, 0, 3, 0, 4, 0], [6, 1.5, 18, 14, 9, 30, 0, 4, 0, 0, 1], [0, 0, 0, 0, 5, 9, 0, 12, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 8, 4, 36, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 0, 0, 0, 1], [0, 0, 0, 26, 13, 75, 0, 2, 0, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 7, 0, 0, 0], [10, 1.6666666666666665, 0, 14, 12, 54, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 10, 51, 0, 1, 0, 0, 1], [10, 0, 0, 10, 10, 42, 0, 10, 0, 0, 1], [4, 0.6666666666666666, 0, 8, 23, 57, 12, 0, 12, 0, 0], [4, 3.9999999999999996, 12, 6, 22, 60, 16, 1, 16, 0, 0], [10, 1.6666666666666665, 0, 0, 11, 12, 52, 1, 32, 0, 0], [14, 3.9999999999999996, 30, 6, 14, 30, 32, 4, 32, 0, 1], [14, 0, 0, 2, 7, 0, 64, 18, 12, 0, 1], [10, 0, 0, 16, 8, 33, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 12, 11, 51, 0, 4, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [14, 3.9999999999999996, 0, 0, 26, 90, 64, 0, 28, 0, 0], [14, 0.6666666666666666, 12, 6, 24, 36, 36, 10, 36, 0, 0], [14, 1.6666666666666665, 30, 6, 26, 51, 0, 3, 0, 0, 0], [14, 1.6666666666666665, 0, 0, 14, 24, 64, 22, 28, 0, 1], [14, 0.6666666666666666, 0, 10, 24, 51, 32, 19, 28, 0, 1], [0, 0, 0, 24, 15, 69, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 14, 10, 36, 0, 8, 0, 0, 1], [0, 0, 0, 20, 13, 63, 0, 1, 0, 0, 1], [6, 0, 0, 8, 8, 36, 0, 3, 0, 0, 0], [0, 0, 0, 2, 8, 21, 0, 0, 0, 0, 0], [6, 1.5, 18, 0, 4, 0, 36, 1, 0, 0, 0], [6, 1.5, 0, 14, 7, 36, 16, 4, 16, 0, 1], [0, 0, 0, 0, 7, 21, 0, 12, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 54, 0, 5, 0, 0, 1], [0, 0, 0, 28, 14, 69, 0, 1, 0, 0, 1], [8, 0.5, 6, 4, 36, 105, 108, 3, 84, 6, 0], [8, 1.5, 18, 8, 40, 165, 60, 1, 40, 0, 0], [8, 0, 0, 8, 36, 153, 72, 4, 52, 0, 0], [2, 0.5, 0, 10, 32, 129, 108, 21, 36, 0, 1], [0, 1.5, 0, 0, 27, 111, 92, 29, 36, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 12, 6, 30, 0, 9, 0, 0, 1], [0, 0, 0, 20, 10, 48, 0, 5, 0, 0, 1], [12, 3.833333333333333, 6, 0, 2, 0, 80, 0, 8, 0, 0], [2, 1.6666666666666665, 0, 8, 15, 39, 0, 1, 0, 0, 0], [2, 0, 0, 0, 11, 15, 44, 4, 24, 0, 0], [12, 1.6666666666666665, 30, 10, 9, 9, 44, 5, 28, 0, 1], [12, 0.5, 0, 4, 8, 0, 56, 14, 8, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 39, 0, 5, 0, 0, 1], [0, 0, 0, 2, 1, 0, 0, 14, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 24, 12, 66, 0, 3, 0, 0, 1], [0, 0, 0, 16, 8, 42, 0, 7, 0, 0, 1], [0, 0, 0, 24, 12, 51, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 4, 2, 12, 0, 13, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 28, 14, 78, 0, 1, 0, 0, 1], [0, 0, 0, 14, 7, 36, 0, 8, 0, 0, 1], [0, 0, 0, 6, 8, 24, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 2, 1, 0, 0, 14, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [0, 0, 0, 14, 10, 39, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 18, 12, 60, 0, 6, 0, 0, 1], [0, 0, 0, 20, 13, 63, 0, 1, 0, 0, 1], [16, 0.6666666666666666, 0, 0, 19, 96, 156, 8, 64, 0, 0], [14, 7.333333333333333, 30, 8, 23, 60, 72, 0, 72, 0, 0], [10, 1.5, 18, 8, 28, 45, 0, 3, 0, 0, 0], [20, 7.333333333333333, 12, 0, 23, 84, 108, 4, 48, 0, 1], [20, 8.166666666666666, 0, 2, 8, 24, 236, 22, 64, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 4, 0, 0, 0], [10, 0, 0, 4, 7, 36, 0, 9, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 10, 45, 0, 1, 0, 0, 1], [10, 0, 0, 2, 6, 30, 0, 14, 0, 0, 1], [6, 0, 0, 10, 22, 144, 16, 3, 16, 0, 0], [6, 0, 0, 10, 22, 108, 32, 4, 16, 0, 0], [6, 1.5, 18, 0, 8, 48, 88, 3, 16, 0, 0], [0, 1.5, 0, 10, 25, 99, 36, 5, 36, 0, 1], [6, 0, 0, 6, 11, 42, 88, 25, 36, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 22, 11, 45, 0, 4, 0, 0, 1], [0, 0, 0, 16, 8, 36, 0, 7, 0, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 16, 13, 63, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 10, 51, 0, 1, 0, 0, 1], [10, 0, 0, 0, 5, 30, 0, 15, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 8, 6, 30, 0, 4, 0, 0, 0], [0, 0, 0, 14, 9, 39, 0, 8, 0, 0, 1], [0, 0, 0, 20, 12, 51, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 10, 5, 12, 0, 5, 0, 0, 0], [0, 0, 0, 16, 8, 24, 0, 3, 0, 0, 1], [0, 0, 0, 22, 11, 39, 0, 3, 0, 0, 1], [10, 1.6666666666666665, 0, 6, 3, 9, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 0, 0, 4, 2, 6, 0, 13, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [6, 0, 0, 4, 9, 54, 0, 3, 0, 0, 0], [6, 0, 0, 8, 9, 54, 0, 3, 0, 0, 0], [6, 1.5, 0, 0, 0, 0, 56, 1, 0, 0, 0], [6, 1.5, 18, 14, 14, 84, 0, 5, 0, 6, 1], [6, 0, 0, 10, 7, 36, 0, 15, 0, 0, 1], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1.6666666666666665, 0, 8, 9, 39, 0, 4, 0, 0, 0], [0, 0, 0, 14, 12, 48, 0, 3, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [2, 0.5, 6, 24, 32, 102, 64, 0, 64, 0, 0], [6, 0.6666666666666666, 0, 8, 28, 114, 64, 1, 64, 0, 0], [6, 0.6666666666666666, 12, 16, 32, 120, 32, 1, 32, 0, 0], [4, 0.6666666666666666, 0, 0, 19, 60, 136, 20, 52, 0, 1], [4, 0.5, 0, 0, 13, 60, 172, 28, 52, 0, 1], [16, 1.6666666666666665, 30, 8, 4, 24, 0, 3, 0, 0, 0], [16, 1.5, 0, 0, 0, 0, 16, 6, 0, 4, 0], [10, 1.6666666666666665, 0, 10, 11, 33, 0, 0, 0, 0, 0], [16, 1.5, 18, 4, 5, 15, 0, 10, 0, 6, 1], [0, 1.6666666666666665, 0, 4, 13, 60, 0, 4, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 4, 2, 12, 0, 13, 0, 0, 1], [0, 0, 0, 20, 10, 51, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 7, 0, 0, 0], [10, 0, 0, 20, 15, 78, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 10, 54, 0, 1, 0, 0, 1], [0, 0, 0, 0, 10, 60, 0, 10, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 16, 8, 42, 0, 7, 0, 0, 1], [0, 0, 0, 14, 7, 42, 0, 8, 0, 0, 1], [0, 0, 0, 2, 21, 96, 20, 0, 0, 0, 0], [6, 1.5, 0, 0, 5, 15, 96, 0, 20, 0, 0], [6, 0, 0, 8, 19, 114, 0, 4, 0, 0, 0], [6, 1.5, 18, 14, 24, 132, 20, 5, 20, 6, 1], [6, 0, 0, 8, 16, 90, 0, 21, 0, 0, 1], [0, 1.6666666666666665, 0, 10, 10, 39, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 15, 60, 0, 0, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 12, 6, 30, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 10, 42, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 2, 11, 75, 0, 9, 0, 0, 1], [12, 3.333333333333333, 0, 10, 30, 0, 140, 0, 108, 0, 0], [12, 0.6666666666666666, 12, 0, 30, 0, 104, 5, 72, 0, 0], [18, 4.166666666666666, 54, 10, 36, 0, 32, 3, 32, 0, 0], [6, 3.333333333333333, 0, 2, 21, 12, 192, 21, 72, 0, 1], [14, 1.5, 0, 0, 23, 12, 172, 10, 72, 0, 1], [6, 1.5, 0, 22, 31, 174, 40, 0, 36, 0, 0], [6, 0, 0, 0, 28, 153, 36, 3, 36, 0, 0], [6, 0, 0, 8, 27, 162, 40, 4, 20, 0, 0], [6, 1.5, 18, 14, 24, 132, 88, 13, 40, 0, 1], [0, 0, 0, 0, 15, 75, 128, 30, 36, 0, 1], [4, 0.6666666666666666, 0, 8, 28, 99, 12, 0, 12, 0, 0], [14, 3.9999999999999996, 12, 6, 22, 60, 36, 1, 16, 0, 0], [0, 1.6666666666666665, 0, 0, 18, 66, 36, 1, 32, 0, 0], [10, 0.6666666666666666, 0, 2, 19, 66, 48, 15, 32, 0, 1], [14, 1.6666666666666665, 30, 6, 19, 60, 36, 7, 20, 0, 1], [0, 0, 0, 14, 7, 30, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 20, 10, 54, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 1], [10, 4.833333333333333, 0, 0, 19, 96, 40, 4, 16, 0, 0], [6, 1.6666666666666665, 0, 0, 18, 108, 0, 6, 0, 0, 0], [6, 0, 0, 0, 13, 63, 20, 4, 20, 0, 0], [16, 4.833333333333333, 63, 4, 10, 51, 72, 13, 40, 0, 1], [10, 0, 0, 4, 17, 84, 56, 10, 16, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 16, 8, 33, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [0, 0, 0, 14, 12, 75, 0, 3, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 4, 0, 0, 1], [6, 1.5, 0, 0, 0, 0, 36, 5, 20, 0, 0], [6, 0, 0, 8, 9, 54, 0, 3, 0, 0, 0], [0, 0, 0, 14, 18, 75, 0, 1, 0, 0, 0], [6, 1.5, 18, 4, 10, 45, 0, 10, 0, 6, 1], [6, 0, 0, 0, 8, 39, 0, 10, 0, 0, 1], [4, 3.9999999999999996, 0, 0, 29, 135, 32, 0, 32, 0, 0], [10, 3.6666666666666665, 12, 8, 25, 60, 32, 1, 20, 0, 0], [14, 1.6666666666666665, 0, 0, 3, 0, 156, 9, 32, 0, 0], [16, 0.6666666666666666, 0, 8, 17, 42, 80, 18, 32, 0, 1], [20, 4.833333333333333, 63, 0, 21, 90, 72, 3, 40, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 8, 6, 30, 0, 4, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 4, 9, 69, 0, 8, 0, 0, 1], [10, 1.6666666666666665, 0, 10, 7, 42, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 18, 9, 27, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 18, 9, 42, 0, 6, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 6, 3, 9, 0, 12, 0, 0, 1], [0, 0, 0, 10, 5, 30, 0, 9, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 12, 6, 24, 0, 9, 0, 0, 1], [0, 0, 0, 6, 3, 18, 0, 12, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 16, 8, 39, 0, 7, 0, 0, 1], [0, 1.6666666666666665, 0, 12, 11, 60, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 10, 5, 24, 0, 10, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [0, 0, 0, 0, 5, 15, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 16, 13, 48, 0, 2, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 12, 13, 63, 0, 9, 0, 0, 0], [0, 0, 0, 2, 13, 72, 0, 9, 0, 0, 1], [10, 1.6666666666666665, 0, 10, 12, 63, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 10, 8, 33, 0, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 2, 4, 9, 0, 14, 0, 0, 1], [0, 0, 0, 20, 13, 63, 0, 1, 0, 0, 1], [6, 0, 0, 18, 14, 84, 0, 6, 0, 0, 0], [0, 0, 0, 10, 21, 108, 20, 0, 20, 4, 0], [6, 1.5, 0, 0, 0, 0, 76, 1, 20, 0, 0], [6, 1.5, 18, 14, 20, 108, 16, 4, 0, 0, 1], [6, 0, 0, 2, 9, 48, 56, 19, 16, 0, 1], [0, 0, 0, 0, 3, 9, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 22, 14, 69, 0, 4, 0, 0, 1], [0, 0, 0, 20, 13, 69, 0, 1, 0, 0, 1], [12, 0.5, 6, 4, 4, 0, 40, 5, 16, 0, 0], [12, 1.6666666666666665, 30, 14, 10, 54, 0, 1, 0, 0, 0], [12, 1.6666666666666665, 0, 6, 6, 0, 16, 5, 0, 0, 0], [0, 0.5, 0, 12, 17, 75, 12, 3, 12, 0, 1], [12, 1.6666666666666665, 0, 0, 5, 9, 28, 4, 12, 0, 1], [2, 0.5, 6, 0, 43, 141, 108, 0, 96, 0, 0], [6, 0.6666666666666666, 12, 8, 43, 111, 92, 1, 52, 0, 0], [4, 0.6666666666666666, 0, 6, 30, 87, 180, 9, 84, 0, 0], [6, 0.6666666666666666, 0, 6, 32, 120, 180, 13, 84, 8, 1], [0, 0.5, 0, 8, 36, 99, 148, 23, 84, 0, 1], [2, 0.5, 6, 0, 4, 0, 72, 3, 8, 0, 0], [0, 0, 0, 0, 12, 9, 0, 0, 0, 0, 0], [2, 0, 0, 18, 13, 42, 0, 4, 0, 0, 0], [2, 0, 0, 20, 17, 57, 0, 1, 0, 0, 1], [2, 0.5, 0, 6, 12, 27, 0, 13, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0], [0, 0, 0, 18, 14, 72, 0, 4, 0, 0, 0], [0, 0, 0, 10, 10, 45, 0, 6, 0, 0, 1], [0, 0, 0, 10, 10, 42, 0, 5, 0, 0, 1], [6, 0, 0, 8, 9, 54, 0, 3, 0, 0, 0], [6, 0, 0, 12, 11, 27, 20, 4, 0, 4, 0], [6, 1.5, 18, 0, 5, 15, 36, 1, 0, 0, 0], [0, 0, 0, 12, 14, 63, 16, 6, 16, 0, 1], [6, 1.5, 0, 14, 7, 30, 36, 4, 20, 0, 1], [8, 0.5, 6, 14, 20, 60, 32, 3, 32, 0, 0], [8, 0, 0, 18, 17, 66, 20, 4, 20, 0, 0], [8, 1.5, 18, 8, 17, 30, 40, 1, 40, 0, 0], [2, 0.5, 0, 0, 7, 18, 144, 20, 32, 0, 1], [6, 1.5, 0, 4, 12, 30, 104, 13, 32, 0, 1], [4, 0.6666666666666666, 0, 8, 28, 87, 52, 0, 32, 0, 0], [4, 0.6666666666666666, 12, 6, 32, 120, 36, 1, 36, 0, 0], [4, 0, 0, 12, 22, 90, 64, 5, 32, 0, 0], [4, 0.6666666666666666, 0, 16, 29, 120, 32, 4, 32, 0, 1], [0, 0, 0, 8, 25, 69, 72, 19, 32, 0, 1], [6, 1.5, 0, 0, 0, 0, 56, 0, 20, 0, 0], [6, 0, 0, 2, 3, 0, 0, 3, 0, 4, 0], [6, 0, 0, 18, 14, 84, 0, 4, 0, 4, 0], [6, 1.5, 18, 14, 14, 60, 0, 4, 0, 0, 1], [0, 0, 0, 14, 17, 63, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 18, 9, 39, 0, 4, 0, 0, 1], [0, 0, 0, 28, 14, 75, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 26, 13, 72, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 48, 0, 0, 0, 0, 1], [0, 0, 0, 10, 5, 24, 0, 10, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 4, 18, 0, 11, 0, 0, 1], [0, 0, 0, 6, 3, 18, 0, 12, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 26, 13, 51, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 14, 7, 18, 0, 8, 0, 0, 1], [14, 3.9999999999999996, 30, 0, 31, 60, 72, 0, 72, 0, 0], [14, 3.9999999999999996, 12, 8, 30, 45, 100, 1, 60, 0, 0], [20, 1.5, 18, 8, 27, 60, 80, 8, 40, 0, 0], [6, 0.6666666666666666, 0, 2, 22, 66, 164, 21, 72, 0, 1], [16, 4.833333333333333, 0, 0, 25, 66, 112, 6, 72, 0, 1], [0, 0, 0, 8, 9, 42, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 20, 15, 84, 0, 1, 0, 0, 1], [0, 0, 0, 24, 17, 90, 0, 3, 0, 0, 1], [10, 1.6666666666666665, 0, 2, 1, 0, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 16, 8, 33, 0, 7, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [0, 0, 0, 8, 7, 21, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 16, 11, 51, 0, 7, 0, 0, 1], [0, 0, 0, 20, 13, 69, 0, 1, 0, 0, 1], [4, 0.6666666666666666, 0, 10, 26, 66, 28, 3, 28, 0, 0], [4, 0.6666666666666666, 12, 8, 24, 36, 68, 1, 52, 0, 0], [4, 0, 0, 18, 26, 66, 0, 3, 0, 0, 0], [0, 0, 0, 0, 16, 36, 76, 23, 28, 0, 1], [0, 0.6666666666666666, 0, 6, 15, 24, 80, 23, 28, 0, 1], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 10, 5, 24, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 54, 0, 1, 0, 0, 1], [0, 0, 0, 10, 5, 30, 0, 10, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 4, 2, 12, 0, 13, 0, 0, 1], [0, 0, 0, 20, 10, 54, 0, 3, 0, 0, 1], [2, 0.5, 6, 0, 0, 0, 116, 0, 20, 0, 0], [0, 0, 0, 24, 18, 93, 48, 0, 28, 0, 0], [2, 0, 0, 12, 21, 102, 0, 1, 0, 0, 0], [2, 0, 0, 20, 25, 129, 16, 1, 16, 0, 1], [2, 0.5, 0, 0, 15, 90, 56, 14, 20, 0, 1], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 18, 9, 42, 0, 6, 0, 0, 0], [0, 0, 0, 16, 8, 39, 0, 3, 0, 0, 1], [0, 0, 0, 20, 10, 27, 0, 5, 0, 0, 1], [8, 0.6666666666666666, 0, 6, 25, 18, 156, 4, 52, 0, 0], [4, 1.3333333333333333, 0, 0, 25, 72, 100, 2, 60, 0, 0], [12, 3.333333333333333, 24, 0, 26, 0, 56, 4, 56, 0, 0], [12, 0.6666666666666666, 12, 0, 25, 12, 116, 8, 60, 0, 1], [12, 1.3333333333333333, 0, 8, 39, 12, 16, 2, 52, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 14, 10, 30, 0, 1, 0, 0, 0], [0, 0, 0, 2, 4, 9, 0, 14, 0, 0, 1], [0, 0, 0, 20, 13, 54, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 7, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 10, 5, 15, 0, 10, 0, 0, 1], [0, 0, 0, 18, 9, 48, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 54, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 1], [6, 1.5, 0, 0, 0, 0, 52, 0, 16, 0, 0], [6, 0, 0, 8, 8, 48, 0, 4, 0, 0, 0], [6, 0, 0, 10, 12, 63, 16, 3, 0, 0, 0], [6, 1.5, 18, 14, 10, 51, 32, 9, 0, 0, 1], [6, 0, 0, 14, 14, 69, 20, 8, 16, 0, 1], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 5, 24, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 10, 5, 24, 0, 10, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 5, 0, 0, 1], [0, 0, 0, 18, 9, 45, 0, 6, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 14, 0, 0, 1], [0, 0, 0, 20, 10, 54, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 28, 14, 84, 0, 1, 0, 0, 1], [0, 0, 0, 6, 3, 18, 0, 12, 0, 0, 1], [12, 0.5, 6, 8, 25, 54, 128, 8, 64, 0, 0], [16, 3.9999999999999996, 57, 8, 31, 114, 84, 1, 84, 0, 0], [6, 3.9999999999999996, 0, 0, 29, 135, 84, 4, 60, 0, 0], [0, 0.5, 0, 0, 30, 105, 112, 12, 52, 0, 1], [14, 3.9999999999999996, 0, 0, 17, 60, 196, 11, 52, 0, 1], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 10, 5, 30, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 54, 0, 1, 0, 0, 1], [0, 0, 0, 8, 4, 18, 0, 11, 0, 0, 1], [0, 0, 0, 10, 20, 102, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 15, 84, 0, 1, 0, 0, 1], [0, 0, 0, 16, 23, 120, 0, 2, 0, 0, 1], [16, 4.833333333333333, 30, 0, 0, 0, 36, 0, 20, 0, 0], [6, 1.6666666666666665, 0, 8, 9, 42, 0, 4, 0, 0, 0], [10, 0, 0, 2, 7, 9, 0, 7, 0, 0, 0], [16, 1.5, 18, 0, 3, 9, 0, 12, 0, 6, 1], [6, 1.6666666666666665, 0, 4, 10, 45, 0, 7, 0, 0, 1], [4, 0.6666666666666666, 0, 18, 28, 87, 32, 3, 32, 0, 0], [4, 0.6666666666666666, 12, 8, 31, 99, 32, 1, 32, 0, 0], [4, 0, 0, 2, 15, 30, 108, 10, 28, 0, 0], [4, 0, 0, 2, 17, 45, 80, 25, 32, 0, 1], [4, 0.6666666666666666, 0, 16, 27, 90, 68, 4, 52, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 22, 11, 60, 0, 4, 0, 0, 1], [0, 0, 0, 12, 6, 15, 0, 9, 0, 0, 1], [2, 0.5, 6, 4, 2, 0, 52, 3, 20, 0, 0], [2, 0, 0, 8, 8, 48, 0, 9, 0, 0, 0], [2, 0, 0, 18, 13, 78, 0, 1, 0, 0, 0], [2, 0.5, 0, 4, 6, 24, 0, 12, 0, 0, 1], [2, 0, 0, 16, 12, 72, 0, 5, 0, 0, 1], [2, 0.5, 6, 10, 28, 30, 68, 3, 56, 8, 0], [6, 0.6666666666666666, 12, 8, 28, 48, 64, 1, 64, 0, 0], [0, 0.6666666666666666, 0, 6, 19, 0, 148, 8, 44, 8, 0], [4, 0.5, 0, 0, 18, 0, 128, 13, 44, 8, 1], [6, 0.6666666666666666, 0, 0, 6, 0, 228, 21, 56, 8, 1], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 8, 9, 42, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 20, 15, 75, 0, 1, 0, 0, 1], [0, 0, 0, 22, 16, 78, 0, 4, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 12, 8, 21, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 10, 7, 18, 0, 10, 0, 0, 1], [0, 0, 0, 20, 12, 51, 0, 1, 0, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], [0, 1.6666666666666665, 0, 14, 17, 108, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 0, 10, 75, 0, 10, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 12, 6, 30, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 20, 10, 27, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 12, 6, 24, 0, 4, 0, 0, 0], [0, 0, 0, 16, 8, 24, 0, 3, 0, 0, 1], [0, 0, 0, 24, 12, 36, 0, 0, 0, 0, 1], [0, 1.6666666666666665, 0, 14, 12, 48, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 15, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [12, 3.833333333333333, 51, 6, 32, 12, 92, 0, 92, 0, 0], [14, 8.333333333333332, 48, 6, 35, 48, 48, 1, 48, 0, 0], [6, 3.333333333333333, 0, 0, 31, 72, 64, 1, 64, 0, 0], [20, 8.333333333333332, 0, 0, 6, 12, 296, 20, 72, 0, 1], [22, 0.5, 0, 0, 15, 24, 216, 27, 72, 0, 1], [12, 8.333333333333332, 0, 0, 10, 0, 40, 0, 12, 0, 0], [12, 1.3333333333333333, 24, 6, 16, 0, 0, 3, 0, 4, 0], [22, 3.9999999999999996, 0, 2, 13, 0, 40, 7, 40, 4, 0], [22, 3.9999999999999996, 57, 6, 15, 0, 40, 4, 40, 0, 1], [18, 1.3333333333333333, 0, 2, 7, 6, 80, 16, 0, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 4, 0, 0, 0], [0, 1.6666666666666665, 0, 4, 10, 66, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0], [10, 0, 0, 6, 6, 27, 0, 12, 0, 0, 1], [10, 1.6666666666666665, 0, 10, 8, 39, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0], [0, 0, 0, 16, 10, 39, 0, 5, 0, 4, 0], [0, 0, 0, 22, 13, 42, 0, 3, 0, 0, 1], [0, 0, 0, 10, 7, 9, 0, 6, 0, 0, 1], [2, 0.5, 6, 0, 0, 0, 116, 0, 20, 0, 0], [0, 0, 0, 6, 9, 24, 0, 0, 0, 0, 0], [2, 0, 0, 12, 21, 99, 0, 1, 0, 0, 0], [0, 0.5, 0, 0, 16, 75, 0, 14, 0, 0, 1], [2, 0, 0, 20, 20, 99, 0, 5, 0, 0, 1], [18, 3.5, 33, 8, 31, 60, 112, 5, 64, 0, 0], [10, 3.9999999999999996, 0, 8, 24, 30, 172, 3, 80, 0, 0], [16, 3.9999999999999996, 57, 0, 35, 120, 108, 1, 108, 0, 0], [22, 0.5, 0, 0, 17, 30, 228, 29, 64, 0, 1], [22, 8.666666666666666, 0, 0, 20, 45, 200, 5, 72, 0, 1], [0, 1.6666666666666665, 0, 14, 12, 66, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 0, 0, 8, 4, 9, 0, 11, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 16, 8, 39, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 12, 6, 30, 0, 9, 0, 0, 1], [8, 0.5, 6, 0, 38, 45, 148, 3, 104, 0, 0], [12, 3.6666666666666665, 39, 10, 48, 75, 56, 1, 56, 0, 0], [12, 0.6666666666666666, 0, 10, 36, 60, 140, 8, 96, 0, 0], [4, 3.5, 0, 0, 34, 15, 184, 24, 84, 0, 1], [0, 0.6666666666666666, 0, 8, 33, 15, 208, 15, 84, 0, 1], [6, 0, 0, 0, 2, 12, 0, 3, 0, 0, 0], [6, 0, 0, 18, 9, 54, 0, 3, 0, 0, 0], [6, 1.5, 0, 0, 0, 0, 36, 1, 0, 0, 0], [6, 1.5, 18, 14, 9, 54, 0, 5, 0, 6, 1], [6, 0, 0, 8, 6, 36, 0, 11, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 6, 0], [0, 0, 0, 8, 4, 24, 0, 8, 0, 0, 1], [0, 0, 0, 14, 7, 42, 0, 8, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 10, 5, 12, 0, 3, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 28, 14, 57, 0, 1, 0, 0, 1], [6, 0, 0, 8, 4, 24, 0, 3, 0, 0, 0], [6, 1.5, 0, 0, 0, 0, 36, 1, 0, 0, 0], [6, 0, 0, 2, 4, 9, 36, 3, 0, 0, 0], [6, 1.5, 18, 14, 10, 45, 16, 5, 0, 0, 1], [0, 0, 0, 8, 10, 30, 20, 8, 16, 0, 1], [2, 0.5, 6, 10, 26, 54, 68, 3, 56, 0, 0], [6, 0.6666666666666666, 0, 8, 21, 72, 76, 1, 52, 0, 0], [6, 0.6666666666666666, 12, 18, 29, 102, 24, 1, 24, 0, 0], [4, 0.5, 0, 0, 13, 24, 152, 24, 44, 0, 1], [6, 0.6666666666666666, 0, 6, 18, 24, 116, 17, 44, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 8, 9, 24, 0, 0, 0, 0, 0], [10, 0, 0, 6, 3, 12, 0, 12, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [0, 1.6666666666666665, 0, 10, 10, 54, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 2, 6, 30, 0, 9, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 24, 0, 5, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 14, 7, 33, 0, 8, 0, 0, 1], [0, 0, 0, 12, 6, 30, 0, 9, 0, 0, 1], [6, 1.5, 0, 0, 0, 0, 56, 0, 20, 0, 0], [6, 0, 0, 8, 9, 54, 0, 3, 0, 0, 0], [6, 0, 0, 12, 8, 36, 0, 3, 0, 0, 0], [6, 1.5, 18, 14, 14, 72, 0, 5, 0, 6, 1], [0, 0, 0, 2, 11, 36, 0, 11, 0, 0, 1], [14, 3.9999999999999996, 30, 8, 21, 36, 52, 3, 52, 0, 0], [14, 0.6666666666666666, 12, 8, 24, 60, 32, 6, 12, 0, 0], [4, 1.6666666666666665, 0, 0, 22, 69, 44, 6, 28, 0, 0], [14, 0, 0, 8, 21, 24, 84, 14, 28, 0, 1], [14, 3.9999999999999996, 0, 6, 12, 0, 128, 8, 56, 0, 1], [0, 0, 0, 20, 13, 69, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 3, 9, 0, 15, 0, 0, 1], [0, 0, 0, 20, 13, 69, 0, 1, 0, 0, 1], [14, 3.9999999999999996, 30, 8, 22, 54, 52, 3, 52, 0, 0], [14, 0.6666666666666666, 12, 8, 25, 66, 32, 6, 12, 0, 0], [10, 1.6666666666666665, 0, 2, 9, 12, 132, 3, 28, 0, 0], [14, 3.9999999999999996, 0, 6, 17, 30, 112, 4, 56, 0, 1], [10, 0, 0, 8, 16, 24, 116, 20, 32, 0, 1], [6, 0, 0, 2, 3, 12, 0, 3, 0, 0, 0], [6, 0, 0, 18, 9, 54, 0, 3, 0, 0, 0], [6, 1.5, 0, 0, 0, 0, 36, 1, 0, 0, 0], [6, 1.5, 18, 14, 9, 54, 0, 5, 0, 6, 1], [0, 0, 0, 6, 8, 24, 0, 9, 0, 0, 1], [0, 0, 0, 18, 9, 33, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 2, 1, 0, 0, 14, 0, 0, 1], [4, 3.9999999999999996, 0, 8, 22, 54, 12, 3, 12, 0, 0], [4, 0.6666666666666666, 12, 8, 25, 63, 12, 1, 12, 0, 0], [14, 1.6666666666666665, 0, 6, 16, 24, 36, 3, 28, 0, 0], [10, 0, 0, 0, 11, 6, 88, 20, 28, 0, 1], [14, 3.9999999999999996, 30, 6, 12, 0, 76, 8, 44, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 8, 4, 9, 0, 0, 0, 0, 0], [0, 0, 0, 20, 10, 45, 0, 1, 0, 0, 1], [0, 0, 0, 20, 10, 54, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 4, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [0, 1.6666666666666665, 0, 0, 10, 75, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 10, 15, 96, 0, 5, 0, 0, 1], [14, 1.3333333333333333, 24, 10, 9, 27, 0, 3, 0, 0, 0], [14, 1.3333333333333333, 0, 0, 4, 12, 40, 4, 40, 4, 0], [0, 1.5, 0, 12, 15, 54, 16, 0, 0, 0, 0], [14, 1.5, 18, 4, 4, 12, 56, 14, 0, 0, 1], [6, 1.3333333333333333, 0, 2, 11, 42, 40, 5, 16, 0, 1], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 1.6666666666666665, 0, 12, 8, 24, 0, 3, 0, 0, 0], [0, 0, 0, 2, 8, 36, 0, 9, 0, 0, 1], [10, 1.6666666666666665, 0, 10, 7, 21, 0, 1, 0, 0, 1], [10, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], [10, 1.6666666666666665, 0, 18, 9, 39, 0, 1, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 6, 3, 9, 0, 11, 0, 0, 1], [10, 1.6666666666666665, 30, 4, 2, 6, 0, 8, 0, 0, 1], [2, 0.5, 6, 14, 22, 51, 32, 0, 32, 0, 0], [6, 3.9999999999999996, 12, 6, 20, 102, 48, 1, 48, 0, 0], [16, 3.9999999999999996, 30, 8, 16, 48, 52, 1, 52, 0, 0], [14, 3.833333333333333, 0, 0, 5, 12, 148, 17, 32, 0, 1], [16, 0.6666666666666666, 0, 0, 4, 12, 148, 17, 32, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 12, 6, 21, 0, 5, 0, 0, 0], [0, 0, 0, 2, 6, 15, 0, 9, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [0, 1.6666666666666665, 0, 6, 8, 21, 0, 3, 0, 0, 0], [0, 0, 0, 8, 9, 24, 0, 6, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 1], [2, 0.5, 6, 8, 30, 114, 144, 0, 84, 0, 0], [6, 0.6666666666666666, 12, 6, 32, 120, 108, 1, 108, 0, 0], [6, 0.6666666666666666, 0, 14, 28, 57, 104, 6, 64, 0, 0], [6, 0.6666666666666666, 0, 0, 16, 60, 236, 26, 64, 0, 1], [4, 0.5, 0, 10, 21, 135, 172, 16, 64, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 22, 11, 60, 0, 4, 0, 0, 1], [0, 0, 0, 30, 15, 69, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 10, 5, 30, 0, 10, 0, 0, 1], [0, 0, 0, 4, 2, 6, 0, 13, 0, 0, 1], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 30, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 16, 23, 111, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 10, 15, 75, 0, 1, 0, 0, 1], [10, 0, 0, 14, 17, 78, 0, 8, 0, 0, 1], [2, 0.5, 6, 16, 32, 150, 136, 0, 88, 0, 0], [6, 0.6666666666666666, 12, 6, 30, 81, 104, 5, 72, 8, 0], [6, 0.6666666666666666, 0, 10, 36, 204, 72, 1, 72, 0, 0], [4, 0.5, 0, 8, 23, 132, 168, 23, 72, 0, 1], [0, 0.6666666666666666, 0, 0, 20, 90, 224, 26, 72, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 18, 9, 54, 0, 6, 0, 0, 1], [0, 0, 0, 24, 12, 60, 0, 3, 0, 0, 1], [2, 0.5, 6, 8, 27, 60, 80, 0, 40, 0, 0], [6, 0.6666666666666666, 12, 8, 25, 75, 80, 1, 40, 0, 0], [10, 3.6666666666666665, 0, 10, 14, 45, 176, 5, 52, 0, 0], [12, 3.6666666666666665, 18, 10, 18, 90, 136, 5, 64, 0, 1], [6, 0.5, 0, 0, 26, 90, 96, 12, 72, 0, 1], [0, 0, 0, 10, 5, 12, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 20, 10, 51, 0, 1, 0, 0, 1], [0, 0, 0, 18, 9, 39, 0, 6, 0, 0, 1], [0, 0, 0, 2, 21, 96, 20, 5, 0, 0, 0], [6, 1.5, 0, 0, 5, 15, 96, 0, 20, 0, 0], [6, 0, 0, 8, 19, 99, 0, 4, 0, 0, 0], [6, 1.5, 18, 4, 24, 132, 20, 5, 20, 6, 1], [0, 0, 0, 2, 26, 111, 0, 11, 0, 0, 1]]
#Checking if the predicted spies is okay to go off of
# An invalid spyPrediction would be one that says everyone is a spy i.e ['MyAgent',1,1,1,1] 
def checkValidPrediction(spyPredictions,resistanceData):
    
    SpyCount = 0
    for value in spyPredictions:
        if value == 1:
            SpyCount+=1
    if(len(resistanceData)==5 and SpyCount>2):
        return -1
    elif(len(resistanceData)==6 and SpyCount>2):
        return -1
    elif(len(resistanceData)==7 and SpyCount>3):
        return -1
    elif(len(resistanceData)==8 and SpyCount>3):
        return -1
    elif(len(resistanceData)==9 and SpyCount>3):
        return -1
    elif(len(resistanceData)==10 and SpyCount>4):
        return -1
    else:
        # all goods
        return 1
def naiveBayesClassifier(resistanceData):
   
    model = summarise_by_class(trainingDataRandomSpy)
    spyPredictions = []
    for row in resistanceData:
        if(row[0] == "MyAgent"):
            spyPredictions.append("MyAgent")
        else:
            # dont need IS_SPY()
            print(row[:IS_SPY])
            spyPredictions.append(predict(model,row[:IS_SPY]))
    
    print("SPY PREDICTIONS =",spyPredictions)
    if(checkValidPrediction(spyPredictions,resistanceData) !=1):
        spyPredictions = []
    return spyPredictions
    

def summarise_by_class(dataSet):
    '''dataSet is the training dataset (data that has  spy (1) or not spy (0))'''
    seperated = separate_by_class(dataSet)
    summaries = dict()
    for class_value, rows in seperated.items():
        summaries[class_value] = summarise_dataset(rows)
    return summaries

# Split the dataset by class values, returns a dictionary
def separate_by_class(dataset):
	separated = dict()
	for i in range(len(dataset)):
		vector = dataset[i]
		class_value = vector[-1]
		if (class_value not in separated):
			separated[class_value] = list()
		separated[class_value].append(vector)

	return separated

def summarise_dataset(dataSet):
    summaries = [(mean(column),stdev(column),len(column)) for column in zip(*dataSet)]
    del(summaries[-1])
    return summaries

# Predict the class for a given row
def predict(summaries,row):
    probabilities = calculate_class_probabilities(summaries, row)
    best_label, best_prob = None,-1
    for class_value,probability in probabilities.items():
        if best_label is None or probability> best_prob:
            best_prob = probability
            best_label = class_value
    return best_label


def calculate_class_probabilities(summaries, row):
    total_rows = sum([summaries[label][0][2] for label in summaries])
    
    probabilities = dict()
    
    for class_value, class_summaries in summaries.items():
        probabilities[class_value] = summaries[class_value][0][2]/float(total_rows)
       
        for i in range(len(class_summaries)):
            
            mean,stdev, _ = class_summaries[i]
            probabilities[class_value] *= calculate_probability(row[i],mean,stdev)
    return probabilities


# Math Calculation Functions

def calculate_probability(x,mean,stdev):
    exponent = exp(-((x-mean)**2/(2*stdev**2)))
    return(1/(sqrt(2*pi)*stdev))*exponent

def mean(numbers):
    return sum(numbers)/float(len(numbers))

def stdev(numbers):
    avg = mean(numbers)
    variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
    return sqrt(variance)

