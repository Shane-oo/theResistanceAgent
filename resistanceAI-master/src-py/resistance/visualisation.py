import numpy as np
import matplotlib.pyplot as plt


#VOTED_FOR_FAILED_MISSION = 0
#WENT_ON_FAILED_MISSION = 1
#PROP_TEAM_FAILED_MISSION = 2
#REJECTED_TEAM_SUCCESFUL_MISSION = 3 
#VOTED_AGAINST_TEAM_PROPOSAL = 4



dataset =[[20, 3.9999999999999996, 30, 0, 0, 0, 116, 7, 40, 0, 1], [14, 0.6666666666666666, 12, 10, 12, 0, 40, 5, 0, 0, 0], [10, 8.666666666666666, 18, 8, 13, 45, 12, 0, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 116, 12, 32, 0, 1], [4, 1.6666666666666665, 0, 2, 13, 45, 32, 2, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 3, 0, 156, 16, 32, 0, 1], [4, 0.6666666666666666, 12, 2, 20, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 15, 0, 72, 0, 72, 0, 0], [10, 4.833333333333333, 18, 10, 21, 30, 0, 2, 0, 0, 0], [20, 4.833333333333333, 0, 0, 3, 0, 156, 7, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 10, 30, 116, 12, 40, 0, 1], [20, 8.666666666666666, 12, 10, 20, 45, 92, 0, 40, 0, 0], [20, 1.5, 18, 0, 10, 30, 116, 13, 40, 0, 1], [14, 1.6666666666666665, 30, 2, 24, 60, 36, 2, 36, 0, 0], [14, 0.6666666666666666, 0, 8, 22, 45, 40, 5, 20, 0, 0], [20, 1.5, 0, 0, 0, 0, 36, 11, 0, 0, 1], [20, 3.9999999999999996, 12, 0, 0, 0, 36, 8, 0, 4, 1], [10, 8.666666666666666, 18, 8, 9, 15, 12, 0, 12, 0, 0], [4, 0.6666666666666666, 0, 2, 9, 24, 16, 0, 16, 0, 0], [14, 1.6666666666666665, 30, 10, 8, 9, 20, 2, 20, 0, 0], [20, 3.9999999999999996, 0, 0, 8, 39, 108, 7, 40, 0, 1], [4, 0.6666666666666666, 12, 10, 21, 30, 40, 0, 40, 0, 0], [20, 8.666666666666666, 30, 10, 15, 72, 64, 0, 52, 0, 0], [20, 1.5, 18, 0, 8, 39, 108, 17, 12, 6, 1], [4, 1.6666666666666665, 0, 0, 21, 99, 16, 2, 16, 0, 0], [4, 0.6666666666666666, 0, 16, 18, 99, 108, 12, 40, 0, 1], [4, 0.6666666666666666, 12, 2, 14, 45, 76, 3, 20, 0, 0], [4, 0.6666666666666666, 0, 16, 18, 99, 108, 10, 52, 6, 1], [4, 0, 0, 8, 22, 87, 40, 2, 20, 0, 0], [4, 0, 0, 2, 24, 90, 0, 2, 0, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 176, 16, 40, 10, 1], [14, 3.9999999999999996, 57, 8, 16, 0, 60, 0, 60, 0, 0], [10, 8.666666666666666, 18, 10, 19, 30, 12, 0, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 176, 8, 32, 0, 1], [4, 0, 0, 2, 18, 45, 32, 2, 32, 0, 0], [20, 8.666666666666666, 30, 8, 7, 0, 52, 0, 40, 0, 0], [4, 0.6666666666666666, 12, 10, 16, 15, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 92, 3, 24, 0, 1], [20, 1.5, 18, 0, 0, 0, 92, 15, 12, 0, 1], [4, 1.6666666666666665, 0, 2, 12, 30, 16, 2, 16, 0, 0], [14, 3.9999999999999996, 30, 8, 10, 0, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 12, 10, 13, 30, 12, 0, 0, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 76, 3, 12, 0, 1], [20, 1.5, 18, 0, 0, 0, 76, 15, 12, 0, 1], [4, 1.6666666666666665, 0, 2, 12, 30, 32, 2, 32, 0, 0], [10, 3.6666666666666665, 0, 8, 12, 30, 52, 0, 40, 0, 0], [14, 3.9999999999999996, 57, 8, 15, 30, 40, 0, 40, 0, 0], [20, 0.6666666666666666, 0, 0, 5, 30, 96, 13, 24, 0, 1], [20, 4.833333333333333, 18, 0, 5, 30, 96, 6, 0, 0, 1], [4, 1.6666666666666665, 0, 2, 17, 75, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 3, 0, 152, 3, 60, 0, 1], [20, 3.9999999999999996, 57, 10, 13, 30, 60, 3, 60, 0, 0], [10, 3.9999999999999996, 0, 10, 15, 60, 12, 3, 12, 0, 0], [20, 1.5, 18, 0, 3, 0, 152, 17, 0, 0, 1], [10, 1.5, 0, 0, 13, 39, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 5, 15, 192, 8, 60, 0, 1], [14, 0.6666666666666666, 12, 10, 18, 45, 80, 5, 40, 0, 0], [20, 4.833333333333333, 63, 10, 20, 60, 40, 2, 40, 0, 0], [4, 3.9999999999999996, 0, 0, 23, 60, 32, 0, 32, 0, 0], [20, 1.5, 0, 0, 5, 15, 192, 17, 60, 0, 0], [20, 0.6666666666666666, 0, 0, 3, 0, 152, 16, 32, 0, 1], [4, 0.6666666666666666, 12, 0, 19, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 30, 10, 16, 0, 52, 0, 52, 0, 0], [10, 4.833333333333333, 18, 10, 21, 30, 0, 2, 0, 0, 0], [20, 4.833333333333333, 0, 0, 3, 0, 152, 7, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 72, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 10, 8, 0, 40, 5, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 72, 12, 0, 0, 1], [4, 3.9999999999999996, 0, 0, 8, 30, 32, 0, 32, 0, 0], [20, 4.833333333333333, 30, 10, 5, 0, 40, 2, 40, 0, 0], [10, 0.6666666666666666, 0, 0, 12, 30, 48, 3, 48, 0, 0], [20, 3.9999999999999996, 57, 10, 12, 0, 60, 3, 60, 4, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 136, 17, 12, 6, 1], [10, 4.833333333333333, 18, 10, 17, 30, 0, 2, 0, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 136, 5, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 124, 12, 20, 0, 1], [14, 3.9999999999999996, 57, 10, 17, 30, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 60, 12, 0, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 124, 8, 32, 0, 1], [4, 1.6666666666666665, 0, 2, 18, 60, 32, 2, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 164, 16, 60, 0, 1], [14, 3.9999999999999996, 57, 10, 17, 15, 40, 0, 40, 0, 0], [10, 1.5, 18, 10, 19, 30, 0, 2, 0, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 164, 8, 32, 0, 1], [4, 3.9999999999999996, 0, 0, 17, 30, 32, 0, 32, 0, 0], [20, 0.6666666666666666, 0, 8, 13, 15, 80, 8, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 5, 15, 144, 8, 40, 0, 1], [20, 4.833333333333333, 63, 8, 18, 45, 40, 2, 40, 0, 0], [20, 1.5, 0, 0, 5, 15, 144, 17, 32, 0, 1], [10, 3.9999999999999996, 0, 2, 20, 60, 32, 3, 32, 0, 0], [10, 3.6666666666666665, 0, 8, 13, 30, 32, 0, 20, 0, 0], [14, 3.9999999999999996, 57, 10, 17, 30, 40, 0, 40, 0, 0], [20, 4.833333333333333, 18, 0, 5, 30, 104, 7, 0, 0, 1], [20, 0.6666666666666666, 0, 0, 5, 30, 104, 12, 32, 0, 1], [4, 1.6666666666666665, 0, 2, 18, 75, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 172, 8, 60, 0, 1], [14, 3.9999999999999996, 57, 10, 18, 45, 60, 0, 60, 0, 0], [20, 1.5, 18, 10, 15, 30, 40, 7, 0, 0, 0], [4, 3.9999999999999996, 0, 0, 18, 60, 32, 0, 32, 0, 0], [20, 1.5, 0, 0, 0, 0, 172, 17, 40, 10, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 7, 0, 0, 1], [4, 0.6666666666666666, 12, 10, 13, 15, 0, 0, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 8, 12, 0, 1], [4, 1.6666666666666665, 0, 2, 9, 30, 32, 2, 32, 0, 0], [20, 8.666666666666666, 30, 8, 4, 0, 52, 0, 40, 0, 0], [4, 0.6666666666666666, 0, 0, 16, 30, 48, 0, 48, 0, 0], [14, 7.333333333333333, 57, 10, 16, 0, 60, 0, 60, 0, 0], [10, 1.5, 18, 10, 18, 30, 0, 2, 0, 0, 0], [20, 8.166666666666666, 0, 0, 0, 0, 188, 7, 48, 0, 1], [20, 7.333333333333333, 0, 0, 0, 0, 188, 7, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 3, 0, 144, 12, 60, 0, 1], [14, 3.9999999999999996, 57, 10, 16, 15, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 0, 10, 15, 45, 24, 0, 12, 0, 0], [20, 4.833333333333333, 18, 0, 3, 0, 144, 8, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 16, 69, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 10, 8, 0, 40, 5, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 12, 12, 0, 1], [10, 8.666666666666666, 0, 0, 5, 45, 44, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 10, 8, 0, 40, 2, 40, 0, 0], [4, 3.9999999999999996, 0, 8, 12, 15, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 88, 4, 0, 0, 1], [20, 1.5, 18, 0, 0, 0, 88, 12, 0, 0, 1], [10, 1.5, 0, 2, 6, 30, 48, 2, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 7, 0, 40, 0, 40, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 3, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 1.6666666666666665, 0, 2, 1, 0, 0, 4, 0, 0, 0], [10, 0, 0, 10, 5, 24, 0, 6, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 24, 0, 5, 0, 0, 0], [10, 3.9999999999999996, 0, 0, 17, 60, 48, 3, 48, 0, 0], [20, 3.9999999999999996, 12, 0, 3, 0, 180, 8, 40, 0, 1], [20, 3.9999999999999996, 30, 10, 14, 30, 72, 3, 72, 0, 0], [10, 1.5, 18, 8, 21, 39, 0, 2, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 180, 13, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 180, 7, 60, 0, 1], [14, 3.9999999999999996, 57, 10, 17, 15, 40, 0, 40, 0, 0], [20, 1.5, 18, 10, 14, 30, 40, 7, 0, 0, 0], [20, 1.5, 0, 0, 0, 0, 180, 17, 48, 0, 1], [4, 3.9999999999999996, 0, 0, 17, 60, 32, 0, 32, 0, 0], [20, 3.9999999999999996, 30, 0, 0, 0, 116, 7, 40, 0, 1], [14, 0.6666666666666666, 12, 10, 12, 0, 20, 5, 0, 0, 0], [10, 8.666666666666666, 18, 8, 13, 45, 12, 0, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 116, 12, 32, 0, 1], [4, 1.6666666666666665, 0, 2, 13, 45, 32, 2, 32, 0, 0], [20, 1.5, 0, 0, 0, 0, 72, 11, 0, 0, 1], [20, 3.9999999999999996, 12, 0, 0, 0, 72, 4, 0, 4, 1], [20, 3.6666666666666665, 18, 8, 4, 0, 32, 5, 12, 0, 0], [4, 3.9999999999999996, 0, 2, 9, 54, 32, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 10, 8, 9, 40, 2, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 36, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 10, 8, 0, 20, 5, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 36, 12, 0, 0, 1], [10, 8.666666666666666, 0, 0, 5, 30, 44, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 10, 8, 0, 20, 2, 20, 0, 0], [0, 1.6666666666666665, 0, 8, 19, 96, 20, 0, 20, 0, 0], [20, 3.9999999999999996, 57, 0, 10, 60, 72, 4, 40, 4, 1], [20, 1.5, 18, 0, 10, 60, 72, 11, 0, 0, 1], [4, 3.9999999999999996, 0, 2, 19, 114, 32, 0, 32, 0, 0], [20, 3.6666666666666665, 0, 10, 10, 15, 92, 5, 40, 0, 0], [4, 0.6666666666666666, 0, 0, 15, 15, 32, 0, 32, 0, 0], [14, 7.333333333333333, 57, 8, 14, 0, 60, 0, 60, 0, 0], [20, 7.333333333333333, 0, 0, 0, 0, 116, 8, 12, 0, 1], [10, 1.5, 18, 10, 17, 15, 0, 2, 0, 0, 0], [20, 8.166666666666666, 0, 0, 0, 0, 116, 10, 32, 0, 0], [4, 0.6666666666666666, 0, 8, 22, 60, 80, 0, 40, 0, 0], [4, 0.6666666666666666, 12, 10, 23, 90, 80, 0, 40, 0, 0], [10, 1.5, 18, 10, 15, 90, 152, 12, 60, 0, 1], [10, 1.5, 0, 2, 21, 120, 72, 2, 72, 0, 0], [10, 0.6666666666666666, 0, 10, 15, 90, 152, 12, 60, 0, 0], [20, 0.6666666666666666, 0, 8, 7, 0, 80, 8, 40, 0, 0], [20, 3.9999999999999996, 57, 10, 13, 39, 60, 3, 60, 4, 0], [20, 3.9999999999999996, 0, 0, 5, 30, 120, 4, 12, 0, 1], [20, 1.5, 18, 0, 5, 30, 120, 15, 0, 0, 1], [10, 4.833333333333333, 0, 0, 13, 84, 48, 2, 48, 0, 0], [10, 0.6666666666666666, 0, 8, 9, 15, 0, 3, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 108, 8, 0, 4, 1], [20, 1.5, 18, 0, 0, 0, 108, 7, 0, 0, 1], [10, 3.9999999999999996, 0, 2, 6, 30, 48, 3, 48, 0, 0], [20, 4.833333333333333, 30, 10, 5, 0, 60, 2, 60, 0, 0], [20, 3.9999999999999996, 0, 0, 3, 0, 136, 7, 32, 0, 1], [4, 3.9999999999999996, 12, 0, 19, 45, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 30, 10, 16, 0, 52, 0, 52, 0, 0], [20, 1.5, 18, 10, 16, 0, 40, 7, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 136, 16, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 108, 7, 20, 0, 1], [14, 3.9999999999999996, 57, 10, 17, 30, 40, 0, 40, 0, 0], [20, 3.6666666666666665, 18, 8, 13, 15, 52, 5, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 108, 17, 16, 0, 1], [4, 1.6666666666666665, 0, 2, 18, 75, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 10, 8, 0, 40, 5, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 12, 12, 0, 1], [4, 1.6666666666666665, 0, 2, 9, 45, 32, 2, 32, 0, 0], [20, 8.666666666666666, 30, 8, 4, 0, 52, 0, 40, 0, 0], [20, 8.666666666666666, 30, 8, 8, 0, 52, 0, 40, 0, 0], [4, 0.6666666666666666, 12, 10, 17, 15, 0, 0, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 132, 12, 12, 0, 1], [20, 3.9999999999999996, 0, 0, 0, 0, 132, 3, 48, 0, 1], [4, 1.6666666666666665, 0, 2, 13, 30, 32, 2, 32, 0, 0]]
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


