from agent import Agent
import random
import numpy as np
import pandas as pd
from game import Game
# Global variables
#indexs of varibales in dataset
VOTED_FOR_FAILED_MISSION = 0
WENT_ON_FAILED_MISSION = 1
PROP_TEAM_FAILED_MISSION = 2
REJECTED_TEAM_SUCCESFUL_MISSION = 3 
IS_SPY = 4

class myAgent(Agent):        
    #initialise class attributes


    '''My agent in the game The Resistance'''
    def __init__(self, name='Rando'):
        '''
        Initialises the agent.
        Nothing to do here.
        '''
         #initialise class attributes
        self.name = name
        self.missionNum = 0
        
       # self.df = None
        self.resistanceData = []
        self.failedMissions = []
        self.propFailedMissions = []
        
        

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
                    resistanceTable.append([0,0,0,0,0])
                    
            #self.df = pd.DataFrame(resistanceTable,columns = ['PlayerNum','votedForFailedMission',
            #'wentOnFailedMission','selTeamFailedMission','rejectedTeamProps','isSpy'])
            self.resistanceData = resistanceTable
            # how to update specific value
            #df.loc[df.PlayerNum == 1,'PlayerNum'] = df.PlayerNum +1
            #print(self.df)
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
            if(self.missionNum ==0):
                team.append(self.player_number)
                while len(team)<team_size:
                    agent = random.randrange(team_size)
                    if agent not in team:
                        team.append(agent)
            else:
                team.append(self.player_number)
                # change this to pick the most trusting players
                while len(team)<team_size:
                    agent = random.randrange(team_size)
                    if agent not in team:
                        team.append(agent)
        # agent is spy
        else:
            while len(team)<team_size:
                agent = random.randrange(team_size)
                if agent not in team:
                    team.append(agent)
        return team        

    def vote(self, mission, proposer):
        print("MY player number",self.player_number)
        print("The proposer = ",proposer)
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        #print("missionNum= ",self.missionNum)
        #always return True if agent is the proposer
        if(proposer == self.player_number):
            print("agent is proposer return True")
            return True
        #Vote on how trustworthy members going on mission are
        return random.random()<0.5

    def vote_outcome(self, mission, proposer, votes):
        self.agentsWhoVoted = []
        self.agentsWhoVoted = votes
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
        #nothing to do here
        
        print("SIZE of VOTES",len(votes),votes)

       
        
        # Mission is approved
        if(not self.is_spy()):
            if(len(votes)>=self.number_of_players//2):
                print("Vote was successful")
                
        pass

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
       
        if self.is_spy():
            return random.random()<0.3

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        mission is a list of agents that were sent on the mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        if(mission_success):
            # onto the next mission
            for i in range(self.number_of_players):
                if i not in self.agentsWhoVoted and i is not self.player_number:
                    # Increases sussness if agent did not want a successful mission to happen
                    amountThatVotedAgainst = self.number_of_players-len(self.agentsWhoVoted)
                    self.resistanceData[i][REJECTED_TEAM_SUCCESFUL_MISSION] += (self.number_of_players/amountThatVotedAgainst)
            self.missionNum +=1
        # failed mission
        else:
            for agent in self.agentsWhoVoted:
                if(agent is not self.player_number):
                    # Increase sussness if agent most liekly voted knowing mission would fail
                    self.resistanceData[agent][VOTED_FOR_FAILED_MISSION]+= (self.number_of_players/len(self.agentsWhoVoted))
            # Increment the amounts that add to untrustworthyness
           
            if(proposer is not self.player_number):
                self.propFailedMissions.append(proposer)
                propFailedMissionsCount = self.propFailedMissions.count(proposer)
                if(propFailedMissionsCount == 0):
                    propFailedMissionsCount = 1
                self.resistanceData[proposer][PROP_TEAM_FAILED_MISSION] += 1*propFailedMissionsCount
                if(proposer in mission):
                    self.resistanceData[proposer][PROP_TEAM_FAILED_MISSION] += (len(mission)/(betrayals))
            #wentOnFailedMission
            # Could weight this with how many betrayals there were
            for agent in mission:
                if(agent is not self.player_number):
                    self.failedMissions.append(agent)
                    failedMissionsCount = self.failedMissions.count(agent)
                    if(failedMissionsCount == 0):
                        failedMissionsCount = 1
                    self.resistanceData[agent][WENT_ON_FAILED_MISSION] += (len(mission)*failedMissionsCount)/(betrayals)
           
        print(self.resistanceData)
        #nothing to do here
        pass

    def round_outcome(self, rounds_complete, missions_failed):
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
        print("6")
        pass



