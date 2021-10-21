from agent import Agent
import random

###-----------------------------------------------###
# Author: Shane Monck 22501734
# Agent that when is Resistance player uses a Naive Bayes Classifier to predict Spies.
# Naive Bayes Classifier was made with help from :
# https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/ written by Jason Brownlee on 18-10-2019
#
###-----------------------------------------------###

#indexs of varibales in dataset

# Variables after missions
VOTED_FOR_FAILED_MISSION = 0
WENT_ON_FAILED_MISSION = 1
PROP_TEAM_FAILED_MISSION = 2
REJECTED_TEAM_SUCCESFUL_MISSION = 3 

# Voting variables
VOTED_AGAINST_TEAM_PROPOSAL = 4
VOTED_NO_TEAM_HAS_SUCCESSFUL_MEMBERS = 5
VOTED_FOR_TEAM_HAS_UNSUCCESSFUL_MEMBERS = 6
VOTED_FOR_MISION_NOT_ON = 7

#Proposed team variables
PROPOSED_TEAM_HAS_UNSUCCESSFUL_MEMBERS = 8
PROPOSED_TEAM_THAT_HAVENT_BEEN_ON_MISSIONS = 9

IS_SPY = 10

class bayesAgent(Agent): 
    '''My agent in the game The Resistance'''
    def __init__(self, name='Rando'):
        '''
        Initialises the agent.
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
        # helper array for determing prediction accuracy
        self.allPredictions = []
        # Seperate and get the training data for later use in predicting
        get_training_data()

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spy_list = spy_list
        # Recording how many spies in game for resistance
        if(self.number_of_players == 5):
            self.howManySpies =2
        elif(self.number_of_players == 6):
            self.howManySpies =2
        elif(self.number_of_players == 7):
            self.howManySpies =3
        elif(self.number_of_players == 8):
            self.howManySpies =3
        elif(self.number_of_players == 9):
            self.howManySpies =3
        elif(self.number_of_players == 10):
            self.howManySpies =4
        
        # Track variables that help with predicting the Spies
        if(not self.is_spy()):
            resistanceTable = []
            for i in range(number_of_players):
                if i == player_number:
                    resistanceTable.append(["MyAgent"])
                else:
                    resistanceTable.append([0,0,0,0,0,0,0,0,0,0,0])
            self.resistanceData = resistanceTable

    def is_spy(self):
        '''
        returns True iff the agent is a spy
        '''
        return self.player_number in self.spy_list
    
    def resistance_propose(self,team_size,betrayals_required = 1):
        ''' 
        Proposing the mission as the resistance
        '''
        team = []
        team.append(self.player_number)
        # For the first mission as resistance
        # I want my agent to pick itself and pick at random the team members for mission
        if(self.missionNum == 1):
            while len(team) < team_size:
                agent = random.randrange(self.number_of_players)
                if agent not in team:
                    team.append(agent)
        # For other missions go of what other players have done
        else:
            onesInPredSpies = self.predictedSpies.count(1)
            # Pick agents that are predicted to not be spies as long as naive bayes has predicted the exact amount of spies in game
            if(len(self.predictedSpies) != 0 and onesInPredSpies == self.howManySpies):
                agentNum = 0
                for prediction in self.predictedSpies:
                    if(prediction == 0):
                        if(len(team) < team_size):
                            team.append(agentNum)
                    agentNum += 1
            # pick members that are the most trusting and not predicted to be a spy
            if(len(team) < team_size):
                for trustingAgents in self.wentOnSuccessfulMissions:
                    if(len(team) < team_size):
                        agent = random.choice(self.wentOnSuccessfulMissions)
                        if agent not in team and agent not in self.outedSpies:
                            if(len(self.predictedSpies) != 0):
                                if(self.predictedSpies[agent] != 1):
                                    team.append(agent)
                            else:
                                team.append(agent)
            # if still need team members
            if(len(team) < team_size):
                # pick members that have not failed any missions yet and not predicted to be a spy
                for i in range(self.number_of_players):
                    if((len(team) < team_size) and i not in self.wentOnFailedMissions):
                        if i not in team and i not in self.outedSpies:
                            if(len(self.predictedSpies) != 0):
                                if(self.predictedSpies[i] != 1):
                                    team.append(i)
                            else:
                                team.append(i)
                # last resort is to pick from random potentially picking member that potentially went on failed mission
                # but do not pick any agents that have been found to be spies
                while len(team) < team_size:
                    agent = random.randrange(self.number_of_players)
                    if agent not in team and agent not in self.outedSpies:
                        team.append(agent)
        return team

    def spy_propose(self,team_size,betrayals_required = 1):
        ''' 
        Proposing the mission as the Spy
        '''
        team = []
        # put self on team with only other reistance members
        if(self.missionNum != 4):
            team.append(self.player_number)
            while len(team) < team_size:
                agent = random.randrange(self.number_of_players)
                if ((agent not in team) and agent not in self.spy_list):
                    team.append(agent)
        else:
            team.append(self.player_number)
            # need to win mission 4 to win game
            if(self.spyWins == 1):
                # add just 1 more spy to team spy if need 2 betrayals
                if(betrayals_required == 2):   
                    while len(team) < team_size:
                        spy_count = sum(el in self.spy_list for el in mission)
                        if(spy_count == 1):
                            agent = random.choice(self.spy_list)
                        else:
                            agent = random.randrange(self.number_of_players)
                            # dont want to pick another spy at random
                            while agent not in self.spy_list:
                                agent = random.randrange(self.number_of_players)
                        if (agent not in team):
                            team.append(agent)
            # mission 4 but dont need to win mission 4 or need to win mission 4 but only need 1 betrayal
            while len(team) < team_size:
                    agent = random.randrange(self.number_of_players)
                    if (agent not in team and agent not in self.spy_list):
                        team.append(agent)
        return team

    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        team = []
        if(not self.is_spy()):
           team = self.resistance_propose(team_size,betrayals_required)
        else:
            team = self.spy_propose(team_size,betrayals_required)
        return team        

    def resistance_vote(self,mission,proposer):
        '''
        Determine vote for a resistance agent
        '''
        if(self.missionNum == 1):
            # no info to go off of for mission 1
            if(self.player_number in mission):
                return True
            else:
                return False
        # Do not vote for a mission that know 100% is a spy
        outedSpiesCount = sum(el in self.outedSpies for el in mission)
        if(outedSpiesCount != 0):
            return False
        # Dont vote for mission if contains a predicted spy
        agentNum = 0 
        predSpies = []
        for predictions in self.predictedSpies:
            if predictions == 1:
                predSpies.append(agentNum)
            agentNum += 1
        predSpiesCount = sum(el in predSpies for el in mission)
        print("predicted spies ",self.predictedSpies,"predicted spies count ", predSpiesCount,"mission ",mission)
        if predSpiesCount != 0:
            return False
        if(proposer in self.outedSpies):
            return False
        # Vote yes for a team that has all successfully passed mission
        trustedAgentsCount = sum(el in self.wentOnSuccessfulMissions for el in mission)
        if(trustedAgentsCount == len(mission)):
            return True
        failedAgentsCount = sum(el in self.wentOnFailedMissions for el in mission)
        if(failedAgentsCount > 0):
            return False
        # If there are some trust worthy members and members yet to be on mission return True
        if(trustedAgentsCount > 0 and failedAgentsCount == 0):
            return True
        # No info about anyone on the team
        if(trustedAgentsCount == 0 and failedAgentsCount == 0): 
            # return true if on team as at least you know there is one resistance member
            if(self.player_number in mission):
                return True
            else:
                return False

    def spy_vote(self,mission,proposer):
        '''
        Determine the vote for a Spy agent
        '''    
        if(self.missionNum == 1 ):
            # Spies will never sabotage first mission so does not matter who goes
            return True
        elif(self.missionNum != 1 and self.missionNum != 4):
            # count amount of spies in mission
            spy_count = sum(el in self.spy_list for el in mission)
            # approve missions that has spies on it but not if mission is full of spies no mission has 0 spies
            if(len(mission) != spy_count and spy_count != 0):
                return True
            else:   
                return False
        else:# mission 4
            # need to win mission 4  to win game
            if(self.spyWins == 1 ):
                spy_count = sum(el in self.spy_list for el in mission)
                if(self.number_of_players >= 7 and spy_count < 2):
                    # need a mission with more than 2 spies
                    return False
                    # mission needs 2 betrayals and contines 2 or more spies
                elif(self.number_of_players >= 7 and spy_count >= 2):
                    return True
                elif(self.number_of_players < 7 and spy_count > 0):
                    return True
                else:
                    # Too many spies in team or no spies at all
                    return False
            else:
            # dont care about mission 4 will go for mission 5 win
                return True
        
    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        print("Voting for mission",self.missionNum,"Round", self.roundCount)
        #always return True if agent is the proposer
        if(proposer == self.player_number):
            print("agent is proposer return True")
            return True
        if(self.is_spy()):
            return self.spy_vote(mission, proposer)
        else:
            return self.resistance_vote(mission, proposer)

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        Votes just returns a list of players that voted for the mission to go ahead
        it just a list of positive voters"
        No return value is required or expected.
        '''
        # Record vote data
        self.agentsWhoVoted = votes
        self.roundCount += 1
        if(not self.is_spy()):
            if(proposer != self.player_number):
                # if proposer proposed a mission that contains no succesful mission members
                if(len(self.wentOnSuccessfulMissions) != 0):
                    trustingMembersCount = sum(el in self.wentOnSuccessfulMissions for el in mission)
                    if(trustingMembersCount == 0):
                        self.resistanceData[proposer][PROPOSED_TEAM_THAT_HAVENT_BEEN_ON_MISSIONS] += 2*(self.missionNum)
                # if proposer proposed a mission that contains failed mission members
                if(len(self.wentOnFailedMissions) != 0):
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
            # Run predictions after significant data is added
            if(self.spyWins > 1 or self.missionNum > 2 or self.roundCount >= 3 ):
                self.predictedSpies = naiveBayesClassifier(self.resistanceData)
                self.allPredictions.append(self.predictedSpies)
            else:
                self.allPredictions.append([0])
        pass

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        if(self.missionNum == 1):
            return False
        elif(self.missionNum == 5):
            return True
        elif(self.missionNum != 4):
            spy_count = sum(el in self.spy_list for el in mission)
            if(spy_count == 1):
                return True
            elif(spy_count == 2):
                # 75 chance of betrayal
                probability = 0.75
                return random.random() <= probability
            else:
                # 50% chance of betrayal
                probability = 0.50
                return random.random() <= probability
        else:
            if(self.spyWins == 1):
                spy_count = sum(el in self.spy_list for el in mission)
                if(self.number_of_players >= 7 and spy_count < 2):
                    # need a mission with more than 2 spies
                    return False
                elif(self.number_of_players < 7 and spy_count == 1):
                    # only need 1 betray
                    return True
                elif(self.number_of_players >= 7 and spy_count == 2):
                     # need both spies to betray
                    return True
                elif(self.number_of_players >= 7 and spy_count > 2):
                    #Hope that random choices you get at least 2 spies fail but also not exposing themself
                    # This situation is difficult since the spies can not communicate
                    # assume spies do a 50/50 
                    probability = 0.5
                    return random.random() <= probability
            else:
                    # dont care about mission 4 will go for mission 5 win
                    return False
                
    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        mission is a list of agents that were sent on the mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        self.roundCount = 1
        # Record mission data for resistance agent
        if(not self.is_spy()):
            if(mission_success):
                self.resistanceWins += 1
                for agents in mission:
                    if agents == self.player_number:
                        continue
                    self.wentOnSuccessfulMissions.append(agents)
                for i in range(self.number_of_players):
    
                    if i not in self.agentsWhoVoted:
                        if(i == self.player_number):
                            continue
                        # Increases sussness if agent did not want a successful mission to happen
                        self.resistanceData[i][REJECTED_TEAM_SUCCESFUL_MISSION] += 2*(self.missionNum)
            # failed mission
            else:
                self.spyWins += 1
                for agent in self.agentsWhoVoted:
                    if(agent is not self.player_number):
                        # Increase sussness if agent most liekly voted knowing mission would fail
                        self.resistanceData[agent][VOTED_FOR_FAILED_MISSION] += 2*(self.missionNum)
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
            if((self.spyWins > 1 or self.missionNum > 2) and self.missionNum != 5):
                # Run predictions after significant data is added
                self.predictedSpies = naiveBayesClassifier(self.resistanceData)
                self.allPredictions.append(self.predictedSpies)
            else:
                self.allPredictions.append([0])
            print("Predicted spies after mission",self.predictedSpies)
            print("Outed spies",self.outedSpies)
        
        self.missionNum += 1
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
                if(len(mission)== 3 and betrayals == 2):
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 4 and betrayals == 3):
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 5 and betrayals == 4):
                    self.outedSpies.append(stupidSpies)
        # spies outed eachother
        else:
            for stupidSpies in mission:
                if(len(mission) == 2 and betrayals == 2):
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 3 and betrayals == 3):
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 4 and betrayals == 4):
                    self.outedSpies.append(stupidSpies)
                if(len(mission) == 5 and betrayals == 5):
                    self.outedSpies.append(stupidSpies)

    # Helper functions for data collection
    def returnValues(self,agentIndex):
        if(self.is_spy()):
            return (-1,self.spy_list)
        else:
            return (1,self.resistanceData,self.allPredictions)
    def returnMyAgentInfo(self,myAgentIndex):
        return self.resistanceData[myAgentIndex]
    def whoWon(self):
        if(self.spyWins > self.resistanceWins):
            return False
        elif(self.resistanceWins > self.spyWins):
            return True
        else:
            return -1

