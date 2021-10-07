import numpy as np
import matplotlib.pyplot as plt


#VOTED_FOR_FAILED_MISSION = 0
#WENT_ON_FAILED_MISSION = 1
#PROP_TEAM_FAILED_MISSION = 2
#REJECTED_TEAM_SUCCESFUL_MISSION = 3 
#VOTED_AGAINST_TEAM_PROPOSAL = 4



dataset = [

    
    
    [0.9, 0, 0, 0.8, 33.33333333333333, 1],
 [0.9, 0.25, 1.25, 0.8, 20.333333333333336, 1],
  [0.9, 0.25, 0, 0, 13.555555555555555, 0], 
  [0, 0.25, 0, 0, 28.555555555555557, 0], 
  [0.9, 0.25, 0, 0, 12.555555555555554, 1],
   [0.9, 0, 0, 0.8, 33.33333333333333, 0],
    [0.9, 0, 0, 0, 20.666666666666668, 0],
     [0.9, 0, 0, 0, 10.666666666666666, 1],
      [0.9, 0, 0, 0.8, 20.333333333333336, 0], 
      [0.9, 0, 0, 0, 23.666666666666668, 0],

[1.0, 0.2, 0, 0, 45.333333333333336, 0],
 [1.7, 0.25, 1.25, 0.4, 12.5, 1],
  [1.0, 0.2, 0, 0, 45.333333333333336, 0],
   [1.7, 0.25, 0, 0, 13.0, 0], 
   [1.7, 0, 0, 0.4, 14.5, 1],
    [1.7, 0.2, 0, 0.4, 14.5, 1],
     [1.0, 0.65, 0, 0, 30.333333333333332, 0], 
     [1.7, 0, 0, 0.4, 12.5, 1], 
     [1.7, 0.65, 1.2, 0, 26.0, 0],
      [1.7, 0, 0, 0, 30.0, 0],
    
    [1.0, 0.25, 0, 0.8, 16.0, 1],
     [1.0, 0.25, 1.25, 0, 16.333333333333336, 0],
      [1.0, 0.25, 0, 0, 17.333333333333332, 0],
       [1.0, 0.25, 0, 0, 13.333333333333332, 0], 
       [1.0, 0, 0, 0.8, 20.0, 1],
        [1.0, 0, 0, 0, 20.333333333333332, 0], 
        [1.0, 0, 0, 0, 20.333333333333332, 0], 
        [1.0, 0, 0, 0.8, 20.0, 1],
         [1.0, 0, 0, 0, 14.333333333333332, 0],
          [1.0, 0, 0, 0.8, 16.0, 1],

          [2.0, 0.25, 0, 0, 49.111111111111114, 0], 
          [2.0, 0.25, 1.25, 0.4, 39.72222222222222, 1],
           [2.0, 0.3333333333333333, 0, 0.4, 39.72222222222222, 1], 
           [2.0, 0.25, 0, 0, 45.11111111111111, 0], 
           [2.0, 0.3333333333333333, 1.25, 0, 48.22222222222222, 0], 
           [2.0, 0.3333333333333333, 0, 0, 55.22222222222222, 0], 
           [2.0, 0.25, 0, 0, 55.22222222222222, 0],
            [2.0, 0.25, 0, 0, 48.22222222222222, 0],
             [2.0, 0, 0, 0.4, 49.72222222222223, 1], 
             [2.0, 0, 0, 0.4, 49.72222222222223, 1],

             [2.0, 0.25, 0, 0.4, 37.52777777777778, 0],
              [2.0, 0.75, 1.25, 0.4, 43.527777777777786, 0],
               [2.0, 0.75, 1.2, 0.4, 30.97222222222222, 1], 
               [2.0, 0, 0, 0.4, 56.63888888888889, 0], 
               [2.0, 0, 0, 0.4, 45.97222222222223, 1],
                [2.0, 0, 0, 0.4, 45.97222222222223, 1], 
                [2.0, 0.75, 0, 0, 36.888888888888886, 0], 
                [2.0, 0.25, 0, 0, 35.138888888888886, 0], 
                [2.0, 0.25, 0, 0.4, 37.388888888888886, 0],
                 [2.0, 0, 0, 0.4, 30.97222222222222, 1],

                [1.7, 0.3333333333333333, 0, 0.4, 35.5, 1],
                [1.7, 0.25, 1.25, 0.4, 35.5, 1],
                [1.7, 0, 0, 0.4, 37.5, 1],
                 [1.7, 0, 0, 0.4, 37.5, 1],
                  [1.0, 0, 0, 0.8, 25.11111111111111, 1],
                  [1.0, 0, 0, 0.8, 25.11111111111111, 1],
                  [1.0, 0, 0, 0.8, 18.11111111111111, 1],
                  [1.0, 0.25, 0, 0.8, 18.11111111111111, 1],
                   [1.0, 0.3333333333333333, 1.25, 0.8, 28.333333333333332, 1],
                   [1.0, 0, 0, 0.8, 43.33333333333333, 1]
   ]

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

