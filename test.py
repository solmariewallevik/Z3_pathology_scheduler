from z3 import *
from z3 import Optimize

'''
Base case for handing out the given samples each day at the pathology department. 
Distribute the samples/sections to the different doctors so that it is evenly distributed and 
no one has more than 24 points each day. 

No special cases for the base case. This is only for one day.
'''

#-----VARIABLES-----

#the name of the doctors working this day, starts with 0 points each day
doctors = {
    'Nils'  : 0,
    'Kari'  : 0,
    'Ola'   : 24,
    'Randi' : 0
    }

#Number of workers
n_doctors = len(doctors.keys())

# points that each sample/section has
# key = points, value = number of sections per sample
points = {
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

#maximum points per doctor
max_points = 24 #23, 24 or 25 points in average per doctor each day

#the samples to hand out this day 
#the values in this list represent number of sections
samples = [1,4,6,11,35,44,100]

#Number of samples
n_samples = len(samples)



#-----CONSTRAINTS-----

#Converts the list of samples to the correct amount of points
def samples_to_points():
    points_for_todays_samples = []

    for pt, semp in points.items():
        for s in semp:
            for slice in samples:
                if s == slice:
                    points_for_todays_samples.append(pt)
    return points_for_todays_samples

#check to see if a doctor has reached the desired amount of points per day.
def check_point():
    for name, point in doctors.items():
        if point >= max_points:
            print(f'{name} is done for the day')
            #remove from workload
        else:
            print('just keep swimming')



#-----LOGICAL FORMULAS-----
#This will be the SMT part
solver = Optimize()

#divide samples. Remember to update points
for section in range(len(samples)):
    for doc, pt in doctors.items():
        #check_point()
        doctors[doc] += section
    #print(doctors)

#Create variables for the number of points assigned to each doctor for each task
#Create a matrix where each row represents a doctor and each column represents a task (sample)
points_assigned = [[Int(f'p_ {i}_{j}') for j in range (n_samples)] for i in range(n_doctors)]

#Add constraints to ensure that each task is assigned to exactly one doctor
pt = samples_to_points()
for j in range(n_samples):
    solver.add(Sum([points_assigned[i][j] for i in range(n_doctors)]) == pt[j]) #her e da noke anna eg må gjera

#Add constraints to ensure that each doctors s assigned at most max_points_per_worker points
for i in range(n_doctors):
    solver.add(Sum(points_assigned[i]) <= max_points)

#Add objective function to minimize the difference between the number of points assigned to each doctor
obj = Sum([Abs(Sum(points_assigned[i]) - Sum(points_assigned[j])) for i in range(n_doctors) for j in range(i+1, n_doctors)])
solver.minimize(obj)

#Check if the solver is satisfiable and print the solution
if solver.check() == sat:
    model = solver.model()
    for i in range(n_doctors):
        print(f"Worker {i}: {', '.join([f'Task {j+1}: {model.evaluate(points_assigned[i][j])}' for j in range(n_samples)])}")
    else: 
        print('No solution found')
        
'''
-----Questions-----
* Should I have Id for the different samples? 
* Do the samples come in all at once or thoughout the day? 

'''