################### Naive Bayes Classifier ####################
# Make Predictions with Naive Bayes 
from math import sqrt
from math import exp
from math import pi

# Global for seperating the training data 
# Call when __init__ so to optimise time
training_data_seperated = None
def get_training_data():
    globals()['training_data_seperated'] = get_stats_for_class(trainingDataLogicalSpy)

def naiveBayesClassifier(resistanceData):
    spyPredictions = []
    for row in resistanceData:
        if(row[0] == "MyAgent"):
            spyPredictions.append("MyAgent")
        else:
            spyPredictions.append(predict(training_data_seperated,row[:IS_SPY]))
    return spyPredictions
# Predict the class for a given row
def predict(statistics,row):
    probabilities = calculate_is_spy_probabilities(statistics, row)
    best_label = None
    best_prob = -1
    for isSpy,probability in probabilities.items():
        # Find the maximum probable hypothesis
        if best_label is None or probability > best_prob:
            best_prob = probability
            best_label = isSpy
    return best_label

#Calculate the probabilites of predicting each class for row
# added Laplace smoothing to help with values that are 0.
LAPLACE_SMOOTHING = 1
def calculate_is_spy_probabilities(statistics, row):
    total_rows = sum([statistics[label][0][2] for label in statistics])
    probabilities = dict()
    for isSpy, class_stats in statistics.items():
        probabilities[isSpy] = (statistics[isSpy][0][2])/float(total_rows)
        for column in range(len(class_stats)):
            mean,stdev,n = class_stats[column]
            probabilities[isSpy] *= gaussian_probability(row[column]+LAPLACE_SMOOTHING,mean,stdev)
    return probabilities

