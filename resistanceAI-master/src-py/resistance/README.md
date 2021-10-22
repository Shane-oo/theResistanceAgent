22/10/2021 
CITS3001 Project - Shane Monck 22501734

My agent for the tournament is in the myAgent22501734.py files and is named bayesAgent
For example: from myAgent22501734 import bayesAgent

For proof of testing and validation of figures in my report please use the __main__.py file in the zip folder.
It features the ability to run x amount of games and calcualtes how many wins each spy or resistance got in those games as well as
calculating the accuracy of the predictions made by my agents.

To validate my trainingAgent if wanted to just replace the bayesAgent with the trainingAgent, 
lines 35, and 64 to 92 would simply have to be commented out otherwise an error would be thrown
as these are used in determining prediction accuracy but the trainingAgent does not have that.
Also uncomment line 93 to display the all the data on the terminal, be warned depending on the amount of games this can be quite big.
My training data uses GAMES_TO_PLAY = 40 if wanting to validate.
