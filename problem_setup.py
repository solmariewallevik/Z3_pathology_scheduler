import random
'''
# Set up the problem data
slices = [1,4,6,11,25,2,3,35,44,100] #number of slices
num_samples = len(slices) #number of samples
num_doctors = 3 #number of doctors
max_points_per_doctor = 24 #the max amount of points for a doctor to have

samples = [f"sample_{i}" for i in range(num_samples)]
doctors = [f"doctor_{i}" for i in range(num_doctors)] 

# points that each sample/section has
# key = points, value = number of sections per sample
point_table = {
    1 : [1,2,3,4,5],
    2 : [6,7,8,9,10],
    3 : [11,12,13,14,15],
    4 : [16,17,18,19,20],
    5 : [21,22,23,24,25],
    6 : [26,27,28,29,30],
    7 : [31,32,33,34,35],
    8 : [36,37,38,39,40],
    9 : [41,42,43,44,45],
    10 : [46,47,48,49,50],
    11 : [51,52,53,54,55],
    12 : [56,57,58,59,60],
    13 : [61,62,63,64,65],
    14 : [66,67,68,69,70],
    15 : [71,72,73,74,75],
    16 : [76,77,78,79,80],
    17 : [81,82,83,84,85],
    18 : [86,87,88,89,90],
    19 : [91,92,93,94,95],
    20 : [96,97,98,99,100],
    21 : [101,102,103,104,105],
    22 : [106,107,108,108,110]
    }

#FAGGRUPPER. Each doctor has 1 or 2 (some have 3 and some none).
spes_table = {
    'u': 'Urogruppen',
    'x': 'Gynogruppen',
    'p': 'Perinatalgruppen',
    'm': 'Mammagruppen',
    'g': 'Gastrogruppen',
    'h': 'Hudgruppen',
    'l': 'Lymfomgruppen',
    's': 'Sarkomgruppen',
    'r': '�re-nese-hals-gruppen',
    'y': 'Nyregrupper',
    'oral': 'oral',
    'nevro': 'nevro'
    }

print('hello')
'''