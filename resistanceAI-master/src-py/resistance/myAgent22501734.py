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
                        if agent not in team:
                            team.append(agent)
                # if still need team members
                if(len(team)<team_size):
                    # pick members that have not failed any missions yet
                    for i in range(self.number_of_players):
                        if((len(team)<team_size) and i not in self.wentOnFailedMissions):
                            if i not in team:
                                team.append(i)
                    # last resort is to pick from random potentially picking member that potentially went on failed mission
                    # but do not pick any agents that have been found to be spies
                    while len(team)<team_size:
                        agent = random.randrange(self.number_of_players)
                        if agent not in team and agent not in self.outedSpies:
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
        naiveBayesClassifier(self.resistanceData)
        print("Outed spies",self.outedSpies)
        #nothing to do here

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
            if(len(mission)==2 and betrayals == 1):
                self.outedSpies.append(agent)
            if(len(mission)==3 and betrayals ==2 ):
                self.outedSpies.append(agent)
            if(len(mission) ==4 and betrayals == 3):
                self.outedSpies.append(agent)
            if(len(mission) == 5 and betrayals ==4):
                self.outedSpies.append(agent)
        else:
            if(len(mission) == 2 and betrayals ==2 ):
                self.outedSpies.append(agent)
            if(len(mission) == 3 and betrayals ==3 ):
                self.outedSpies.append(agent)
            if(len(mission) == 4 and betrayals ==4 ):
                self.outedSpies.append(agent)
            if(len(mission) == 5 and betrayals ==5 ):
                self.outedSpies.append(agent)



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
from csv import reader
from math import sqrt
from math import exp
from math import pi
trainingData = [[10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 0, 0, 10, 5, 15, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 0], [10, 0.6666666666666666, 0, 10, 15, 90, 88, 12, 40, 0, 1], [10, 3.6666666666666665, 12, 8, 19, 75, 52, 1, 20, 0, 0], [10, 1.5, 18, 10, 15, 90, 88, 12, 32, 0, 1], [4, 0.6666666666666666, 0, 0, 23, 105, 36, 0, 36, 0, 0], [4, 0, 0, 8, 22, 75, 40, 3, 20, 0, 0], [20, 3.9999999999999996, 0, 0, 3, 0, 152, 7, 32, 0, 1], [4, 3.9999999999999996, 12, 0, 19, 30, 32, 0, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 15, 0, 72, 1, 72, 0, 0], [20, 1.5, 18, 8, 15, 0, 40, 8, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 152, 16, 48, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 0, 0, 10, 5, 21, 0, 6, 0, 0, 0], [10, 1.6666666666666665, 30, 10, 5, 21, 0, 5, 0, 0, 0], [20, 8.666666666666666, 30, 8, 9, 30, 52, 0, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 5, 15, 36, 12, 0, 0, 1], [20, 4.833333333333333, 18, 0, 5, 15, 36, 3, 0, 0, 1], [4, 1.6666666666666665, 0, 0, 13, 45, 16, 3, 16, 0, 0], [14, 0.6666666666666666, 0, 8, 7, 0, 40, 6, 20, 0, 0], [10, 3.6666666666666665, 0, 8, 14, 30, 52, 0, 40, 0, 0], [14, 3.9999999999999996, 57, 8, 17, 45, 40, 1, 40, 0, 0], [20, 1.5, 18, 0, 5, 30, 124, 17, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 18, 60, 16, 3, 16, 0, 0], [20, 3.9999999999999996, 0, 0, 5, 30, 124, 7, 40, 0, 0], [20, 3.9999999999999996, 30, 0, 0, 0, 68, 7, 20, 0, 1], [14, 0.6666666666666666, 12, 8, 11, 0, 20, 6, 0, 0, 0], [10, 8.666666666666666, 18, 8, 13, 30, 12, 0, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 68, 12, 32, 0, 0], [4, 1.6666666666666665, 0, 0, 12, 30, 16, 3, 16, 0, 0], [4, 0.6666666666666666, 0, 0, 15, 30, 48, 0, 48, 0, 0], [14, 7.333333333333333, 57, 8, 14, 0, 60, 0, 60, 0, 0], [20, 7.333333333333333, 0, 0, 0, 0, 152, 8, 12, 0, 1], [10, 1.5, 18, 8, 16, 30, 0, 3, 0, 0, 0], [20, 8.166666666666666, 0, 0, 0, 0, 152, 6, 32, 0, 0], [14, 0.6666666666666666, 0, 8, 7, 0, 40, 5, 0, 0, 0], [4, 3.9999999999999996, 12, 8, 12, 30, 0, 1, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 72, 12, 0, 0, 1], [10, 4.833333333333333, 0, 0, 5, 30, 32, 3, 32, 0, 0], [20, 3.9999999999999996, 30, 0, 0, 0, 72, 3, 40, 0, 0], [4, 3.9999999999999996, 0, 0, 15, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 57, 8, 14, 0, 40, 0, 40, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 144, 17, 24, 0, 1], [10, 1.5, 18, 8, 16, 30, 0, 3, 0, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 144, 6, 32, 0, 0], [20, 3.9999999999999996, 30, 0, 0, 0, 116, 7, 40, 0, 1], [14, 0.6666666666666666, 12, 8, 11, 0, 40, 5, 0, 0, 0], [10, 8.666666666666666, 18, 8, 13, 30, 12, 1, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 116, 12, 32, 0, 0], [4, 1.6666666666666665, 0, 0, 12, 45, 32, 3, 32, 0, 0], [20, 3.9999999999999996, 30, 8, 7, 0, 40, 3, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 3, 0, 72, 4, 0, 0, 1], [20, 0.6666666666666666, 0, 8, 4, 0, 52, 9, 12, 0, 0], [20, 1.5, 18, 0, 3, 0, 72, 12, 0, 0, 0], [10, 4.833333333333333, 0, 0, 8, 54, 48, 2, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 12, 15, 40, 0, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 148, 14, 0, 0, 1], [10, 1.5, 18, 8, 14, 60, 0, 3, 0, 0, 0], [4, 3.9999999999999996, 0, 0, 13, 60, 48, 0, 48, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 148, 3, 60, 0, 0], [20, 3.9999999999999996, 30, 8, 8, 0, 60, 3, 60, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 120, 8, 0, 4, 1], [10, 1.5, 18, 8, 13, 30, 0, 2, 0, 0, 0], [20, 1.5, 0, 0, 0, 0, 120, 12, 32, 0, 0], [10, 3.9999999999999996, 0, 0, 9, 30, 48, 4, 48, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 72, 2, 0, 0, 1], [20, 0.6666666666666666, 12, 0, 0, 0, 72, 13, 0, 4, 1], [10, 3.6666666666666665, 18, 8, 9, 42, 12, 1, 12, 0, 0], [4, 3.9999999999999996, 0, 0, 8, 54, 32, 1, 32, 0, 0], [10, 1.6666666666666665, 30, 8, 9, 21, 40, 0, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 7, 0, 0, 1], [4, 0.6666666666666666, 12, 8, 12, 15, 0, 1, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 8, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 8, 15, 16, 3, 16, 0, 0], [20, 8.666666666666666, 30, 8, 4, 0, 52, 0, 40, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 172, 12, 40, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 15, 40, 1, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 30, 12, 0, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 172, 8, 48, 0, 0], [4, 1.6666666666666665, 0, 0, 17, 60, 32, 3, 32, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 4, 0, 0, 0], [10, 0, 0, 10, 5, 30, 0, 6, 0, 0, 0], [10, 1.6666666666666665, 30, 10, 5, 30, 0, 5, 0, 0, 0], [20, 0.6666666666666666, 0, 0, 8, 15, 124, 12, 40, 0, 1], [10, 3.6666666666666665, 12, 8, 17, 30, 52, 1, 40, 0, 0], [14, 3.9999999999999996, 30, 8, 17, 30, 52, 1, 52, 0, 0], [20, 4.833333333333333, 18, 0, 8, 15, 124, 8, 12, 0, 0], [4, 1.6666666666666665, 0, 0, 21, 69, 16, 2, 16, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 120, 7, 40, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 15, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 45, 12, 1, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 120, 13, 16, 0, 0], [4, 1.6666666666666665, 0, 0, 17, 45, 32, 3, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 11, 0, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 12, 8, 13, 15, 12, 1, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 88, 16, 0, 0, 1], [20, 3.9999999999999996, 0, 0, 0, 0, 88, 3, 32, 0, 0], [4, 1.6666666666666665, 0, 0, 12, 30, 16, 3, 16, 0, 0], [20, 3.9999999999999996, 30, 0, 0, 0, 112, 8, 40, 0, 1], [4, 3.9999999999999996, 12, 8, 17, 75, 0, 1, 0, 0, 0], [20, 1.5, 18, 8, 9, 15, 40, 8, 0, 0, 0], [4, 3.9999999999999996, 0, 0, 13, 45, 32, 0, 32, 0, 0], [20, 1.5, 0, 0, 0, 0, 112, 12, 40, 0, 0], [16, 1.6666666666666665, 0, 8, 18, 81, 0, 3, 0, 0, 0], [16, 1.6666666666666665, 0, 8, 18, 81, 0, 4, 0, 0, 0], [16, 1.5, 18, 4, 12, 66, 20, 14, 20, 6, 1], [16, 1.6666666666666665, 30, 4, 12, 66, 20, 13, 0, 0, 0], [16, 1.5, 0, 0, 19, 87, 16, 5, 16, 0, 0], [4, 3.9999999999999996, 0, 0, 15, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 57, 8, 14, 0, 60, 0, 60, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 168, 8, 12, 0, 1], [10, 1.5, 18, 8, 16, 30, 0, 3, 0, 0, 0], [20, 1.5, 0, 0, 0, 0, 168, 11, 48, 0, 0], [6, 1.5, 0, 8, 19, 114, 40, 0, 20, 0, 0], [6, 0, 0, 8, 19, 84, 0, 4, 0, 0, 0], [6, 1.5, 18, 14, 17, 96, 20, 10, 20, 6, 1], [6, 0, 0, 0, 20, 90, 0, 3, 0, 0, 0], [6, 0, 0, 14, 17, 96, 20, 13, 0, 0, 0], [4, 1.6666666666666665, 0, 0, 24, 63, 16, 2, 16, 0, 0], [20, 0.6666666666666666, 12, 0, 11, 33, 88, 12, 40, 10, 1], [10, 3.6666666666666665, 0, 8, 17, 51, 44, 1, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 20, 66, 52, 1, 52, 0, 0], [20, 4.833333333333333, 18, 0, 11, 33, 88, 8, 12, 6, 0], [6, 1.5, 0, 8, 23, 108, 40, 0, 20, 0, 0], [6, 0, 0, 8, 23, 108, 40, 4, 20, 0, 0], [6, 1.5, 18, 14, 17, 96, 92, 14, 40, 0, 1], [6, 0, 0, 14, 17, 96, 92, 13, 36, 0, 0], [6, 0, 0, 0, 24, 132, 36, 3, 36, 0, 0], [10, 3.6666666666666665, 0, 8, 9, 15, 12, 0, 0, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 84, 13, 0, 0, 1], [20, 4.833333333333333, 18, 0, 0, 0, 84, 3, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 8, 30, 32, 2, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 7, 0, 40, 1, 40, 0, 0], [4, 0.6666666666666666, 0, 0, 15, 15, 32, 0, 32, 0, 0], [14, 3.9999999999999996, 57, 8, 14, 0, 40, 1, 40, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 144, 16, 24, 0, 1], [10, 4.833333333333333, 18, 8, 16, 30, 0, 3, 0, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 144, 6, 48, 0, 0], [6, 0, 0, 8, 19, 84, 0, 3, 0, 0, 0], [6, 0, 0, 8, 19, 84, 0, 4, 0, 0, 0], [6, 1.5, 18, 14, 17, 96, 20, 10, 20, 6, 1], [6, 1.5, 0, 0, 20, 120, 36, 0, 36, 0, 0], [6, 0, 0, 14, 17, 96, 20, 13, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 7, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 0, 0, 10, 5, 15, 0, 6, 0, 0, 0], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 0], [4, 1.3333333333333333, 0, 16, 24, 90, 80, 16, 32, 0, 1], [4, 1.3333333333333333, 12, 8, 35, 111, 52, 0, 32, 0, 0], [4, 1.3333333333333333, 0, 16, 24, 90, 80, 13, 48, 0, 1], [4, 0, 0, 0, 30, 102, 0, 3, 0, 0, 0], [4, 0, 0, 8, 29, 84, 0, 6, 0, 0, 0], [10, 0.6666666666666666, 0, 10, 15, 90, 132, 12, 40, 0, 1], [4, 0.6666666666666666, 12, 8, 22, 60, 80, 1, 40, 0, 0], [10, 1.5, 18, 8, 19, 75, 80, 3, 40, 0, 0], [4, 0.6666666666666666, 0, 0, 23, 105, 72, 0, 72, 0, 0], [10, 1.5, 0, 10, 15, 90, 132, 12, 60, 0, 0], [14, 3.9999999999999996, 30, 6, 3, 9, 60, 3, 20, 0, 1], [14, 0.6666666666666666, 12, 8, 7, 12, 20, 9, 0, 0, 0], [14, 0.6666666666666666, 0, 6, 3, 9, 60, 10, 24, 6, 1], [4, 1.6666666666666665, 0, 8, 12, 42, 0, 2, 0, 0, 0], [4, 1.6666666666666665, 0, 0, 8, 45, 16, 3, 16, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 7, 0, 0, 1], [10, 3.6666666666666665, 12, 8, 9, 15, 12, 1, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 12, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 8, 15, 16, 3, 16, 0, 0], [14, 3.9999999999999996, 30, 8, 7, 0, 40, 0, 40, 0, 0], [14, 3.9999999999999996, 0, 8, 22, 75, 100, 0, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 10, 60, 152, 13, 40, 0, 1], [20, 1.5, 18, 8, 19, 60, 80, 8, 40, 0, 0], [14, 3.9999999999999996, 30, 0, 23, 90, 72, 0, 72, 0, 0], [20, 1.5, 0, 0, 10, 60, 152, 17, 40, 0, 0], [14, 3.9999999999999996, 30, 8, 11, 9, 40, 0, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 132, 17, 0, 0, 1], [10, 3.6666666666666665, 18, 8, 13, 15, 12, 1, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 132, 2, 48, 0, 0], [4, 1.6666666666666665, 0, 0, 12, 39, 32, 3, 32, 0, 0], [20, 1.5, 0, 0, 0, 0, 72, 7, 0, 0, 1], [20, 3.9999999999999996, 12, 0, 0, 0, 72, 8, 0, 0, 1], [10, 3.6666666666666665, 18, 8, 9, 15, 12, 1, 12, 0, 0], [4, 3.9999999999999996, 0, 0, 8, 39, 32, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 8, 7, 9, 40, 3, 40, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 56, 6, 0, 0, 1], [20, 0.6666666666666666, 12, 0, 0, 0, 56, 13, 0, 0, 1], [10, 3.6666666666666665, 18, 8, 9, 15, 12, 1, 12, 0, 0], [4, 3.9999999999999996, 0, 0, 8, 39, 16, 0, 16, 0, 0], [14, 1.6666666666666665, 30, 8, 7, 9, 40, 3, 40, 0, 0], [14, 0.6666666666666666, 0, 8, 17, 30, 80, 5, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 5, 30, 188, 18, 40, 0, 1], [20, 4.833333333333333, 63, 8, 19, 75, 60, 3, 60, 0, 0], [4, 3.9999999999999996, 0, 0, 23, 120, 48, 0, 48, 0, 0], [20, 4.833333333333333, 0, 0, 5, 30, 188, 8, 40, 0, 0], [20, 8.666666666666666, 30, 8, 7, 21, 52, 0, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 3, 9, 68, 13, 0, 0, 1], [4, 0.6666666666666666, 0, 8, 12, 42, 12, 1, 12, 0, 0], [20, 4.833333333333333, 18, 0, 3, 9, 68, 3, 12, 6, 0], [4, 1.6666666666666665, 0, 0, 11, 39, 16, 2, 16, 0, 0], [20, 1.5, 0, 0, 3, 0, 152, 12, 40, 0, 1], [20, 3.9999999999999996, 12, 0, 3, 0, 152, 13, 40, 4, 1], [20, 3.9999999999999996, 30, 8, 14, 30, 52, 4, 52, 16, 0], [6, 4.833333333333333, 18, 8, 24, 69, 0, 0, 0, 0, 0], [10, 0.6666666666666666, 0, 0, 18, 30, 32, 4, 32, 0, 0], [4, 1.6666666666666665, 0, 8, 12, 42, 0, 2, 0, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 56, 13, 0, 4, 1], [20, 4.833333333333333, 18, 0, 0, 0, 56, 7, 0, 6, 1], [10, 3.6666666666666665, 0, 0, 5, 15, 28, 0, 16, 0, 0], [14, 3.9999999999999996, 30, 8, 7, 12, 40, 1, 40, 0, 0], [20, 8.666666666666666, 0, 8, 23, 60, 92, 0, 40, 0, 0], [14, 0.6666666666666666, 12, 8, 26, 60, 80, 6, 40, 0, 0], [20, 4.833333333333333, 18, 0, 10, 60, 212, 16, 52, 0, 1], [20, 0.6666666666666666, 0, 0, 10, 60, 212, 17, 88, 0, 0], [14, 1.6666666666666665, 30, 0, 27, 105, 56, 3, 56, 0, 0], [20, 1.5, 0, 0, 3, 9, 172, 16, 60, 0, 1], [20, 3.9999999999999996, 12, 0, 3, 9, 172, 13, 40, 4, 1], [20, 3.9999999999999996, 30, 8, 14, 30, 72, 4, 72, 6, 0], [6, 1.5, 18, 8, 24, 69, 0, 0, 0, 0, 0], [10, 3.9999999999999996, 0, 0, 18, 69, 32, 4, 32, 0, 0], [4, 3.9999999999999996, 0, 0, 15, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 57, 8, 14, 0, 40, 1, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 132, 11, 12, 0, 1], [10, 1.5, 18, 8, 16, 15, 0, 3, 0, 0, 0], [20, 1.5, 0, 0, 0, 0, 132, 11, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 10, 0, 60, 0, 60, 0, 0], [20, 3.9999999999999996, 12, 0, 3, 0, 104, 4, 0, 0, 1], [10, 8.666666666666666, 0, 8, 9, 30, 24, 1, 12, 0, 0], [20, 1.5, 18, 0, 3, 0, 104, 12, 12, 0, 0], [4, 0, 0, 0, 11, 39, 32, 2, 32, 0, 0], [20, 4.833333333333333, 30, 8, 9, 30, 40, 2, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 5, 30, 72, 7, 0, 0, 1], [20, 1.5, 18, 0, 5, 30, 72, 12, 0, 0, 1], [10, 3.9999999999999996, 0, 0, 10, 45, 32, 4, 32, 0, 0], [10, 0.6666666666666666, 0, 8, 9, 15, 40, 4, 40, 0, 0], [4, 3.9999999999999996, 0, 8, 12, 30, 0, 0, 0, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 68, 13, 0, 0, 1], [20, 4.833333333333333, 18, 0, 0, 0, 68, 3, 12, 0, 1], [4, 0, 0, 0, 8, 15, 16, 3, 16, 0, 0], [20, 8.666666666666666, 30, 8, 4, 0, 52, 0, 40, 0, 0], [10, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 10, 5, 15, 0, 6, 0, 0, 0], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 0]]


def naiveBayesClassifier(resistanceData):
    print(resistanceData)
    model = summarise_by_class(trainingData)
    spyPredictions = []
    for row in resistanceData:
        if(row[0] == "MyAgent"):
            
            spyPredictions.append("MyAgent")
        else:
          
            # dont need IS_SPY()
            print(row[:IS_SPY])
            spyPredictions.append(predict(model,row[:IS_SPY]))
    print(resistanceData)
    print("SPY PREDICTIONS =",spyPredictions)
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

