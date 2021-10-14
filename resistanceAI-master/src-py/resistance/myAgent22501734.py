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
trainingDataStupidSpy = [[20, 8.333333333333332, 30, 0, 20, 0, 84, 6, 72, 0, 0], [0, 4.833333333333333, 33, 2, 37, 30, 0, 0, 12, 10, 0], [18, 1.3333333333333333, 24, 0, 24, 9, 28, 5, 16, 0, 0], [28, 8.333333333333332, 0, 2, 7, 18, 184, 11, 64, 6, 1], [28, 3.6666666666666665, 0, 0, 9, 18, 160, 15, 52, 6, 1], [0, 0.6666666666666666, 3, 8, 63, 90, 0, 0, 84, 10, 0], [12, 3.6666666666666665, 39, 0, 48, 60, 96, 1, 96, 0, 0], [8, 0.5, 0, 0, 38, 30, 180, 3, 96, 0, 0], [12, 0.5, 0, 8, 24, 60, 312, 20, 116, 0, 1], [12, 3.6666666666666665, 0, 0, 16, 60, 376, 13, 100, 0, 1], [2, 3.1666666666666665, 6, 0, 22, 0, 32, 0, 32, 0, 0], [14, 8.333333333333332, 48, 0, 20, 0, 32, 1, 32, 0, 0], [22, 8.666666666666666, 63, 0, 16, 0, 84, 1, 84, 0, 0], [30, 3.6666666666666665, 0, 0, 4, 0, 196, 14, 48, 0, 1], [30, 8.166666666666666, 0, 0, 4, 0, 196, 5, 32, 0, 1], [18, 7.666666666666666, 24, 0, 9, 0, 44, 0, 32, 0, 0], [14, 4.666666666666666, 30, 0, 11, 0, 60, 3, 60, 0, 0], [0, 3.9999999999999996, 12, 2, 21, 24, 0, 0, 0, 0, 0], [28, 4.833333333333333, 18, 0, 2, 12, 132, 11, 12, 0, 1], [28, 3.333333333333333, 0, 2, 3, 12, 132, 8, 48, 0, 1], [18, 3.5, 33, 0, 30, 0, 104, 5, 64, 0, 0], [24, 8.333333333333332, 108, 0, 32, 0, 108, 1, 108, 0, 0], [0, 3.333333333333333, 0, 0, 44, 0, 0, 0, 72, 0, 0], [30, 8.666666666666666, 0, 0, 8, 0, 316, 10, 52, 0, 1], [30, 8.166666666666666, 0, 0, 8, 0, 316, 16, 84, 0, 1], [12, 8.333333333333332, 24, 0, 21, 0, 48, 0, 48, 0, 0], [0, 3.333333333333333, 12, 2, 28, 12, 0, 0, 40, 0, 0], [20, 4.833333333333333, 63, 0, 17, 0, 40, 3, 40, 0, 0], [28, 4.166666666666666, 0, 2, 1, 0, 208, 11, 48, 0, 1], [28, 3.9999999999999996, 0, 0, 0, 0, 208, 17, 32, 0, 1], [18, 3.333333333333333, 0, 0, 15, 90, 60, 4, 20, 0, 0], [18, 0, 0, 0, 15, 75, 40, 12, 0, 0, 0], [18, 2.6666666666666665, 0, 0, 15, 90, 60, 6, 20, 0, 0], [18, 9.333333333333332, 69, 12, 21, 114, 80, 5, 40, 0, 1], [18, 9.333333333333332, 0, 12, 21, 114, 80, 0, 40, 0, 1], [8, 6.5, 33, 0, 27, 0, 60, 3, 48, 0, 0], [0, 0.6666666666666666, 0, 0, 37, 0, 0, 0, 64, 0, 0], [14, 6.666666666666666, 48, 0, 27, 0, 56, 1, 56, 0, 0], [20, 2.6666666666666665, 0, 0, 8, 0, 220, 8, 48, 0, 1], [20, 3.1666666666666665, 0, 0, 8, 0, 220, 14, 60, 0, 1], [8, 0.5, 6, 0, 32, 0, 120, 6, 84, 0, 0], [12, 2.6666666666666665, 39, 8, 40, 0, 60, 1, 60, 0, 0], [0, 2.6666666666666665, 0, 8, 49, 0, 0, 0, 80, 0, 0], [12, 2.5, 0, 0, 9, 0, 328, 29, 96, 0, 1], [12, 0.6666666666666666, 0, 0, 9, 0, 328, 7, 80, 0, 1], [20, 8.333333333333332, 30, 0, 23, 0, 52, 3, 52, 0, 0], [0, 1.5, 33, 2, 37, 6, 0, 0, 0, 0, 0], [18, 8.333333333333332, 24, 0, 24, 0, 44, 3, 44, 0, 0], [28, 3.333333333333333, 0, 2, 7, 0, 184, 16, 52, 0, 1], [28, 4.833333333333333, 0, 0, 9, 0, 172, 12, 60, 0, 1], [4, 3.9999999999999996, 0, 0, 26, 90, 48, 0, 48, 0, 0], [0, 3.9999999999999996, 12, 10, 33, 102, 0, 0, 40, 0, 0], [20, 1.5, 18, 8, 17, 15, 80, 8, 40, 0, 0], [20, 3.9999999999999996, 30, 0, 5, 30, 228, 4, 108, 0, 1], [20, 1.5, 0, 2, 6, 30, 228, 19, 32, 0, 1], [0, 1.6666666666666665, 0, 10, 40, 63, 0, 0, 36, 0, 0], [20, 8.666666666666666, 30, 0, 17, 30, 100, 0, 56, 0, 0], [14, 0.6666666666666666, 0, 0, 20, 15, 52, 9, 16, 0, 0], [20, 3.9999999999999996, 12, 0, 9, 27, 100, 16, 16, 0, 1], [20, 1.5, 18, 2, 18, 27, 68, 15, 16, 0, 1], [0, 0, 0, 10, 55, 138, 0, 0, 68, 8, 0], [20, 8.666666666666666, 0, 0, 27, 102, 120, 0, 36, 0, 0], [14, 3.9999999999999996, 0, 0, 30, 72, 92, 5, 36, 0, 0], [20, 0.6666666666666666, 12, 2, 23, 66, 196, 12, 72, 12, 1], [20, 4.833333333333333, 63, 0, 14, 42, 228, 16, 56, 6, 1], [0, 8.333333333333332, 0, 2, 40, 30, 0, 0, 64, 6, 0], [20, 4.833333333333333, 63, 0, 25, 9, 60, 2, 60, 0, 0], [18, 3.333333333333333, 24, 0, 26, 0, 48, 3, 48, 0, 0], [28, 4.166666666666666, 6, 2, 5, 12, 288, 18, 60, 4, 1], [28, 3.9999999999999996, 0, 0, 4, 12, 288, 8, 72, 0, 1], [20, 4.833333333333333, 63, 0, 22, 0, 40, 2, 40, 0, 0], [18, 8.333333333333332, 24, 0, 23, 0, 48, 3, 48, 0, 0], [0, 3.333333333333333, 0, 2, 37, 21, 0, 0, 60, 0, 0], [28, 8.333333333333332, 12, 2, 5, 12, 244, 16, 60, 4, 1], [28, 1.5, 0, 0, 4, 12, 244, 12, 52, 6, 1], [20, 1.6666666666666665, 30, 8, 20, 51, 32, 5, 20, 0, 0], [0, 0.6666666666666666, 30, 10, 37, 96, 0, 0, 12, 0, 0], [10, 4.833333333333333, 0, 0, 21, 90, 44, 3, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 6, 0, 240, 4, 72, 0, 1], [20, 3.6666666666666665, 0, 2, 7, 0, 240, 20, 84, 0, 1], [8, 1.6666666666666665, 0, 0, 10, 30, 20, 4, 20, 0, 0], [18, 1.6666666666666665, 30, 0, 10, 45, 20, 7, 20, 0, 0], [8, 2.6666666666666665, 0, 0, 15, 60, 0, 1, 0, 0, 0], [18, 6.0, 24, 12, 11, 54, 40, 5, 0, 0, 1], [18, 2.6666666666666665, 0, 12, 11, 54, 40, 5, 20, 0, 1], [18, 1.6666666666666665, 30, 0, 5, 0, 0, 7, 0, 0, 0], [18, 4.666666666666666, 0, 0, 5, 15, 20, 0, 0, 0, 0], [8, 1.3333333333333333, 0, 0, 10, 30, 0, 1, 0, 0, 0], [18, 1.3333333333333333, 24, 12, 6, 24, 60, 5, 0, 0, 1], [18, 1.6666666666666665, 0, 12, 6, 24, 60, 4, 40, 0, 1], [8, 1.6666666666666665, 0, 0, 15, 75, 20, 7, 20, 0, 0], [8, 1.3333333333333333, 0, 0, 15, 75, 40, 0, 40, 0, 0], [18, 4.666666666666666, 30, 0, 15, 90, 20, 1, 20, 0, 0], [18, 1.6666666666666665, 12, 12, 16, 84, 60, 4, 0, 0, 1], [18, 1.3333333333333333, 0, 12, 16, 84, 60, 10, 40, 0, 1], [12, 3.333333333333333, 24, 0, 20, 0, 44, 3, 44, 0, 0], [10, 6.666666666666666, 12, 0, 24, 0, 24, 1, 12, 0, 0], [0, 1.0, 18, 2, 33, 6, 0, 0, 24, 0, 0], [18, 0.6666666666666666, 0, 0, 9, 0, 160, 11, 72, 0, 1], [18, 3.6666666666666665, 0, 0, 9, 0, 160, 13, 44, 0, 1], [18, 2.6666666666666665, 0, 0, 15, 75, 60, 5, 20, 0, 0], [18, 0, 0, 0, 15, 75, 60, 12, 20, 0, 0], [18, 3.333333333333333, 0, 0, 15, 75, 60, 5, 20, 0, 0], [18, 9.333333333333332, 69, 12, 21, 111, 60, 5, 40, 10, 1], [18, 9.333333333333332, 0, 12, 21, 111, 60, 0, 20, 0, 1], [18, 4.666666666666666, 0, 0, 15, 75, 60, 0, 20, 0, 0], [18, 1.6666666666666665, 0, 0, 15, 75, 60, 8, 20, 0, 0], [18, 1.3333333333333333, 0, 0, 15, 75, 40, 5, 20, 0, 0], [18, 4.666666666666666, 69, 12, 21, 105, 60, 0, 40, 0, 1], [18, 0, 0, 12, 21, 105, 60, 9, 20, 0, 1], [14, 1.3333333333333333, 0, 0, 28, 90, 28, 3, 0, 0, 0], [0, 4.666666666666666, 72, 2, 43, 156, 0, 0, 28, 10, 0], [28, 8.666666666666666, 30, 0, 18, 45, 128, 8, 88, 0, 0], [28, 7.666666666666666, 0, 2, 15, 75, 124, 16, 28, 0, 1], [28, 3.9999999999999996, 0, 0, 6, 27, 124, 19, 28, 6, 1], [18, 0, 0, 0, 15, 75, 60, 12, 20, 0, 0], [18, 3.333333333333333, 0, 0, 15, 75, 40, 5, 0, 0, 0], [18, 2.6666666666666665, 0, 0, 15, 75, 60, 5, 20, 0, 0], [18, 9.333333333333332, 69, 12, 21, 111, 80, 0, 40, 10, 1], [18, 9.333333333333332, 0, 12, 21, 111, 80, 0, 40, 0, 1], [0, 0.6666666666666666, 0, 2, 23, 18, 0, 0, 32, 0, 0], [18, 9.166666666666666, 24, 0, 9, 0, 32, 3, 32, 0, 0], [14, 8.333333333333332, 30, 0, 11, 0, 40, 0, 40, 0, 0], [28, 3.333333333333333, 12, 2, 5, 12, 104, 12, 0, 0, 1], [28, 4.833333333333333, 18, 0, 4, 12, 104, 7, 0, 0, 1], [0, 6.666666666666666, 3, 0, 36, 0, 0, 0, 48, 0, 0], [8, 2.5, 18, 0, 24, 0, 68, 3, 56, 0, 0], [14, 3.333333333333333, 48, 0, 26, 0, 72, 1, 72, 0, 0], [20, 2.6666666666666665, 0, 0, 14, 0, 176, 5, 60, 0, 1], [20, 3.1666666666666665, 0, 0, 8, 0, 224, 14, 48, 0, 1], [8, 2.5, 33, 8, 27, 0, 60, 3, 48, 0, 0], [0, 0.6666666666666666, 0, 8, 37, 0, 0, 0, 60, 0, 0], [6, 2.6666666666666665, 12, 0, 27, 0, 56, 1, 56, 0, 0], [12, 0.5, 0, 0, 9, 0, 200, 22, 48, 0, 1], [12, 2.6666666666666665, 0, 0, 9, 0, 200, 6, 48, 0, 1], [0, 3.833333333333333, 6, 0, 47, 0, 0, 0, 88, 0, 0], [24, 8.333333333333332, 108, 0, 35, 0, 108, 1, 108, 0, 0], [22, 3.6666666666666665, 18, 0, 31, 0, 104, 6, 64, 0, 0], [30, 14.166666666666666, 0, 0, 5, 0, 388, 16, 108, 0, 1], [30, 3.333333333333333, 0, 0, 5, 0, 388, 9, 72, 0, 1], [10, 1.6666666666666665, 0, 0, 19, 51, 40, 5, 16, 0, 0], [20, 1.6666666666666665, 30, 8, 18, 0, 44, 6, 20, 0, 0], [0, 3.6666666666666665, 39, 10, 37, 42, 0, 0, 24, 0, 0], [20, 0.6666666666666666, 0, 2, 9, 6, 132, 19, 28, 0, 1], [20, 8.666666666666666, 0, 0, 8, 6, 132, 8, 44, 0, 1], [0, 3.833333333333333, 6, 0, 47, 0, 0, 0, 92, 0, 0], [24, 8.333333333333332, 108, 0, 35, 0, 92, 1, 92, 0, 0], [22, 7.666666666666666, 18, 0, 31, 0, 104, 6, 64, 0, 0], [30, 3.6666666666666665, 0, 0, 5, 0, 364, 14, 88, 0, 1], [30, 8.166666666666666, 0, 0, 5, 0, 364, 23, 88, 0, 1], [8, 6.5, 33, 0, 27, 0, 60, 0, 48, 0, 0], [0, 0.6666666666666666, 0, 0, 37, 0, 0, 0, 64, 0, 0], [14, 6.666666666666666, 48, 0, 27, 0, 44, 1, 44, 0, 0], [20, 3.1666666666666665, 0, 0, 6, 0, 216, 11, 60, 0, 1], [20, 2.6666666666666665, 0, 0, 12, 0, 168, 9, 36, 0, 1], [0, 1.3333333333333333, 0, 2, 40, 18, 0, 0, 72, 0, 0], [28, 8.666666666666666, 30, 0, 17, 0, 84, 4, 56, 0, 0], [12, 8.333333333333332, 0, 0, 25, 0, 48, 0, 16, 0, 0], [28, 3.9999999999999996, 12, 0, 4, 12, 188, 20, 16, 0, 1], [28, 4.166666666666666, 54, 2, 13, 12, 156, 16, 28, 0, 1], [18, 0, 0, 0, 15, 75, 60, 12, 20, 0, 0], [18, 7.999999999999999, 0, 0, 15, 90, 80, 0, 40, 0, 0], [18, 1.3333333333333333, 0, 0, 15, 90, 80, 6, 40, 0, 0], [18, 7.999999999999999, 69, 12, 21, 114, 80, 5, 40, 0, 1], [18, 3.333333333333333, 0, 12, 21, 114, 80, 4, 40, 0, 1], [18, 4.666666666666666, 0, 0, 0, 0, 20, 3, 0, 0, 0], [8, 1.3333333333333333, 0, 0, 5, 15, 0, 0, 0, 0, 0], [8, 1.6666666666666665, 0, 0, 5, 15, 0, 5, 0, 0, 0], [18, 1.6666666666666665, 12, 12, 6, 24, 0, 4, 0, 0, 1], [18, 1.3333333333333333, 15, 12, 6, 24, 0, 5, 0, 0, 1], [18, 8.333333333333332, 24, 0, 23, 0, 60, 3, 60, 0, 0], [20, 4.833333333333333, 63, 0, 25, 9, 40, 2, 40, 0, 0], [0, 0.6666666666666666, 12, 2, 38, 12, 0, 0, 32, 0, 0], [28, 8.333333333333332, 0, 0, 8, 6, 224, 8, 56, 0, 1], [28, 4.166666666666666, 0, 2, 6, 6, 236, 14, 60, 0, 1], [0, 3.9999999999999996, 0, 2, 40, 39, 0, 0, 44, 0, 0], [18, 3.333333333333333, 24, 0, 23, 0, 44, 3, 44, 0, 0], [20, 9.166666666666666, 63, 0, 25, 18, 60, 2, 60, 0, 0], [28, 3.9999999999999996, 12, 0, 7, 21, 228, 8, 32, 4, 1], [28, 4.166666666666666, 0, 2, 8, 21, 228, 21, 60, 6, 1], [22, 3.9999999999999996, 30, 0, 25, 0, 124, 4, 92, 0, 0], [0, 8.333333333333332, 12, 2, 41, 12, 0, 0, 32, 0, 0], [18, 4.166666666666666, 54, 0, 31, 0, 48, 3, 48, 0, 0], [28, 8.333333333333332, 0, 2, 5, 0, 320, 12, 108, 0, 1], [28, 1.5, 0, 0, 0, 0, 352, 21, 88, 0, 1], [6, 1.0, 18, 0, 36, 54, 60, 0, 60, 0, 0], [0, 1.0, 6, 10, 50, 108, 0, 0, 32, 4, 0], [4, 1.3333333333333333, 0, 0, 27, 18, 88, 11, 56, 6, 0], [10, 1.3333333333333333, 0, 0, 15, 63, 240, 11, 72, 0, 1], [10, 3.333333333333333, 0, 2, 17, 63, 232, 14, 68, 6, 1], [20, 4.166666666666666, 18, 0, 32, 18, 80, 7, 40, 0, 0], [0, 3.9999999999999996, 12, 2, 48, 6, 0, 0, 88, 0, 0], [28, 8.333333333333332, 69, 0, 30, 0, 104, 4, 104, 0, 0], [28, 0.6666666666666666, 0, 0, 8, 0, 316, 18, 84, 0, 1], [28, 9.166666666666666, 0, 2, 9, 0, 316, 18, 52, 0, 1], [0, 0, 9, 10, 24, 36, 0, 0, 12, 0, 0], [10, 8.666666666666666, 12, 0, 14, 30, 44, 1, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 13, 0, 52, 0, 52, 0, 0], [20, 3.9999999999999996, 0, 0, 6, 0, 96, 3, 12, 0, 1], [20, 1.5, 0, 0, 3, 0, 108, 15, 12, 0, 1], [16, 1.6666666666666665, 30, 8, 25, 75, 32, 3, 20, 0, 0], [0, 1.5, 33, 10, 37, 108, 0, 0, 12, 4, 0], [10, 3.9999999999999996, 0, 0, 21, 90, 56, 7, 44, 6, 0], [20, 3.9999999999999996, 0, 0, 6, 9, 220, 4, 84, 6, 1], [20, 3.6666666666666665, 0, 2, 7, 9, 220, 25, 52, 6, 1], [14, 3.9999999999999996, 30, 8, 30, 60, 56, 0, 56, 0, 0], [10, 8.666666666666666, 12, 0, 32, 105, 44, 1, 32, 0, 0], [0, 0, 9, 10, 42, 111, 0, 0, 52, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 284, 7, 52, 0, 1], [20, 1.5, 0, 0, 4, 0, 268, 25, 92, 0, 1], [18, 3.833333333333333, 51, 0, 25, 0, 96, 3, 72, 0, 0], [12, 14.333333333333332, 39, 0, 31, 0, 24, 1, 24, 0, 0], [20, 3.333333333333333, 24, 0, 24, 0, 68, 4, 56, 0, 0], [30, 8.666666666666666, 0, 0, 6, 0, 252, 5, 84, 0, 1], [30, 3.1666666666666665, 0, 0, 6, 0, 252, 26, 52, 0, 1], [20, 4.833333333333333, 63, 8, 27, 69, 40, 2, 40, 0, 0], [0, 0.6666666666666666, 12, 10, 38, 111, 0, 0, 32, 0, 0], [10, 3.9999999999999996, 0, 0, 25, 105, 60, 4, 60, 0, 0], [20, 4.833333333333333, 0, 0, 6, 0, 252, 7, 72, 0, 1], [20, 0.6666666666666666, 0, 2, 8, 0, 232, 20, 72, 0, 1], [16, 3.1666666666666665, 42, 0, 28, 0, 68, 3, 44, 0, 0], [22, 8.666666666666666, 99, 0, 28, 0, 64, 1, 64, 0, 0], [12, 8.333333333333332, 0, 0, 26, 0, 68, 4, 56, 0, 0], [30, 7.666666666666666, 0, 0, 10, 0, 224, 12, 72, 0, 1], [30, 3.833333333333333, 0, 0, 10, 0, 224, 17, 56, 0, 1], [28, 9.166666666666666, 69, 0, 41, 18, 84, 2, 72, 0, 0], [0, 1.3333333333333333, 24, 2, 59, 42, 0, 0, 52, 0, 0], [20, 4.666666666666666, 0, 0, 33, 0, 120, 7, 68, 0, 0], [28, 9.0, 0, 0, 20, 18, 256, 24, 104, 6, 1], [28, 4.333333333333333, 0, 0, 16, 18, 272, 13, 68, 0, 1], [22, 8.333333333333332, 69, 0, 37, 0, 104, 0, 104, 0, 0], [0, 3.9999999999999996, 0, 2, 56, 18, 0, 0, 52, 0, 0], [20, 4.166666666666666, 18, 0, 36, 0, 80, 8, 40, 0, 0], [28, 0.6666666666666666, 12, 0, 12, 12, 296, 18, 72, 0, 1], [28, 9.166666666666666, 0, 2, 13, 12, 296, 22, 100, 0, 1], [0, 3.9999999999999996, 0, 2, 23, 18, 0, 0, 32, 0, 0], [18, 3.333333333333333, 24, 0, 9, 0, 32, 4, 32, 0, 0], [20, 9.166666666666666, 30, 0, 8, 0, 60, 2, 60, 0, 0], [28, 3.9999999999999996, 12, 0, 4, 12, 104, 12, 0, 0, 1], [28, 4.166666666666666, 18, 2, 5, 12, 104, 7, 0, 0, 1], [0, 1.3333333333333333, 0, 10, 59, 228, 0, 0, 76, 6, 0], [10, 0, 0, 0, 34, 138, 64, 5, 52, 0, 0], [10, 1.5, 0, 8, 33, 45, 92, 3, 40, 0, 0], [10, 1.3333333333333333, 30, 2, 21, 102, 244, 23, 52, 6, 1], [10, 4.333333333333333, 0, 0, 20, 102, 244, 14, 84, 0, 1], [10, 0.6666666666666666, 0, 0, 22, 63, 56, 3, 44, 0, 0], [20, 3.9999999999999996, 30, 8, 21, 45, 64, 4, 52, 0, 0], [0, 1.6666666666666665, 24, 10, 37, 102, 0, 0, 12, 6, 0], [14, 8.666666666666666, 0, 0, 11, 30, 148, 1, 40, 6, 1], [20, 1.5, 0, 2, 9, 30, 160, 25, 56, 6, 1], [0, 4.666666666666666, 42, 0, 59, 0, 0, 0, 80, 0, 0], [22, 4.333333333333333, 0, 0, 32, 0, 148, 6, 68, 0, 0], [30, 4.666666666666666, 69, 0, 37, 0, 104, 6, 76, 0, 0], [30, 14.333333333333332, 0, 0, 20, 0, 244, 10, 60, 0, 1], [30, 7.166666666666666, 0, 0, 24, 0, 228, 21, 72, 0, 1], [10, 3.6666666666666665, 0, 0, 13, 30, 44, 0, 32, 0, 0], [14, 3.9999999999999996, 57, 8, 15, 0, 40, 1, 40, 0, 0], [0, 1.6666666666666665, 9, 10, 23, 42, 0, 0, 12, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 128, 3, 32, 0, 1], [20, 1.5, 0, 0, 0, 0, 128, 16, 32, 0, 1], [18, 2.6666666666666665, 0, 0, 15, 75, 40, 5, 20, 0, 0], [18, 1.6666666666666665, 0, 0, 15, 75, 40, 8, 20, 0, 0], [18, 1.6666666666666665, 0, 0, 15, 75, 40, 4, 20, 0, 0], [18, 6.0, 69, 12, 21, 105, 80, 0, 20, 0, 1], [18, 2.6666666666666665, 0, 12, 21, 105, 80, 5, 60, 0, 1], [0, 0.6666666666666666, 0, 10, 44, 108, 0, 0, 88, 0, 0], [20, 4.833333333333333, 30, 0, 27, 90, 72, 3, 72, 4, 0], [14, 3.9999999999999996, 12, 8, 29, 45, 80, 0, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 7, 21, 264, 8, 64, 0, 1], [20, 1.5, 18, 0, 7, 21, 264, 25, 40, 0, 1], [0, 3.333333333333333, 3, 0, 65, 0, 0, 0, 100, 0, 0], [16, 0.5, 0, 0, 38, 0, 188, 7, 104, 0, 0], [20, 7.666666666666666, 87, 0, 50, 0, 112, 1, 112, 0, 0], [20, 3.6666666666666665, 0, 0, 18, 0, 392, 9, 84, 0, 1], [20, 3.1666666666666665, 0, 0, 22, 0, 360, 24, 116, 0, 1], [18, 3.333333333333333, 24, 0, 23, 0, 44, 3, 44, 0, 0], [20, 9.166666666666666, 63, 0, 25, 18, 60, 2, 60, 0, 0], [0, 3.9999999999999996, 12, 2, 38, 12, 0, 0, 32, 0, 0], [28, 3.9999999999999996, 0, 0, 5, 6, 236, 16, 60, 0, 1], [28, 4.166666666666666, 0, 2, 10, 6, 204, 17, 72, 0, 1], [0, 1.0, 15, 0, 37, 0, 0, 0, 16, 0, 0], [6, 0.6666666666666666, 0, 0, 17, 0, 28, 1, 12, 0, 0], [12, 1.0, 18, 0, 17, 0, 28, 5, 12, 0, 0], [12, 4.833333333333333, 0, 0, 19, 0, 84, 8, 32, 0, 1], [12, 1.8333333333333333, 0, 0, 19, 0, 84, 5, 24, 0, 1], [18, 8.333333333333332, 24, 0, 22, 18, 60, 3, 60, 0, 0], [20, 3.9999999999999996, 30, 0, 21, 18, 52, 4, 52, 0, 0], [0, 1.5, 33, 2, 37, 54, 0, 0, 0, 0, 0], [28, 4.166666666666666, 0, 2, 9, 30, 176, 18, 44, 6, 1], [28, 8.333333333333332, 0, 0, 11, 30, 164, 4, 44, 0, 1], [28, 8.333333333333332, 69, 0, 28, 0, 72, 3, 72, 0, 0], [0, 0.6666666666666666, 12, 2, 43, 6, 0, 0, 60, 0, 0], [20, 9.166666666666666, 18, 0, 27, 0, 80, 2, 40, 0, 0], [28, 3.9999999999999996, 0, 0, 5, 0, 296, 17, 92, 0, 1], [28, 4.166666666666666, 0, 2, 6, 0, 296, 21, 72, 0, 1], [4, 1.0, 0, 0, 17, 9, 48, 2, 48, 0, 0], [0, 1.3333333333333333, 12, 10, 33, 42, 0, 0, 0, 0, 0], [10, 1.0, 18, 8, 18, 0, 12, 3, 12, 0, 0], [10, 3.333333333333333, 0, 0, 9, 27, 148, 15, 44, 6, 1], [10, 1.3333333333333333, 0, 0, 9, 27, 148, 3, 44, 6, 1], [8, 0.5, 6, 0, 30, 0, 132, 3, 96, 0, 0], [0, 2.6666666666666665, 0, 8, 47, 0, 0, 0, 56, 0, 0], [12, 2.6666666666666665, 39, 8, 38, 0, 48, 1, 48, 0, 0], [12, 0.6666666666666666, 0, 0, 12, 0, 272, 8, 80, 0, 1], [12, 2.5, 0, 0, 12, 0, 272, 19, 80, 0, 1], [0, 0, 0, 10, 58, 141, 0, 0, 96, 24, 0], [20, 9.333333333333332, 30, 8, 33, 84, 92, 4, 68, 0, 0], [6, 1.6666666666666665, 0, 0, 43, 174, 28, 3, 16, 0, 0], [20, 1.3333333333333333, 30, 2, 15, 42, 296, 28, 64, 10, 1], [20, 9.333333333333332, 0, 0, 10, 30, 312, 13, 80, 6, 1], [18, 7.666666666666666, 24, 0, 17, 21, 44, 0, 32, 0, 0], [0, 4.666666666666666, 6, 2, 27, 33, 0, 0, 40, 4, 0], [14, 3.9999999999999996, 30, 0, 16, 24, 72, 1, 72, 0, 0], [28, 1.5, 18, 0, 3, 9, 132, 16, 0, 6, 1], [28, 8.333333333333332, 0, 2, 4, 9, 132, 3, 16, 0, 1], [0, 3.9999999999999996, 0, 10, 27, 36, 0, 0, 48, 0, 0], [4, 0.6666666666666666, 12, 0, 20, 30, 48, 0, 48, 0, 0], [20, 4.833333333333333, 63, 8, 16, 0, 60, 3, 60, 0, 0], [20, 1.5, 0, 0, 0, 0, 220, 16, 48, 0, 1], [20, 3.9999999999999996, 0, 0, 0, 0, 220, 3, 32, 0, 1], [20, 4.833333333333333, 30, 8, 20, 54, 72, 2, 60, 0, 0], [0, 3.9999999999999996, 30, 10, 37, 96, 0, 0, 12, 0, 0], [10, 0, 0, 0, 21, 90, 44, 6, 32, 0, 0], [20, 3.6666666666666665, 0, 0, 6, 0, 200, 18, 64, 0, 1], [20, 3.9999999999999996, 0, 0, 9, 0, 176, 3, 52, 0, 1], [0, 0.6666666666666666, 3, 8, 41, 15, 0, 0, 56, 0, 0], [8, 3.833333333333333, 0, 0, 28, 15, 76, 3, 64, 0, 0], [22, 8.666666666666666, 99, 8, 30, 0, 64, 1, 64, 0, 0], [22, 3.833333333333333, 0, 0, 8, 0, 260, 24, 72, 0, 1], [22, 3.6666666666666665, 0, 0, 8, 0, 260, 9, 72, 0, 1], [8, 3.833333333333333, 6, 0, 28, 30, 68, 3, 56, 0, 0], [22, 8.666666666666666, 99, 8, 28, 0, 64, 1, 64, 0, 0], [0, 0.6666666666666666, 0, 8, 39, 30, 0, 0, 56, 0, 0], [22, 8.666666666666666, 0, 0, 6, 0, 260, 4, 72, 0, 1], [22, 0.5, 0, 0, 3, 0, 284, 25, 72, 0, 1], [8, 3.5, 33, 0, 30, 0, 104, 0, 64, 0, 0], [14, 3.333333333333333, 48, 0, 32, 0, 72, 1, 72, 0, 0], [6, 3.333333333333333, 0, 0, 28, 0, 104, 1, 64, 0, 0], [20, 3.6666666666666665, 0, 10, 18, 0, 224, 5, 84, 0, 1], [20, 3.1666666666666665, 0, 10, 18, 0, 224, 8, 84, 0, 1], [0, 3.9999999999999996, 0, 2, 40, 24, 0, 0, 44, 0, 0], [12, 3.333333333333333, 24, 0, 26, 0, 44, 1, 44, 0, 0], [20, 9.166666666666666, 63, 0, 25, 0, 60, 3, 60, 0, 0], [28, 3.9999999999999996, 12, 0, 7, 12, 212, 7, 32, 0, 1], [28, 4.166666666666666, 0, 0, 7, 12, 212, 22, 44, 0, 1], [8, 3.5, 33, 8, 33, 75, 104, 0, 64, 0, 0], [0, 0.6666666666666666, 0, 8, 47, 150, 0, 0, 96, 0, 0], [6, 0.6666666666666666, 12, 0, 35, 120, 88, 1, 88, 0, 0], [12, 3.6666666666666665, 0, 0, 13, 60, 260, 1, 64, 0, 1], [12, 0.5, 0, 0, 10, 60, 284, 27, 64, 0, 1], [8, 3.5, 33, 8, 33, 45, 104, 0, 64, 0, 0], [0, 0.6666666666666666, 0, 8, 47, 135, 0, 0, 80, 0, 0], [6, 0.6666666666666666, 12, 0, 35, 105, 88, 1, 88, 0, 0], [12, 0.5, 0, 0, 15, 90, 216, 20, 52, 0, 1], [12, 3.6666666666666665, 0, 0, 15, 90, 216, 10, 64, 0, 1], [8, 3.5, 33, 0, 20, 0, 24, 0, 24, 0, 0], [14, 3.333333333333333, 48, 0, 17, 0, 48, 1, 48, 0, 0], [16, 13.333333333333332, 30, 0, 13, 0, 84, 1, 84, 0, 0], [30, 13.666666666666666, 0, 0, 3, 0, 140, 8, 12, 0, 1], [30, 13.166666666666666, 0, 0, 3, 0, 140, 8, 12, 0, 1], [20, 1.6666666666666665, 30, 0, 34, 141, 84, 5, 72, 0, 0], [20, 1.5, 0, 8, 33, 60, 92, 8, 40, 0, 0], [0, 4.666666666666666, 30, 10, 57, 117, 0, 0, 52, 0, 0], [20, 9.333333333333332, 0, 0, 13, 21, 328, 6, 104, 0, 1], [20, 1.3333333333333333, 0, 2, 14, 21, 328, 32, 100, 10, 1], [0, 3.9999999999999996, 0, 2, 27, 12, 0, 0, 32, 0, 0], [12, 3.333333333333333, 48, 0, 20, 0, 32, 1, 32, 0, 0], [20, 9.166666666666666, 63, 0, 16, 0, 60, 3, 60, 0, 0], [28, 4.166666666666666, 0, 0, 0, 0, 220, 16, 48, 0, 1], [28, 3.9999999999999996, 0, 0, 0, 0, 220, 7, 48, 0, 1], [16, 4.833333333333333, 63, 0, 27, 9, 40, 0, 40, 0, 0], [18, 8.333333333333332, 24, 0, 26, 9, 48, 4, 48, 4, 0], [0, 3.333333333333333, 12, 2, 38, 18, 0, 0, 40, 4, 0], [28, 1.5, 0, 0, 2, 0, 264, 19, 52, 0, 1], [28, 8.333333333333332, 0, 0, 2, 0, 264, 17, 84, 6, 1], [6, 0, 0, 0, 28, 75, 56, 3, 32, 0, 0], [10, 1.3333333333333333, 0, 8, 27, 27, 48, 10, 24, 0, 0], [0, 2.0, 33, 10, 47, 162, 0, 0, 24, 4, 0], [10, 5.333333333333333, 0, 0, 17, 93, 164, 1, 40, 0, 1], [10, 5.333333333333333, 0, 2, 18, 93, 164, 21, 68, 8, 1], [0, 3.9999999999999996, 0, 10, 46, 81, 0, 0, 72, 0, 0], [14, 3.9999999999999996, 57, 0, 30, 60, 124, 0, 92, 0, 0], [10, 1.5, 18, 0, 36, 75, 32, 3, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 356, 20, 92, 0, 1], [20, 1.5, 0, 8, 8, 0, 292, 22, 88, 0, 1], [18, 1.3333333333333333, 0, 0, 15, 90, 60, 5, 40, 0, 0], [18, 1.6666666666666665, 0, 0, 15, 75, 20, 8, 20, 0, 0], [18, 4.666666666666666, 0, 0, 15, 90, 60, 0, 40, 0, 0], [18, 1.3333333333333333, 54, 12, 21, 120, 80, 5, 20, 0, 1], [18, 1.6666666666666665, 0, 12, 21, 120, 80, 9, 60, 0, 1], [18, 2.6666666666666665, 0, 0, 15, 75, 40, 8, 20, 0, 0], [18, 1.6666666666666665, 0, 0, 15, 60, 20, 4, 0, 0, 0], [18, 1.6666666666666665, 0, 0, 15, 60, 20, 5, 0, 0, 0], [18, 2.6666666666666665, 54, 12, 21, 114, 60, 5, 20, 8, 1], [18, 6.0, 0, 12, 21, 114, 60, 0, 40, 10, 1], [12, 3.333333333333333, 24, 0, 20, 0, 72, 0, 60, 0, 0], [0, 1.0, 6, 2, 33, 6, 0, 0, 0, 0, 0], [10, 2.6666666666666665, 18, 0, 21, 0, 24, 4, 24, 0, 0], [18, 3.333333333333333, 0, 0, 9, 0, 144, 3, 44, 0, 1], [18, 3.6666666666666665, 0, 0, 9, 0, 144, 17, 56, 0, 1], [18, 4.166666666666666, 24, 0, 19, 0, 44, 2, 32, 0, 0], [20, 4.666666666666666, 30, 0, 18, 0, 72, 6, 60, 0, 0], [0, 4.666666666666666, 30, 2, 37, 12, 0, 0, 12, 0, 0], [28, 4.333333333333333, 0, 0, 11, 6, 148, 14, 28, 0, 1], [28, 9.0, 0, 2, 9, 6, 172, 10, 56, 0, 1], [0, 8.333333333333332, 3, 0, 46, 0, 0, 0, 52, 0, 0], [18, 3.5, 18, 0, 30, 0, 112, 5, 72, 0, 0], [24, 8.333333333333332, 108, 0, 34, 0, 108, 1, 108, 0, 0], [30, 8.666666666666666, 0, 0, 10, 0, 272, 10, 52, 0, 1], [30, 3.1666666666666665, 0, 0, 10, 0, 272, 21, 84, 0, 1], [0, 8.333333333333332, 0, 2, 27, 12, 0, 0, 32, 0, 0], [12, 3.333333333333333, 48, 0, 20, 0, 48, 0, 48, 0, 0], [20, 4.833333333333333, 63, 0, 16, 0, 60, 3, 60, 0, 0], [28, 4.166666666666666, 0, 0, 0, 0, 184, 16, 32, 0, 1], [28, 3.9999999999999996, 0, 0, 0, 0, 184, 7, 32, 0, 1], [20, 8.666666666666666, 30, 0, 23, 0, 96, 0, 72, 0, 0], [0, 4.666666666666666, 24, 2, 37, 6, 0, 0, 12, 0, 0], [18, 3.333333333333333, 24, 0, 24, 0, 40, 4, 28, 0, 0], [28, 4.666666666666666, 0, 0, 6, 0, 236, 17, 84, 0, 1], [28, 3.6666666666666665, 0, 0, 6, 0, 236, 9, 84, 0, 1], [20, 3.9999999999999996, 30, 8, 25, 39, 72, 3, 72, 0, 0], [0, 1.5, 6, 10, 40, 69, 0, 0, 32, 0, 0], [10, 3.9999999999999996, 0, 0, 27, 90, 60, 4, 60, 0, 0], [20, 4.833333333333333, 18, 0, 3, 9, 264, 11, 40, 0, 1], [20, 0.6666666666666666, 0, 2, 8, 9, 232, 22, 88, 0, 1], [4, 0.6666666666666666, 0, 0, 30, 45, 144, 0, 72, 0, 0], [0, 0.6666666666666666, 12, 10, 51, 126, 0, 0, 88, 0, 0], [10, 1.5, 18, 0, 36, 90, 72, 3, 72, 0, 0], [10, 1.5, 0, 8, 18, 60, 272, 16, 92, 0, 1], [10, 0.6666666666666666, 0, 0, 10, 60, 336, 20, 92, 0, 1], [18, 3.333333333333333, 24, 0, 18, 0, 32, 3, 32, 0, 0], [0, 3.9999999999999996, 12, 2, 28, 6, 0, 0, 40, 0, 0], [20, 9.166666666666666, 63, 0, 17, 0, 60, 2, 60, 0, 0], [28, 3.9999999999999996, 0, 0, 0, 0, 208, 8, 48, 0, 1], [28, 4.166666666666666, 0, 2, 1, 0, 208, 11, 48, 0, 1], [8, 8.166666666666666, 6, 0, 30, 0, 76, 3, 64, 0, 0], [22, 8.666666666666666, 99, 0, 31, 0, 84, 1, 84, 0, 0], [20, 3.333333333333333, 24, 0, 29, 0, 84, 4, 72, 0, 0], [30, 3.9999999999999996, 0, 0, 11, 0, 256, 8, 84, 0, 1], [30, 7.5, 0, 0, 11, 0, 256, 10, 72, 0, 1]]

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
   
    model = summarise_by_class(trainingDataStupidSpy)
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