print(len(idk[0]))
print(len(idk[1]))

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
x6ForZeros = []
x6ForOnes = []
x7ForZeros = []
x7ForOnes = []
x8ForZeros = []
x8ForOnes = []
x9ForZeros = []
x9ForOnes = []
x10ForZeros = []
x10ForOnes = []


sizeOfOnes = len(idk[1])
index = 0
for arrs in idk[0]:
    #if(index== sizeOfOnes):
     #   break
    x1ForZeros.append(arrs[0])
    x2ForZeros.append(arrs[1])
    x3ForZeros.append(arrs[2])
    x4ForZeros.append(arrs[3])
    x5ForZeros.append(arrs[4])
    x6ForZeros.append(arrs[5])
    x7ForZeros.append(arrs[6])
    x8ForZeros.append(arrs[7])
    x9ForZeros.append(arrs[8])
    x10ForZeros.append(arrs[9])
    index+=1
for arrs in idk[1]:
    x1ForOnes.append(arrs[0])
    x2ForOnes.append(arrs[1])
    x3ForOnes.append(arrs[2])
    x4ForOnes.append(arrs[3])
    x5ForOnes.append(arrs[4])
    x6ForOnes.append(arrs[5])
    x7ForOnes.append(arrs[6])
    x8ForOnes.append(arrs[7])
    x9ForOnes.append(arrs[8])
    x10ForOnes.append(arrs[9])