idk = separate_by_class(dataset)
print(idk[1][0][0])

print(len(idk[0]))

y1 = [0,1,2,3,4,5]
x1ForZeros = []
x1ForOnes = []
x2ForZeros = []
x2ForOnes = []
x3ForZeros = []
x3ForOnes = []
x4ForZeros = []
x4ForOnes = []
x5ForZeros = []
x5ForOnes = []

for arrs in idk[0]:
    x1ForZeros.append(arrs[0])
    x2ForZeros.append(arrs[1])
    x3ForZeros.append(arrs[2])
    x4ForZeros.append(arrs[3])
    x5ForZeros.append(arrs[4])
for arrs in idk[1]:
    x1ForOnes.append(arrs[0])
    x2ForOnes.append(arrs[1])
    x3ForOnes.append(arrs[2])
    x4ForOnes.append(arrs[3])
    x5ForOnes.append(arrs[4])

'''
fig = plt.figure()
plt.scatter(x1ForZeros,x4ForZeros, c='b', marker='x', label='Resistance')
plt.scatter(x1ForOnes, x4ForOnes, c='r', marker='s', label='Spys')
fig.suptitle('Voted for Failed mIssion VS Rejected Team Successful Mission ', fontsize=10)
plt.legend()
plt.show()

fig = plt.figure()
plt.scatter(x3ForZeros,x2ForZeros, c='b', marker='x', label='Resistance')
plt.scatter(x3ForOnes, x2ForOnes, c='r', marker='s', label='Spys')
fig.suptitle('Proposed Team Failed Mission VS Went on Failed Mission ', fontsize=10)
plt.legend()
plt.show()

fig = plt.figure()
plt.scatter(x5ForZeros,x4ForZeros, c='b', marker='x', label='Resistance')
plt.scatter(x5ForOnes, x4ForOnes, c='r', marker='s', label='Spys')
fig.suptitle('Voted Against Team Proposal VS Rejected Team Successful Mission ', fontsize=10)
plt.legend()
plt.show()

'''
fig = plt.figure()

plt.xlabel("Times Rejected Teams", size=14)
plt.ylabel("Count", size=14)
plt.hist(x4ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x4ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Rejected Team That Was on Successful Mission: Logical Spy Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.show()

fig = plt.figure()
plt.xlabel("Voted For Failed Missions", size=14)
plt.ylabel("Count", size=14)
plt.hist(x1ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x1ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Voted For Failed Missions: Logical Spy Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Voted For Failed Missions.png")
plt.show()

fig = plt.figure()


plt.xlabel("Went On Failed Missions", size=14)
plt.ylabel("Count", size=14)
plt.hist(x2ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x2ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Went On Failed Missions: Logical Spy Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Went On Failed Missions.png")
plt.show()



fig = plt.figure()
plt.xlabel("Proposed Teams That Failed", size=14)
plt.ylabel("Count", size=14)
plt.hist(x3ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x3ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Proposed Teams That Failed: Logical Spy Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Proposed Teams That Failed.png")
plt.show()


fig = plt.figure()
plt.xlabel("Voted No for Successful Missions", size=14)
plt.ylabel("Count", size=14)
plt.hist(x3ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x3ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Voted No for Successful Missions: Logical Spy Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Voted No for Successful Missions.png")
plt.show()