# Split the dataset by the resistance (0) and spy (1) then calculate statistics for each of the rows
def get_stats_for_class(dataSet):
    '''dataSet is the training dataset (data that has  spy (1) or not spy (0))'''
    seperated = separate_by_class(dataSet)
    statistics = dict()
    for isSpy, rows in seperated.items():
        statistics[isSpy] = summarise_dataset(rows)
    return statistics

# Split the dataset by class values isSpy (1 For Spy 0 for Resistance). class value is determeined by last index in array which is the IS_SPY
def separate_by_class(dataset):
	separated = dict()
	for i in range(len(dataset)):
		vector = dataset[i]
		isSpy = vector[IS_SPY]
		if (isSpy not in separated):
			separated[isSpy] = list()
		separated[isSpy].append(vector)
	return separated
    
# Calculate the mean, standard deviation and count for each column in the training dataset
def summarise_dataset(dataSet):
    statistics = [(mean(column),stdev(column),len(column)) for column in zip(*dataSet)]
    del(statistics[-1])
    return statistics

# Math Calculation Functions
# Calculate the Gaussian probability distribution
def gaussian_probability(column_value,mean,stdev):
    exponent = exp(-((column_value-mean)**2/(2*stdev**2)))
    return(1/(sqrt(2*pi)*stdev))*exponent

