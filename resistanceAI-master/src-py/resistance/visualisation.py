import numpy as np
import matplotlib.pyplot as plt


#VOTED_FOR_FAILED_MISSION = 0
#WENT_ON_FAILED_MISSION = 1
#PROP_TEAM_FAILED_MISSION = 2
#REJECTED_TEAM_SUCCESFUL_MISSION = 3 
#VOTED_AGAINST_TEAM_PROPOSAL = 4



dataset = [[4, 3.9999999999999996, 0, 0, 15, 30, 32, 0, 32, 0, 0], [14, 3.9999999999999996, 57, 8, 14, 0, 40, 1, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 132, 7, 12, 0, 1], [20, 1.5, 18, 8, 11, 0, 40, 8, 0, 0, 0], [20, 1.5, 0, 0, 0, 0, 132, 15, 48, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 136, 12, 40, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 15, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 45, 12, 1, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 136, 8, 32, 0, 1], [4, 1.6666666666666665, 0, 0, 17, 45, 32, 3, 32, 0, 0], [4, 3.9999999999999996, 0, 8, 22, 75, 40, 0, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 5, 30, 172, 12, 60, 0, 1], [20, 4.833333333333333, 63, 8, 19, 75, 40, 3, 40, 0, 0], [4, 0.6666666666666666, 0, 0, 23, 90, 32, 1, 32, 0, 0], [20, 1.5, 0, 0, 5, 30, 172, 17, 40, 0, 0], [4, 0.6666666666666666, 0, 16, 24, 90, 136, 16, 52, 0, 1], [4, 0.6666666666666666, 12, 0, 26, 45, 88, 0, 32, 0, 0], [4, 0.6666666666666666, 0, 16, 24, 90, 136, 13, 68, 8, 1], [4, 0, 0, 0, 30, 102, 0, 3, 0, 0, 0], [4, 0, 0, 8, 29, 87, 52, 6, 20, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 124, 7, 20, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 30, 40, 0, 40, 0, 0], [20, 3.6666666666666665, 18, 8, 13, 15, 52, 6, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 124, 17, 32, 0, 1], [4, 1.6666666666666665, 0, 0, 17, 75, 32, 3, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 8, 7, 0, 20, 6, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 12, 12, 0, 1], [10, 8.666666666666666, 0, 0, 5, 45, 44, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 8, 7, 0, 40, 3, 40, 0, 0], [10, 0.6666666666666666, 0, 10, 15, 90, 132, 12, 60, 0, 1], [4, 0.6666666666666666, 12, 8, 22, 75, 80, 1, 40, 0, 0], [10, 1.5, 18, 10, 15, 90, 132, 12, 40, 0, 1], [10, 1.5, 0, 0, 20, 105, 72, 3, 72, 0, 0], [4, 0.6666666666666666, 0, 8, 22, 75, 80, 0, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 112, 7, 40, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 30, 40, 1, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 60, 12, 0, 12, 0, 0], [20, 1.5, 0, 0, 0, 0, 112, 17, 16, 0, 1], [4, 1.6666666666666665, 0, 0, 17, 60, 16, 3, 16, 0, 0], [4, 1.6666666666666665, 0, 8, 20, 81, 20, 2, 20, 0, 0], [20, 3.9999999999999996, 12, 0, 8, 15, 124, 4, 40, 0, 1], [20, 8.666666666666666, 30, 8, 14, 30, 64, 0, 52, 0, 0], [20, 1.5, 18, 0, 8, 15, 124, 17, 12, 0, 1], [4, 0.6666666666666666, 0, 0, 21, 45, 32, 1, 32, 0, 0], [0, 0, 0, 8, 14, 51, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 104, 4, 0, 4, 1], [20, 1.5, 18, 0, 0, 0, 104, 11, 12, 0, 1], [10, 8.666666666666666, 0, 0, 5, 30, 44, 1, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 7, 9, 60, 1, 60, 0, 0], [14, 3.9999999999999996, 30, 8, 12, 15, 60, 0, 60, 0, 0], [10, 8.666666666666666, 12, 8, 14, 60, 12, 1, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 104, 17, 12, 0, 1], [4, 0, 0, 0, 13, 60, 32, 3, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 104, 3, 20, 0, 0], [20, 3.9999999999999996, 0, 0, 3, 0, 152, 7, 48, 0, 1], [4, 3.9999999999999996, 12, 0, 19, 45, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 15, 0, 52, 1, 52, 0, 0], [20, 1.5, 18, 8, 15, 0, 40, 8, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 152, 16, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 10, 0, 60, 0, 60, 0, 0], [14, 0.6666666666666666, 12, 8, 10, 0, 40, 5, 0, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 120, 4, 12, 0, 1], [20, 1.5, 18, 0, 0, 0, 120, 15, 0, 0, 1], [10, 4.833333333333333, 0, 0, 8, 45, 48, 3, 48, 0, 0], [10, 1.5, 0, 10, 15, 90, 56, 11, 20, 0, 1], [10, 0.6666666666666666, 12, 10, 15, 90, 56, 13, 20, 4, 1], [10, 3.6666666666666665, 18, 8, 19, 102, 52, 1, 32, 0, 0], [4, 0.6666666666666666, 0, 0, 23, 99, 36, 1, 36, 0, 0], [0, 0, 0, 8, 24, 81, 40, 0, 20, 0, 0], [4, 0.6666666666666666, 0, 8, 22, 87, 40, 0, 20, 0, 0], [10, 0.6666666666666666, 12, 10, 15, 90, 88, 13, 40, 4, 1], [10, 1.5, 18, 10, 15, 90, 88, 12, 32, 6, 1], [10, 3.6666666666666665, 0, 0, 20, 90, 48, 1, 36, 0, 0], [4, 0, 0, 8, 22, 72, 40, 2, 20, 0, 0], [10, 0.6666666666666666, 0, 10, 18, 99, 112, 12, 40, 0, 1], [10, 0.6666666666666666, 12, 8, 22, 90, 80, 4, 40, 0, 0], [10, 0.6666666666666666, 0, 8, 19, 60, 92, 4, 52, 0, 0], [10, 1.5, 18, 10, 18, 99, 112, 12, 40, 0, 1], [10, 1.5, 0, 0, 23, 99, 72, 2, 72, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 128, 16, 40, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 15, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 45, 12, 1, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 128, 8, 32, 0, 1], [4, 1.6666666666666665, 0, 0, 17, 45, 16, 3, 16, 0, 0], [20, 3.9999999999999996, 30, 8, 9, 15, 40, 3, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 5, 15, 72, 8, 0, 4, 1], [20, 1.5, 18, 0, 5, 15, 72, 7, 0, 0, 1], [10, 3.9999999999999996, 0, 0, 10, 30, 32, 4, 32, 0, 0], [10, 1.5, 0, 8, 9, 15, 40, 3, 40, 0, 0], [4, 1.3333333333333333, 0, 16, 24, 90, 152, 16, 52, 0, 1], [4, 1.3333333333333333, 12, 0, 26, 57, 88, 0, 32, 0, 0], [4, 1.3333333333333333, 0, 16, 24, 90, 152, 13, 84, 0, 1], [4, 0, 0, 0, 30, 129, 48, 3, 36, 0, 0], [4, 0, 0, 8, 29, 99, 52, 6, 20, 0, 0], [4, 1.6666666666666665, 0, 8, 12, 42, 0, 2, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 52, 3, 0, 0, 1], [20, 1.5, 18, 0, 0, 0, 52, 12, 0, 6, 1], [4, 0.6666666666666666, 0, 0, 8, 30, 32, 1, 32, 0, 0], [20, 8.666666666666666, 30, 8, 4, 0, 52, 1, 40, 0, 0], [4, 3.9999999999999996, 0, 0, 21, 45, 32, 0, 32, 0, 0], [14, 0.6666666666666666, 12, 8, 15, 0, 80, 6, 40, 0, 0], [20, 4.833333333333333, 63, 8, 17, 15, 40, 3, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 5, 15, 136, 7, 32, 0, 1], [20, 1.5, 0, 0, 5, 15, 136, 16, 32, 0, 0], [20, 0.6666666666666666, 0, 8, 4, 0, 40, 8, 0, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 72, 13, 0, 0, 1], [10, 4.833333333333333, 18, 8, 9, 30, 0, 2, 0, 0, 0], [10, 3.9999999999999996, 0, 0, 5, 30, 32, 4, 32, 0, 0], [20, 4.833333333333333, 30, 0, 0, 0, 72, 3, 40, 0, 0], [16, 0, 0, 8, 9, 27, 0, 8, 0, 0, 0], [16, 1.6666666666666665, 30, 8, 14, 57, 0, 4, 0, 0, 0], [16, 4.833333333333333, 18, 0, 5, 15, 56, 1, 0, 0, 0], [16, 1.6666666666666665, 0, 4, 7, 36, 20, 9, 0, 0, 1], [16, 1.5, 0, 4, 7, 36, 20, 9, 20, 0, 0], [20, 3.9999999999999996, 0, 0, 8, 30, 152, 11, 32, 0, 1], [4, 0.6666666666666666, 12, 0, 24, 45, 32, 1, 32, 0, 0], [4, 3.9999999999999996, 0, 8, 20, 15, 52, 0, 52, 0, 0], [20, 4.833333333333333, 63, 8, 20, 30, 40, 3, 40, 0, 0], [20, 1.5, 0, 0, 8, 30, 152, 16, 48, 0, 0], [14, 3.9999999999999996, 30, 0, 31, 105, 108, 0, 108, 0, 0], [14, 0.6666666666666666, 12, 8, 30, 45, 80, 6, 40, 0, 0], [20, 4.833333333333333, 18, 8, 27, 75, 100, 3, 40, 0, 0], [20, 4.833333333333333, 0, 0, 10, 60, 284, 12, 88, 0, 1], [20, 0.6666666666666666, 0, 0, 10, 60, 284, 21, 88, 0, 0], [10, 1.5, 0, 10, 15, 90, 96, 11, 40, 0, 1], [10, 0.6666666666666666, 12, 10, 15, 90, 96, 13, 40, 0, 1], [10, 3.6666666666666665, 18, 8, 19, 90, 92, 1, 52, 0, 0], [4, 0, 0, 0, 23, 99, 36, 3, 36, 0, 0], [4, 0.6666666666666666, 0, 8, 22, 69, 40, 0, 20, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 156, 12, 40, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 15, 40, 1, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 30, 12, 0, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 156, 8, 32, 0, 1], [4, 1.6666666666666665, 0, 0, 17, 60, 32, 3, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 12, 30, 60, 0, 60, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 128, 17, 0, 0, 1], [10, 1.5, 18, 8, 14, 60, 0, 3, 0, 0, 0], [4, 3.9999999999999996, 0, 0, 13, 60, 48, 1, 48, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 128, 3, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 3, 0, 0, 1], [14, 0.6666666666666666, 12, 8, 7, 0, 40, 6, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 12, 12, 0, 1], [10, 8.666666666666666, 0, 0, 5, 45, 44, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 8, 7, 0, 40, 3, 40, 0, 0], [14, 3.9999999999999996, 30, 8, 11, 0, 40, 0, 40, 0, 0], [14, 0.6666666666666666, 12, 8, 11, 0, 40, 6, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 120, 16, 0, 0, 1], [20, 3.9999999999999996, 0, 0, 0, 0, 120, 3, 48, 0, 1], [10, 4.833333333333333, 0, 0, 9, 30, 32, 3, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 3, 0, 152, 12, 32, 0, 1], [4, 3.9999999999999996, 12, 0, 19, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 15, 0, 52, 1, 52, 0, 0], [10, 1.5, 18, 8, 20, 15, 0, 3, 0, 0, 0], [20, 4.833333333333333, 0, 0, 3, 0, 152, 7, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 11, 0, 40, 0, 40, 0, 0], [4, 3.9999999999999996, 12, 8, 16, 15, 0, 1, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 104, 16, 0, 0, 1], [20, 3.9999999999999996, 0, 0, 0, 0, 104, 3, 32, 0, 1], [10, 1.5, 0, 0, 9, 15, 32, 3, 32, 0, 0], [4, 0, 0, 8, 22, 72, 40, 2, 20, 0, 0], [10, 0.6666666666666666, 12, 10, 15, 90, 76, 12, 40, 0, 1], [10, 1.5, 18, 10, 15, 90, 76, 12, 20, 6, 1], [4, 0.6666666666666666, 0, 0, 23, 90, 36, 1, 36, 0, 0], [10, 3.6666666666666665, 0, 8, 19, 87, 52, 1, 20, 0, 0], [6, 0, 0, 0, 5, 15, 0, 3, 0, 0, 0], [16, 4.833333333333333, 0, 0, 0, 0, 20, 5, 0, 0, 0], [16, 1.5, 18, 4, 2, 6, 20, 10, 0, 0, 1], [6, 1.6666666666666665, 0, 0, 5, 30, 0, 3, 0, 0, 0], [16, 1.6666666666666665, 30, 4, 2, 6, 20, 4, 20, 0, 0], [10, 4.833333333333333, 0, 0, 11, 48, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 57, 0, 6, 18, 72, 3, 40, 0, 1], [10, 3.9999999999999996, 0, 8, 12, 30, 12, 4, 12, 0, 0], [20, 0.6666666666666666, 0, 8, 7, 9, 52, 9, 12, 0, 0], [20, 1.5, 18, 0, 6, 18, 72, 12, 0, 0, 0], [14, 3.9999999999999996, 30, 8, 11, 0, 40, 0, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 116, 12, 0, 0, 1], [10, 3.6666666666666665, 18, 8, 13, 15, 12, 1, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 116, 7, 32, 0, 1], [4, 1.6666666666666665, 0, 0, 12, 30, 32, 3, 32, 0, 0], [4, 3.9999999999999996, 0, 0, 16, 15, 32, 0, 32, 0, 0], [14, 3.9999999999999996, 57, 8, 15, 0, 60, 1, 60, 0, 0], [10, 1.5, 18, 8, 17, 15, 0, 3, 0, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 136, 16, 32, 0, 1], [20, 4.833333333333333, 0, 0, 0, 0, 136, 11, 32, 0, 0], [16, 1.5, 0, 0, 0, 0, 16, 5, 0, 0, 0], [16, 1.6666666666666665, 0, 8, 4, 24, 0, 4, 0, 0, 0], [16, 1.5, 18, 4, 2, 6, 16, 10, 0, 0, 1], [16, 1.6666666666666665, 0, 0, 0, 0, 16, 3, 16, 0, 0], [16, 1.6666666666666665, 30, 4, 2, 6, 16, 8, 0, 0, 0], [20, 4.833333333333333, 0, 0, 10, 60, 116, 11, 40, 0, 1], [20, 0.6666666666666666, 12, 0, 10, 60, 116, 18, 40, 0, 1], [20, 8.666666666666666, 18, 8, 19, 75, 92, 1, 52, 0, 0], [14, 1.6666666666666665, 30, 0, 23, 114, 36, 3, 36, 0, 0], [14, 0.6666666666666666, 0, 8, 22, 84, 40, 5, 20, 0, 0], [20, 1.5, 0, 0, 5, 15, 88, 11, 40, 10, 1], [20, 3.9999999999999996, 57, 0, 5, 15, 88, 9, 20, 0, 1], [20, 3.6666666666666665, 18, 8, 14, 15, 32, 5, 12, 0, 0], [4, 3.9999999999999996, 0, 0, 18, 99, 32, 1, 32, 0, 0], [4, 1.6666666666666665, 0, 8, 17, 39, 20, 3, 20, 0, 0], [16, 1.6666666666666665, 0, 8, 4, 12, 0, 3, 0, 0, 0], [16, 1.5, 0, 0, 0, 0, 16, 6, 0, 0, 0], [16, 1.5, 18, 4, 2, 12, 0, 10, 0, 6, 1], [16, 1.6666666666666665, 0, 4, 2, 12, 0, 4, 0, 0, 1], [16, 1.6666666666666665, 30, 8, 4, 12, 0, 3, 0, 0, 0], [4, 0.6666666666666666, 0, 0, 20, 60, 48, 0, 48, 0, 0], [20, 3.9999999999999996, 12, 0, 3, 0, 160, 7, 40, 0, 1], [14, 3.9999999999999996, 30, 8, 16, 30, 52, 1, 52, 0, 0], [10, 4.833333333333333, 18, 8, 21, 60, 0, 3, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 160, 17, 32, 0, 0], [10, 1.5, 0, 0, 26, 108, 72, 2, 72, 0, 0], [10, 0.6666666666666666, 12, 10, 21, 108, 112, 12, 40, 0, 1], [10, 0.6666666666666666, 0, 8, 22, 84, 92, 4, 52, 0, 0], [10, 0.6666666666666666, 0, 8, 22, 69, 92, 4, 52, 0, 0], [10, 1.5, 18, 10, 21, 108, 112, 12, 40, 0, 0], [0, 1.6666666666666665, 0, 8, 14, 51, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 68, 4, 0, 4, 1], [20, 1.5, 18, 0, 0, 0, 68, 11, 12, 0, 1], [4, 0.6666666666666666, 0, 0, 8, 24, 32, 1, 32, 0, 0], [20, 8.666666666666666, 30, 8, 4, 12, 52, 1, 40, 0, 0], [20, 1.5, 0, 0, 10, 60, 152, 16, 40, 0, 1], [20, 3.9999999999999996, 12, 0, 10, 60, 152, 13, 40, 0, 1], [20, 1.5, 18, 8, 19, 60, 80, 8, 40, 0, 0], [20, 3.9999999999999996, 30, 0, 20, 105, 92, 4, 92, 0, 0], [20, 3.9999999999999996, 0, 8, 19, 60, 80, 3, 40, 0, 0], [14, 3.9999999999999996, 30, 8, 12, 24, 40, 0, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 5, 15, 84, 4, 0, 0, 1], [20, 1.5, 18, 0, 5, 15, 84, 11, 12, 0, 1], [10, 3.6666666666666665, 0, 0, 10, 30, 44, 1, 32, 0, 0], [4, 1.6666666666666665, 0, 8, 12, 39, 20, 3, 20, 0, 0], [4, 0.6666666666666666, 0, 0, 15, 15, 32, 0, 32, 0, 0], [14, 3.9999999999999996, 57, 8, 14, 0, 40, 1, 40, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 116, 7, 12, 0, 1], [10, 4.833333333333333, 18, 8, 16, 15, 0, 3, 0, 0, 0], [20, 1.5, 0, 0, 0, 0, 116, 15, 32, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 4, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 9, 0, 4, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 1, 0, 0, 0], [10, 0, 0, 10, 5, 9, 0, 6, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 9, 0, 4, 0, 0, 0], [4, 1.6666666666666665, 0, 0, 19, 63, 32, 2, 32, 0, 0], [20, 3.9999999999999996, 12, 0, 6, 18, 112, 3, 40, 0, 1], [14, 3.9999999999999996, 30, 8, 15, 36, 52, 1, 52, 0, 0], [10, 3.6666666666666665, 0, 8, 17, 30, 24, 1, 12, 0, 0], [20, 1.5, 18, 0, 6, 18, 112, 13, 0, 6, 0], [6, 0, 0, 8, 9, 39, 0, 3, 0, 0, 0], [6, 1.6666666666666665, 0, 8, 9, 39, 0, 4, 0, 0, 0], [16, 1.5, 18, 4, 2, 12, 36, 10, 0, 0, 1], [16, 4.833333333333333, 0, 0, 0, 0, 36, 0, 16, 0, 0], [16, 1.6666666666666665, 30, 4, 2, 12, 36, 8, 20, 0, 0], [14, 3.9999999999999996, 30, 8, 11, 9, 40, 0, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 88, 13, 0, 0, 1], [10, 3.6666666666666665, 18, 8, 13, 15, 12, 1, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 88, 6, 16, 0, 1], [4, 1.6666666666666665, 0, 0, 12, 39, 32, 3, 32, 0, 0], [14, 1.6666666666666665, 0, 8, 25, 96, 40, 2, 20, 0, 0], [20, 3.9999999999999996, 12, 0, 13, 69, 116, 12, 40, 0, 1], [14, 0.6666666666666666, 0, 8, 22, 87, 52, 6, 32, 0, 0], [20, 1.5, 18, 0, 13, 69, 116, 17, 40, 6, 1], [20, 8.666666666666666, 30, 0, 23, 105, 84, 1, 72, 0, 0], [4, 1.3333333333333333, 0, 16, 24, 90, 80, 16, 32, 0, 1], [4, 1.3333333333333333, 12, 0, 26, 57, 88, 0, 32, 0, 0], [4, 1.3333333333333333, 0, 16, 24, 90, 80, 13, 48, 8, 1], [4, 0, 0, 0, 30, 90, 0, 3, 0, 0, 0], [4, 0, 0, 8, 29, 72, 0, 6, 0, 0, 0], [20, 7.333333333333333, 0, 0, 3, 0, 172, 7, 48, 0, 1], [4, 0.6666666666666666, 12, 0, 19, 30, 48, 1, 48, 0, 0], [14, 7.333333333333333, 30, 8, 15, 0, 72, 0, 72, 0, 0], [10, 1.5, 18, 8, 20, 30, 0, 3, 0, 0, 0], [20, 8.166666666666666, 0, 0, 3, 0, 172, 7, 32, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 4, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 4, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0], [10, 0, 0, 10, 5, 15, 0, 6, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 0], [14, 1.6666666666666665, 30, 8, 10, 21, 40, 2, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 3, 0, 84, 9, 0, 0, 1], [4, 0.6666666666666666, 0, 8, 12, 15, 12, 0, 12, 0, 0], [20, 4.833333333333333, 18, 0, 3, 0, 84, 7, 12, 0, 1], [10, 8.666666666666666, 0, 0, 8, 15, 44, 1, 32, 0, 0], [4, 3.9999999999999996, 0, 0, 20, 75, 48, 0, 48, 0, 0], [20, 3.9999999999999996, 12, 0, 3, 0, 180, 7, 60, 0, 1], [14, 3.9999999999999996, 30, 8, 16, 30, 52, 1, 52, 0, 0], [20, 1.5, 18, 8, 16, 30, 40, 8, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 180, 17, 48, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 196, 16, 60, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 30, 40, 1, 40, 0, 0], [10, 4.833333333333333, 18, 8, 18, 30, 0, 3, 0, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 196, 8, 48, 0, 1], [4, 0.6666666666666666, 0, 0, 17, 60, 48, 0, 48, 0, 0], [4, 3.9999999999999996, 0, 0, 20, 60, 48, 0, 48, 0, 0], [20, 0.6666666666666666, 12, 0, 3, 0, 180, 13, 40, 0, 1], [14, 3.9999999999999996, 30, 8, 16, 30, 72, 0, 72, 0, 0], [10, 1.5, 18, 8, 21, 30, 0, 3, 0, 0, 0], [20, 4.833333333333333, 0, 0, 3, 0, 180, 8, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 10, 0, 40, 0, 40, 0, 0], [20, 3.6666666666666665, 12, 8, 7, 0, 52, 6, 0, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 108, 3, 24, 0, 1], [20, 1.5, 18, 0, 0, 0, 108, 15, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 11, 30, 16, 3, 16, 0, 0], [0, 1.6666666666666665, 0, 8, 14, 51, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 52, 4, 0, 4, 1], [20, 1.5, 18, 0, 0, 0, 52, 11, 0, 0, 1], [4, 0.6666666666666666, 0, 0, 8, 39, 32, 1, 32, 0, 0], [20, 8.666666666666666, 30, 8, 4, 12, 52, 1, 40, 0, 0], [10, 1.5, 0, 10, 15, 90, 132, 11, 60, 0, 1], [10, 0.6666666666666666, 12, 10, 15, 90, 132, 13, 40, 4, 1], [6, 1.5, 18, 8, 21, 75, 80, 0, 40, 0, 0], [10, 0.6666666666666666, 0, 0, 20, 105, 72, 4, 72, 0, 0], [10, 0.6666666666666666, 0, 8, 19, 60, 80, 4, 40, 0, 0], [20, 3.9999999999999996, 30, 0, 3, 9, 48, 3, 20, 0, 1], [4, 3.9999999999999996, 12, 8, 15, 30, 0, 1, 0, 0, 0], [20, 3.6666666666666665, 0, 8, 4, 12, 44, 6, 12, 0, 0], [20, 1.5, 18, 0, 3, 9, 48, 12, 12, 6, 1], [4, 1.6666666666666665, 0, 0, 11, 39, 16, 2, 16, 0, 0], [20, 8.666666666666666, 30, 8, 7, 0, 52, 0, 40, 0, 0], [4, 0.6666666666666666, 12, 8, 15, 24, 0, 1, 0, 4, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 48, 8, 12, 6, 1], [20, 1.5, 18, 0, 0, 0, 48, 14, 0, 0, 1], [4, 1.6666666666666665, 0, 0, 11, 24, 16, 3, 16, 0, 0], [4, 0.6666666666666666, 0, 16, 24, 90, 80, 16, 32, 0, 1], [4, 0.6666666666666666, 12, 0, 26, 57, 88, 0, 32, 0, 0], [4, 0.6666666666666666, 0, 16, 24, 90, 80, 13, 48, 0, 1], [4, 0, 0, 0, 30, 102, 0, 3, 0, 0, 0], [4, 0, 0, 8, 29, 84, 0, 6, 0, 0, 0], [20, 3.9999999999999996, 0, 0, 3, 0, 152, 7, 32, 0, 1], [4, 3.9999999999999996, 12, 0, 19, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 15, 0, 52, 1, 52, 0, 0], [10, 1.5, 18, 8, 20, 15, 0, 3, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 152, 16, 48, 0, 0], [6, 1.6666666666666665, 0, 0, 5, 30, 0, 3, 0, 0, 0], [16, 4.833333333333333, 0, 0, 0, 0, 20, 5, 0, 0, 0], [16, 1.5, 18, 4, 2, 12, 0, 10, 0, 6, 1], [6, 0, 0, 0, 5, 30, 0, 3, 0, 0, 0], [16, 1.6666666666666665, 30, 4, 2, 12, 0, 4, 0, 0, 0], [20, 0.6666666666666666, 0, 0, 10, 60, 136, 16, 20, 0, 1], [14, 0.6666666666666666, 12, 8, 21, 15, 80, 6, 40, 0, 0], [10, 8.666666666666666, 18, 8, 23, 90, 32, 0, 32, 0, 0], [20, 4.833333333333333, 30, 0, 10, 60, 136, 8, 72, 0, 1], [4, 1.6666666666666665, 0, 0, 27, 120, 32, 3, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 3, 0, 168, 7, 48, 0, 1], [4, 3.9999999999999996, 12, 0, 19, 30, 48, 0, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 15, 0, 52, 1, 52, 0, 0], [10, 1.5, 18, 8, 20, 30, 0, 3, 0, 0, 0], [20, 1.5, 0, 0, 3, 0, 168, 12, 32, 0, 0], [4, 0.6666666666666666, 0, 8, 15, 30, 40, 0, 40, 0, 0], [14, 7.333333333333333, 57, 8, 15, 15, 60, 1, 60, 0, 0], [20, 7.333333333333333, 0, 0, 5, 15, 104, 3, 12, 0, 1], [20, 8.166666666666666, 18, 0, 5, 15, 104, 10, 0, 0, 1], [10, 1.5, 0, 0, 13, 30, 32, 3, 32, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 7, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0], [10, 0, 0, 10, 5, 15, 0, 6, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 15, 0, 5, 0, 0, 0], [14, 1.6666666666666665, 0, 8, 25, 111, 40, 2, 20, 0, 0], [20, 3.9999999999999996, 12, 0, 13, 69, 116, 12, 40, 0, 1], [14, 0.6666666666666666, 0, 8, 22, 102, 52, 6, 32, 0, 0], [20, 1.5, 18, 0, 13, 69, 116, 17, 40, 6, 1], [20, 8.666666666666666, 30, 0, 23, 90, 84, 1, 72, 0, 0], [4, 3.9999999999999996, 0, 8, 12, 30, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 88, 3, 0, 0, 1], [20, 1.5, 18, 0, 0, 0, 88, 12, 0, 0, 1], [10, 1.5, 0, 0, 5, 30, 48, 3, 48, 0, 0], [14, 3.9999999999999996, 30, 8, 7, 0, 40, 1, 40, 0, 0], [20, 1.5, 0, 0, 0, 0, 108, 7, 0, 0, 1], [20, 3.9999999999999996, 12, 0, 0, 0, 108, 4, 0, 0, 1], [10, 1.5, 18, 8, 9, 15, 0, 3, 0, 0, 0], [10, 3.9999999999999996, 0, 0, 5, 30, 48, 3, 48, 0, 0], [20, 3.9999999999999996, 30, 8, 4, 0, 60, 4, 60, 0, 0], [10, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 4, 0, 0, 0], [10, 1.6666666666666665, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 10, 5, 30, 0, 6, 0, 0, 1], [10, 1.6666666666666665, 30, 10, 5, 30, 0, 5, 0, 0, 0], [4, 3.9999999999999996, 0, 8, 12, 15, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 12, 0, 0, 0, 92, 8, 0, 0, 1], [20, 1.5, 18, 0, 0, 0, 92, 8, 0, 0, 1], [4, 0.6666666666666666, 0, 0, 8, 15, 48, 0, 48, 0, 0], [20, 4.833333333333333, 30, 8, 4, 0, 60, 3, 60, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 128, 16, 40, 10, 1], [14, 3.9999999999999996, 57, 8, 16, 0, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 45, 12, 1, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 128, 8, 32, 0, 1], [4, 1.6666666666666665, 0, 0, 17, 30, 16, 3, 16, 0, 0], [16, 1.5, 0, 0, 0, 0, 16, 5, 0, 0, 0], [16, 1.6666666666666665, 0, 8, 4, 24, 0, 4, 0, 0, 0], [16, 1.5, 18, 4, 2, 6, 16, 10, 0, 0, 1], [16, 1.6666666666666665, 0, 0, 0, 0, 16, 3, 16, 0, 0], [16, 1.6666666666666665, 30, 4, 2, 6, 16, 8, 0, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 116, 12, 20, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 30, 40, 0, 40, 0, 0], [10, 3.6666666666666665, 18, 8, 18, 60, 12, 1, 12, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 116, 8, 32, 0, 1], [4, 1.6666666666666665, 0, 0, 17, 60, 32, 3, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 10, 60, 128, 16, 20, 0, 1], [14, 0.6666666666666666, 12, 8, 26, 60, 40, 5, 20, 0, 0], [20, 8.666666666666666, 18, 8, 23, 75, 92, 1, 52, 0, 0], [20, 1.5, 0, 0, 10, 60, 128, 17, 72, 0, 1], [14, 1.6666666666666665, 30, 0, 27, 90, 36, 3, 36, 0, 0], [20, 8.666666666666666, 30, 8, 7, 0, 52, 0, 40, 0, 0], [4, 0.6666666666666666, 12, 8, 15, 30, 0, 0, 0, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 96, 4, 12, 0, 1], [20, 1.5, 18, 0, 0, 0, 96, 11, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 11, 30, 32, 3, 32, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 176, 16, 40, 0, 1], [14, 3.9999999999999996, 57, 8, 16, 15, 40, 1, 40, 0, 0], [10, 4.833333333333333, 18, 8, 18, 45, 0, 3, 0, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 176, 8, 48, 0, 1], [4, 0.6666666666666666, 0, 0, 17, 45, 48, 0, 48, 0, 0], [10, 0.6666666666666666, 0, 10, 15, 90, 96, 12, 40, 0, 1], [4, 0.6666666666666666, 12, 8, 22, 60, 40, 1, 20, 0, 0], [10, 1.5, 18, 10, 15, 90, 96, 12, 40, 0, 1], [10, 3.6666666666666665, 0, 0, 20, 120, 84, 0, 72, 0, 0], [4, 0, 0, 8, 22, 60, 40, 3, 20, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 84, 2, 0, 0, 1], [20, 0.6666666666666666, 12, 0, 0, 0, 84, 13, 0, 0, 1], [10, 3.6666666666666665, 18, 8, 9, 30, 12, 1, 12, 0, 0], [4, 3.9999999999999996, 0, 0, 8, 39, 32, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 8, 7, 9, 20, 3, 20, 0, 0], [20, 0.6666666666666666, 0, 0, 0, 0, 72, 12, 0, 0, 1], [14, 0.6666666666666666, 12, 8, 7, 0, 40, 6, 0, 0, 0], [10, 4.833333333333333, 18, 8, 9, 45, 0, 3, 0, 0, 0], [4, 3.9999999999999996, 0, 0, 8, 30, 32, 0, 32, 0, 0], [20, 4.833333333333333, 30, 0, 0, 0, 72, 3, 40, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 48, 2, 0, 0, 1], [20, 0.6666666666666666, 12, 0, 0, 0, 48, 13, 0, 4, 1], [10, 3.6666666666666665, 18, 8, 9, 30, 12, 1, 12, 0, 0], [4, 3.9999999999999996, 0, 0, 8, 39, 32, 0, 32, 0, 0], [14, 1.6666666666666665, 30, 8, 7, 9, 20, 3, 20, 0, 0], [4, 0.6666666666666666, 0, 16, 24, 90, 132, 16, 32, 0, 1], [4, 0.6666666666666666, 12, 0, 26, 54, 88, 0, 32, 0, 0], [4, 0.6666666666666666, 0, 16, 24, 90, 132, 13, 84, 0, 1], [4, 0, 0, 0, 30, 114, 48, 3, 36, 0, 0], [4, 0, 0, 8, 29, 99, 0, 6, 0, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 84, 3, 0, 0, 1], [20, 3.6666666666666665, 12, 8, 4, 0, 52, 6, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 84, 12, 12, 0, 1], [4, 1.6666666666666665, 0, 0, 8, 30, 16, 3, 16, 0, 0], [14, 3.9999999999999996, 30, 8, 7, 0, 40, 0, 40, 0, 0], [4, 0.6666666666666666, 0, 8, 22, 75, 80, 0, 40, 0, 0], [10, 0.6666666666666666, 12, 10, 15, 90, 144, 12, 40, 0, 1], [10, 1.5, 18, 10, 15, 90, 144, 12, 72, 0, 1], [10, 3.6666666666666665, 0, 0, 20, 105, 84, 1, 72, 0, 0], [4, 0, 0, 8, 22, 60, 40, 3, 20, 0, 0], [4, 3.9999999999999996, 0, 0, 20, 75, 48, 0, 48, 0, 0], [14, 0.6666666666666666, 12, 8, 14, 0, 80, 5, 40, 0, 0], [20, 3.9999999999999996, 30, 0, 5, 30, 152, 8, 72, 0, 1], [10, 4.833333333333333, 18, 8, 21, 75, 0, 3, 0, 0, 0], [20, 1.5, 0, 0, 5, 30, 152, 15, 32, 0, 0], [14, 3.9999999999999996, 30, 8, 12, 30, 60, 0, 60, 0, 0], [20, 0.6666666666666666, 12, 0, 5, 15, 72, 12, 0, 0, 1], [20, 4.833333333333333, 18, 0, 5, 15, 72, 3, 0, 0, 1], [4, 3.9999999999999996, 0, 0, 13, 45, 32, 1, 32, 0, 0], [10, 1.5, 0, 8, 9, 30, 40, 3, 40, 0, 0], [10, 1.6666666666666665, 30, 8, 14, 51, 40, 0, 40, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 124, 18, 0, 4, 1], [10, 8.666666666666666, 18, 8, 14, 30, 12, 1, 12, 0, 0], [4, 0.6666666666666666, 0, 0, 13, 39, 32, 1, 32, 0, 0], [20, 4.833333333333333, 0, 0, 0, 0, 124, 2, 40, 0, 0], [10, 3.6666666666666665, 0, 8, 9, 30, 12, 0, 0, 0, 0], [20, 0.6666666666666666, 12, 0, 0, 0, 84, 13, 0, 0, 1], [20, 4.833333333333333, 18, 0, 0, 0, 84, 2, 12, 0, 1], [4, 3.9999999999999996, 0, 0, 8, 39, 32, 1, 32, 0, 0], [14, 1.6666666666666665, 30, 8, 7, 9, 20, 3, 20, 0, 0], [20, 8.666666666666666, 30, 8, 9, 15, 52, 0, 40, 0, 0], [4, 0.6666666666666666, 12, 8, 17, 45, 0, 1, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 92, 13, 0, 0, 1], [4, 1.6666666666666665, 0, 0, 13, 45, 32, 3, 32, 0, 0], [20, 3.9999999999999996, 0, 0, 0, 0, 92, 7, 40, 0, 0], [4, 3.9999999999999996, 0, 0, 21, 30, 32, 0, 32, 0, 0], [4, 0.6666666666666666, 12, 8, 20, 15, 40, 1, 40, 0, 0], [20, 4.833333333333333, 63, 8, 17, 30, 60, 3, 60, 0, 0], [20, 3.9999999999999996, 0, 0, 5, 15, 152, 11, 48, 0, 1], [20, 1.5, 0, 0, 5, 15, 152, 12, 32, 0, 0], [20, 8.666666666666666, 30, 8, 7, 21, 52, 0, 40, 0, 0], [20, 3.9999999999999996, 12, 0, 3, 9, 68, 4, 0, 0, 1], [4, 0.6666666666666666, 0, 8, 12, 42, 12, 1, 12, 0, 0], [20, 1.5, 18, 0, 3, 9, 68, 12, 12, 6, 1], [4, 1.6666666666666665, 0, 0, 11, 39, 16, 2, 16, 0, 0], [20, 0.6666666666666666, 0, 0, 10, 60, 132, 21, 40, 0, 1], [14, 0.6666666666666666, 12, 8, 26, 75, 40, 5, 20, 0, 0], [20, 8.666666666666666, 18, 8, 23, 75, 92, 1, 52, 0, 0], [20, 4.833333333333333, 0, 0, 10, 60, 132, 12, 56, 0, 1], [14, 1.6666666666666665, 30, 0, 27, 105, 36, 3, 36, 0, 0], [20, 3.9999999999999996, 0, 0, 5, 15, 156, 11, 40, 10, 1], [4, 0.6666666666666666, 12, 8, 21, 15, 40, 0, 40, 0, 0], [20, 8.666666666666666, 63, 8, 18, 15, 52, 1, 52, 0, 0], [20, 1.5, 0, 0, 5, 15, 156, 13, 32, 0, 1], [4, 1.6666666666666665, 0, 0, 22, 45, 16, 3, 16, 0, 0], [14, 3.9999999999999996, 30, 8, 11, 0, 60, 0, 60, 0, 0], [14, 0.6666666666666666, 12, 8, 11, 0, 40, 6, 0, 0, 0], [20, 1.5, 18, 0, 0, 0, 140, 16, 0, 0, 1], [20, 3.9999999999999996, 0, 0, 0, 0, 140, 3, 32, 0, 1], [10, 4.833333333333333, 0, 0, 9, 45, 48, 3, 48, 0, 0], [4, 0.6666666666666666, 0, 16, 24, 90, 80, 16, 32, 0, 1], [4, 0.6666666666666666, 12, 0, 26, 54, 88, 0, 32, 0, 0], [4, 0.6666666666666666, 0, 16, 24, 90, 80, 13, 48, 0, 1], [4, 0, 0, 0, 30, 132, 0, 3, 0, 0, 0], [4, 0, 0, 8, 29, 114, 0, 6, 0, 0, 0]]

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
    if(index== sizeOfOnes):
        break
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


