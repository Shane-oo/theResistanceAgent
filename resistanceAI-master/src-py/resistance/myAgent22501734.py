from agent import Agent
import random


# Global variables
#indexs of varibales in dataset
VOTED_FOR_FAILED_MISSION = 0#
WENT_ON_FAILED_MISSION = 1#
PROP_TEAM_FAILED_MISSION = 2#
REJECTED_TEAM_SUCCESFUL_MISSION = 3 #
VOTED_AGAINST_TEAM_PROPOSAL = 4
IS_SPY = 5

# Logical playing Agent

class myAgent(Agent):        


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
                    resistanceTable.append([0,0,0,0,0,0])
                    
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
            # If agent was asked on mission and declined it is very suss
            # extra sussness if multiple mission members vote no
            missionMembersDeclining = 0
            for agents in mission:
                if agents not in votes:
                    missionMembersDeclining +=1
            for agents in mission:
                if agents not in votes:
                    if agents == self.player_number:
                        continue
                    self.resistanceData[agents][VOTED_AGAINST_TEAM_PROPOSAL] += missionMembersDeclining
            
            for i in range(self.number_of_players):
                # if agent votes no for mission its suss
                if i == self.player_number:
                        continue
                if i not in votes:
                    self.resistanceData[i][VOTED_AGAINST_TEAM_PROPOSAL] += self.number_of_players/(self.number_of_players-len(votes))
                    # If they say not to teams that contatin successful mission members its suss
                    SuccessfulMissionsMembers = sum(el in self.wentOnSuccessfulMissions for el in mission)
                    self.resistanceData[i][VOTED_AGAINST_TEAM_PROPOSAL] += SuccessfulMissionsMembers

                if i in votes:
                    # If they vote yes for a mission that contains members that prevousily failed missions its suss
                    failedPriorMissionsMembers = sum(el in self.wentOnFailedMissions for el in mission)
                    self.resistanceData[i][VOTED_AGAINST_TEAM_PROPOSAL] += failedPriorMissionsMembers
                
                if (i in votes and i not in mission):
                    # voted for a mission they are not on
                    self.resistanceData[i][VOTED_AGAINST_TEAM_PROPOSAL] += 1
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
    
                    if i not in self.agentsWhoVoted and i is not self.player_number:
                        # Increases sussness if agent did not want a successful mission to happen
                        amountThatVotedAgainst = self.number_of_players-len(self.agentsWhoVoted)
                        self.resistanceData[i][REJECTED_TEAM_SUCCESFUL_MISSION] += amountThatVotedAgainst/self.number_of_players
                
            # failed mission
            else:
                self.spyWins += 1
                
                for agent in self.agentsWhoVoted:
                    if(agent is not self.player_number):
                        # Increase sussness if agent most liekly voted knowing mission would fail
                        self.resistanceData[agent][VOTED_FOR_FAILED_MISSION]+= len(self.agentsWhoVoted)/self.number_of_players
                # Increment the amounts that add to untrustworthyness
            
                if(proposer is not self.player_number):

                    self.propFailedMissions.append(proposer)
                    propFailedMissionsCount = self.propFailedMissions.count(proposer)
                    if(propFailedMissionsCount == 0):
                        propFailedMissionsCount = 1
                    # increment by one or by how many times agent has proposed failed mission    
                    self.resistanceData[proposer][PROP_TEAM_FAILED_MISSION] += propFailedMissionsCount
                    if(proposer in mission):
                        self.resistanceData[proposer][PROP_TEAM_FAILED_MISSION] += (betrayals)/len(mission)

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
                        if(self.player_number in mission):
                            sussMembers = len(mission) - 1
                        else:
                            sussMembers = len(mission)

                        self.resistanceData[agent][WENT_ON_FAILED_MISSION] += failedMissionsCount*(betrayals/sussMembers)

        print(self.resistanceData)
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