def mean(numbers):
    return sum(numbers)/float(len(numbers))

def stdev(numbers):
    avg = mean(numbers)
    variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
    return sqrt(variance)

'''
    Training Data comes from data collected from 40, 5 player games therefore array is 200 in length
    The win percentage was 7.5% for resistance, so only 3 out of the 40 games were won by resistance.
    This gives the best results as it seperate the Resistance to the Spies clearly for the Bayes Classifier

    Apologies this is bad practise to have hard coded data but is essential for agent to be run in the tournament
    Otherwise I would store data in a csv and read it into the program.
'''
trainingDataLogicalSpy =[[20, 3.9999999999999996, 30, 0, 0, 0, 116, 7, 40, 0, 1], [14, 0.6666666666666666, 12, 10, 12, 0, 40, 5, 0, 0, 0], [10, 8.666666666666666, 18, 8, 13, 45, 12, 0, 12, 0, 0], 
[20, 1.5, 0, 0, 0, 0, 116, 12, 32, 0, 1], [4, 1.6666666666666665, 0, 2, 13, 45, 32, 2, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 3, 0, 156, 16, 32, 0, 1], [4, 0.6666666666666666, 12, 2, 20, 30, 48, 0, 48, 0, 0],
[14, 3.9999999999999996, 30, 8, 15, 0, 72, 0, 72, 0, 0], [10, 4.833333333333333, 18, 10, 21, 30, 0, 2, 0, 0, 0], [20, 4.833333333333333, 0, 0, 3, 0, 156, 7, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 10, 30, 116, 12, 40, 0, 1],
[20, 8.666666666666666, 12, 10, 20, 45, 92, 0, 40, 0, 0], [20, 1.5, 18, 0, 10, 30, 116, 13, 40, 0, 1], [14, 1.6666666666666665, 30, 2, 24, 60, 36, 2, 36, 0, 0], [14, 0.6666666666666666, 0, 8, 22, 45, 40, 5, 20, 0, 0],
[20, 1.5, 0, 0, 0, 0, 36, 11, 0, 0, 1], [20, 3.9999999999999996, 12, 0, 0, 0, 36, 8, 0, 4, 1], [10, 8.666666666666666, 18, 8, 9, 15, 12, 0, 12, 0, 0], [4, 0.6666666666666666, 0, 2, 9, 24, 16, 0, 16, 0, 0], 
[14, 1.6666666666666665, 30, 10, 8, 9, 20, 2, 20, 0, 0], [20, 3.9999999999999996, 0, 0, 8, 39, 108, 7, 40, 0, 1], [4, 0.6666666666666666, 12, 10, 21, 30, 40, 0, 40, 0, 0], [20, 8.666666666666666, 30, 10, 15, 72, 64, 0, 52, 0, 0],
[20, 1.5, 18, 0, 8, 39, 108, 17, 12, 6, 1], [4, 1.6666666666666665, 0, 0, 21, 99, 16, 2, 16, 0, 0], [4, 0.6666666666666666, 0, 16, 18, 99, 108, 12, 40, 0, 1], [4, 0.6666666666666666, 12, 2, 14, 45, 76, 3, 20, 0, 0],
[4, 0.6666666666666666, 0, 16, 18, 99, 108, 10, 52, 6, 1], [4, 0, 0, 8, 22, 87, 40, 2, 20, 0, 0], [4, 0, 0, 2, 24, 90, 0, 2, 0, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 176, 16, 40, 10, 1], [14, 3.9999999999999996, 57, 8, 16, 0, 60, 0, 60, 0, 0], 
[10, 8.666666666666666, 18, 10, 19, 30, 12, 0, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 176, 8, 32, 0, 1], [4, 0, 0, 2, 18, 45, 32, 2, 32, 0, 0], [20, 8.666666666666666, 30, 8, 7, 0, 52, 0, 40, 0, 0],
[4, 0.6666666666666666, 12, 10, 16, 15, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 92, 3, 24, 0, 1], [20, 1.5, 18, 0, 0, 0, 92, 15, 12, 0, 1], [4, 1.6666666666666665, 0, 2, 12, 30, 16, 2, 16, 0, 0], 
[14, 3.9999999999999996, 30, 8, 10, 0, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 12, 10, 13, 30, 12, 0, 0, 0, 0],[20, 3.9999999999999996, 0, 0, 0, 0, 76, 3, 12, 0, 1], [20, 1.5, 18, 0, 0, 0, 76, 15, 12, 0, 1], 
[4, 1.6666666666666665, 0, 2, 12, 30, 32, 2, 32, 0, 0], [10, 3.6666666666666665, 0, 8, 12, 30, 52, 0, 40, 0, 0], [14, 3.9999999999999996, 57, 8, 15, 30, 40, 0, 40, 0, 0],[20, 0.6666666666666666, 0, 0, 5, 30, 96, 13, 24, 0, 1],
[20, 4.833333333333333, 18, 0, 5, 30, 96, 6, 0, 0, 1], [4, 1.6666666666666665, 0, 2, 17, 75, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 3, 0, 152, 3, 60, 0, 1], [20, 3.9999999999999996, 57, 10, 13, 30, 60, 3, 60, 0, 0], 
[10, 3.9999999999999996, 0, 10, 15, 60, 12, 3, 12, 0, 0], [20, 1.5, 18, 0, 3, 0, 152, 17, 0, 0, 1], [10, 1.5, 0, 0, 13, 39, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 5, 15, 192, 8, 60, 0, 1], [14, 0.6666666666666666, 12, 10, 18, 45, 80, 5, 40, 0, 0], 
[20, 4.833333333333333, 63, 10, 20, 60, 40, 2, 40, 0, 0], [4, 3.9999999999999996, 0, 0, 23, 60, 32, 0, 32, 0, 0], [20, 1.5, 0, 0, 5, 15, 192, 17, 60, 0, 0], [20, 0.6666666666666666, 0, 0, 3, 0, 152, 16, 32, 0, 1],
[4, 0.6666666666666666, 12, 0, 19, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 30, 10, 16, 0, 52, 0, 52, 0, 0], [10, 4.833333333333333, 18, 10, 21, 30, 0, 2, 0, 0, 0],[20, 4.833333333333333, 0, 0, 3, 0, 152, 7, 32, 0, 0], 
[20, 3.9999999999999996, 0, 0, 0, 0, 72, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 10, 8, 0, 40, 5, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 72, 12, 0, 0, 1], [4, 3.9999999999999996, 0, 0, 8, 30, 32, 0, 32, 0, 0], 
[20, 4.833333333333333, 30, 10, 5, 0, 40, 2, 40, 0, 0],[10, 0.6666666666666666, 0, 0, 12, 30, 48, 3, 48, 0, 0], [20, 3.9999999999999996, 57, 10, 12, 0, 60, 3, 60, 4, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 136, 17, 12, 6, 1], 
[10, 4.833333333333333, 18, 10, 17, 30, 0, 2, 0, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 136, 5, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 124, 12, 20, 0, 1], [14, 3.9999999999999996, 57, 10, 17, 30, 40, 0, 40, 0, 0], 
[10, 3.6666666666666665, 18, 8, 18, 60, 12, 0, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 124, 8, 32, 0, 1], [4, 1.6666666666666665, 0, 2, 18, 60, 32, 2, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 164, 16, 60, 0, 1], 
[14, 3.9999999999999996, 57, 10, 17, 15, 40, 0, 40, 0, 0], [10, 1.5, 18, 10, 19, 30, 0, 2, 0, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 164, 8, 32, 0, 1], [4, 3.9999999999999996, 0, 0, 17, 30, 32, 0, 32, 0, 0],
[20, 0.6666666666666666, 0, 8, 13, 15, 80, 8, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 5, 15, 144, 8, 40, 0, 1], [20, 4.833333333333333, 63, 8, 18, 45, 40, 2, 40, 0, 0], [20, 1.5, 0, 0, 5, 15, 144, 17, 32, 0, 1], 
[10, 3.9999999999999996, 0, 2, 20, 60, 32, 3, 32, 0, 0], [10, 3.6666666666666665, 0, 8, 13, 30, 32, 0, 20, 0, 0], [14, 3.9999999999999996, 57, 10, 17, 30, 40, 0, 40, 0, 0], [20, 4.833333333333333, 18, 0, 5, 30, 104, 7, 0, 0, 1], 
[20, 0.6666666666666666, 0, 0, 5, 30, 104, 12, 32, 0, 1], [4, 1.6666666666666665, 0, 2, 18, 75, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 172, 8, 60, 0, 1], [14, 3.9999999999999996, 57, 10, 18, 45, 60, 0, 60, 0, 0], 
[20, 1.5, 18, 10, 15, 30, 40, 7, 0, 0, 0], [4, 3.9999999999999996, 0, 0, 18, 60, 32, 0, 32, 0, 0], [20, 1.5, 0, 0, 0, 0, 172, 17, 40, 10, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 7, 0, 0, 1], 
[4, 0.6666666666666666, 12, 10, 13, 15, 0, 0, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 8, 12, 0, 1], [4, 1.6666666666666665, 0, 2, 9, 30, 32, 2, 32, 0, 0],[20, 8.666666666666666, 30, 8, 4, 0, 52, 0, 40, 0, 0], 
[4, 0.6666666666666666, 0, 0, 16, 30, 48, 0, 48, 0, 0], [14, 7.333333333333333, 57, 10, 16, 0, 60, 0, 60, 0, 0], [10, 1.5, 18, 10, 18, 30, 0, 2, 0, 0, 0], [20, 8.166666666666666, 0, 0, 0, 0, 188, 7, 48, 0, 1],
[20, 7.333333333333333, 0, 0, 0, 0, 188, 7, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 3, 0, 144, 12, 60, 0, 1], [14, 3.9999999999999996, 57, 10, 16, 15, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 0, 10, 15, 45, 24, 0, 12, 0, 0], 
[20, 4.833333333333333, 18, 0, 3, 0, 144, 8, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 16, 69, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 10, 8, 0, 40, 5, 0, 0, 0],
[20, 1.5, 18, 0, 0, 0, 84, 12, 12, 0, 1], [10, 8.666666666666666, 0, 0, 5, 45, 44, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 10, 8, 0, 40, 2, 40, 0, 0], [4, 3.9999999999999996, 0, 8, 12, 15, 0, 0, 0, 0, 0], 
[20, 3.9999999999999996, 12, 0, 0, 0, 88, 4, 0, 0, 1], [20, 1.5, 18, 0, 0, 0, 88, 12, 0, 0, 1], [10, 1.5, 0, 2, 6, 30, 48, 2, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 7, 0, 40, 0, 40, 0, 0], 
[10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 2, 1, 0, 0, 4, 0, 0, 0], [10, 0, 0, 10, 5, 24, 0, 6, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 24, 0, 5, 0, 0, 0], 
[10, 3.9999999999999996, 0, 0, 17, 60, 48, 3, 48, 0, 0], [20, 3.9999999999999996, 12, 0, 3, 0, 180, 8, 40, 0, 1], [20, 3.9999999999999996, 30, 10, 14, 30, 72, 3, 72, 0, 0], [10, 1.5, 18, 8, 21, 39, 0, 2, 0, 0, 0], 
[20, 1.5, 0, 0, 3, 0, 180, 13, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 180, 7, 60, 0, 1], [14, 3.9999999999999996, 57, 10, 17, 15, 40, 0, 40, 0, 0],[20, 1.5, 18, 10, 14, 30, 40, 7, 0, 0, 0], 
[20, 1.5, 0, 0, 0, 0, 180, 17, 48, 0, 1], [4, 3.9999999999999996, 0, 0, 17, 60, 32, 0, 32, 0, 0], [20, 3.9999999999999996, 30, 0, 0, 0, 116, 7, 40, 0, 1], [14, 0.6666666666666666, 12, 10, 12, 0, 20, 5, 0, 0, 0],
[10, 8.666666666666666, 18, 8, 13, 45, 12, 0, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 116, 12, 32, 0, 1], [4, 1.6666666666666665, 0, 2, 13, 45, 32, 2, 32, 0, 0], [20, 1.5, 0, 0, 0, 0, 72, 11, 0, 0, 1], 
[20, 3.9999999999999996, 12, 0, 0, 0, 72, 4, 0, 4, 1], [20, 3.6666666666666665, 18, 8, 4, 0, 32, 5, 12, 0, 0], [4, 3.9999999999999996, 0, 2, 9, 54, 32, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 10, 8, 9, 40, 2, 40, 0, 0], 
[20, 3.9999999999999996, 0, 0, 0, 0, 36, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 10, 8, 0, 20, 5, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 36, 12, 0, 0, 1], [10, 8.666666666666666, 0, 0, 5, 30, 44, 0, 32, 0, 0], 
[14, 1.6666666666666665, 30, 10, 8, 0, 20, 2, 20, 0, 0],[0, 1.6666666666666665, 0, 8, 19, 96, 20, 0, 20, 0, 0], [20, 3.9999999999999996, 57, 0, 10, 60, 72, 4, 40, 4, 1], [20, 1.5, 18, 0, 10, 60, 72, 11, 0, 0, 1],
[4, 3.9999999999999996, 0, 2, 19, 114, 32, 0, 32, 0, 0], [20, 3.6666666666666665, 0, 10, 10, 15, 92, 5, 40, 0, 0], [4, 0.6666666666666666, 0, 0, 15, 15, 32, 0, 32, 0, 0], [14, 7.333333333333333, 57, 8, 14, 0, 60, 0, 60, 0, 0], 
[20, 7.333333333333333, 0, 0, 0, 0, 116, 8, 12, 0, 1], [10, 1.5, 18, 10, 17, 15, 0, 2, 0, 0, 0],[20, 8.166666666666666, 0, 0, 0, 0, 116, 10, 32, 0, 0], [4, 0.6666666666666666, 0, 8, 22, 60, 80, 0, 40, 0, 0], 
[4, 0.6666666666666666, 12, 10, 23, 90, 80, 0, 40, 0, 0], [10, 1.5, 18, 10, 15, 90, 152, 12, 60, 0, 1], [10, 1.5, 0, 2, 21, 120, 72, 2, 72, 0, 0], [10, 0.6666666666666666, 0, 10, 15, 90, 152, 12, 60, 0, 0], 
[20, 0.6666666666666666, 0, 8, 7, 0, 80, 8, 40, 0, 0], [20, 3.9999999999999996, 57, 10, 13, 39, 60, 3, 60, 4, 0], [20, 3.9999999999999996, 0, 0, 5, 30, 120, 4, 12, 0, 1], [20, 1.5, 18, 0, 5, 30, 120, 15, 0, 0, 1], 
[10, 4.833333333333333, 0, 0, 13, 84, 48, 2, 48, 0, 0], [10, 0.6666666666666666, 0, 8, 9, 15, 0, 3, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 108, 8, 0, 4, 1], [20, 1.5, 18, 0, 0, 0, 108, 7, 0, 0, 1], 
[10, 3.9999999999999996, 0, 2, 6, 30, 48, 3, 48, 0, 0], [20, 4.833333333333333, 30, 10, 5, 0, 60, 2, 60, 0, 0], [20, 3.9999999999999996, 0, 0, 3, 0, 136, 7, 32, 0, 1], [4, 3.9999999999999996, 12, 0, 19, 45, 48, 0, 48, 0, 0],
[14, 3.9999999999999996, 30, 10, 16, 0, 52, 0, 52, 0, 0], [20, 1.5, 18, 10, 16, 0, 40, 7, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 136, 16, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 108, 7, 20, 0, 1], 
[14, 3.9999999999999996, 57, 10, 17, 30, 40, 0, 40, 0, 0], [20, 3.6666666666666665, 18, 8, 13, 15, 52, 5, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 108, 17, 16, 0, 1], [4, 1.6666666666666665, 0, 2, 18, 75, 32, 2, 32, 0, 0], 
[20, 3.9999999999999996, 0, 0, 0, 0, 84, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 10, 8, 0, 40, 5, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 12, 12, 0, 1], [4, 1.6666666666666665, 0, 2, 9, 45, 32, 2, 32, 0, 0],
[20, 8.666666666666666, 30, 8, 4, 0, 52, 0, 40, 0, 0], [20, 8.666666666666666, 30, 8, 8, 0, 52, 0, 40, 0, 0], [4, 0.6666666666666666, 12, 10, 17, 15, 0, 0, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 132, 12, 12, 0, 1], 
[20, 3.9999999999999996, 0, 0, 0, 0, 132, 3, 48, 0, 1], [4, 1.6666666666666665, 0, 2, 13, 30, 32, 2, 32, 0, 0]]