print(len(x1ForOnes),len(x1ForZeros))
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
plt.xlabel("Voted For Failed Missions", size=14)
plt.ylabel("Count", size=14)
plt.hist(x1ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x1ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Voted For Failed Missions: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Voted For Failed Missions.png")
plt.show()

fig = plt.figure()


plt.xlabel("Went On Failed Missions", size=14)
plt.ylabel("Count", size=14)
plt.hist(x2ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x2ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Went On Failed Missions: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Went On Failed Missions.png")
plt.show()



fig = plt.figure()
plt.xlabel("Proposed Teams That Failed", size=14)
plt.ylabel("Count", size=14)
plt.hist(x3ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x3ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Proposed Teams That Failed: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Proposed Teams That Failed.png")
plt.show()


fig = plt.figure()
plt.xlabel("Voted No for Successful Missions", size=14)
plt.ylabel("Count", size=14)
plt.hist(x4ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x4ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Voted No for Successful Missions: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Voted No for Successful Missions.png")
plt.show()
fig = plt.figure()


plt.xlabel("Times Rejected Teams", size=14)
plt.ylabel("Count", size=14)
plt.hist(x5ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x5ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Voted Against Team Proposal:  Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Votes No.png")
plt.show()

plt.xlabel("Votes Against Team That Has Successful Members", size=14)
plt.ylabel("Count", size=14)
plt.hist(x6ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x6ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Voted Against Team That Has Successful Members: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Voted Against Team That Has Successful Members.png")
plt.show()

plt.xlabel("Votes For Team That Has UnSuccessful Members", size=14)
plt.ylabel("Count", size=14)
plt.hist(x7ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x7ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Voted For Team That Has UnSuccessful Members: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Voted For Team That Has UnSuccessful Members.png")
plt.show()

plt.xlabel("Votes For A Mission They Arent On", size=14)
plt.ylabel("Count", size=14)
plt.hist(x8ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x8ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Voted For A Mission They Arent On: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Voted For A Mission They Arent On.png")
plt.show()

plt.xlabel("Proposes For Team With Unsuccessful Members", size=14)
plt.ylabel("Count", size=14)
plt.hist(x9ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x9ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Proposed For Team With Unsuccessful Members: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Proposed For Team With Unsuccessful Members.png")
plt.show()

plt.xlabel("Proposes For Team With No SuccessFul Members", size=14)
plt.ylabel("Count", size=14)
plt.hist(x10ForZeros,bins=100,alpha = 1.0, label="resitance",color='b')
plt.hist(x10ForOnes,bins=100,alpha = 1.0, label="spies",color='r')
plt.title("Proposes For Team With No SuccessFul Members: Agents Vs Logical Resistance Agents")
plt.legend(loc='upper right')
plt.savefig("Proposes For Team With No SuccessFul Members.png")
plt.show()


