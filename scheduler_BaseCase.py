from z3 import *
import random
import faggrupper
import problem_setup
# Set up the problem data
slices = [1,4,6,11,25,2,3,35,44,100] #number of slices
num_samples = len(slices) #number of samples
num_doctors = 3 #number of doctors
max_points_per_doctor = 24 #the max amount of points for a doctor to have

samples = [f"sample_{i}" for i in range(num_samples)]
doctors = [f"doctor_{i}" for i in range(num_doctors)] 


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
    'r': 'øre-nese-hals-gruppen',
    'y': 'Nyregrupper',
    'oral': 'oral',
    'nevro': 'nevro'
    }
path_groups = list(spes_table.keys()) #list of the keys in spes_table
random.shuffle(path_groups) #shuffle the keys so that they are assigned randomly


doctors_spes = {} #create a dictionary to store the assigned faggruppe for each doctor
#iterate over the list of doctors and assign 1 or 2 faggrupper randomly
for doctor in doctors: 
    num_keys = random.randint(1,2)
    doctors_spes[doctor] = {}
    for i in range(num_keys):
        key = path_groups.pop(0)
        doctors_spes[doctor][key] = spes_table[key]

#print the assigned keys for each doctor.
for doctor, key_values in doctors_spes.items():
    print(f"{doctor}: {', '.join(f'{value} ({key})' for key, value in key_values.items())}")
print()

#each sample must be marked with one specialization (faggruppe) What type of sample it is. 

# POINTSYSTEM: points that each sample/section has
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
#Converts the list of samples to the correct amount of points
def slices_to_points():
    points_for_todays_slices = []
    for pt, semp in point_table.items():
        for s in semp:
            for slice in slices:
                if s == slice:
                    points_for_todays_slices.append(pt)
    return points_for_todays_slices

points = slices_to_points() #list of the points for the samples 


# Initialize Z3 solver
#--------------------------------------------------------------
solver = Solver()

# Create variables for each sample-doctor assignment
assignments = [[Bool(f"{sample}_assigned_to_{doctor}") for doctor in doctors] for sample in samples]

# Create variables for the total points assigned to each doctor
points_assigned = [Int(f"{doctor}_points_assigned") for doctor in doctors]

#----------------------Constraints-------------------------

# Add constraints to ensure each sample is assigned to exactly one doctor
for sample_assignments in assignments:
    solver.add(Or(sample_assignments))
    solver.add(Not(And(sample_assignments)))

# Add constraints to ensure each sample is assigned to at most one doctor
for i in range(num_samples):
    solver.add(sum([If(assignments[i][j], 1, 0) for j in range(num_doctors)]) <= 1)

# Add constraints to limit the number of points each doctor can receive
for j in range(num_doctors):
    total_assigned_points = sum([If(assignments[i][j], points[i], 0) for i in range(num_samples)]) # assume points is a list containing the number of points for each sample
    solver.add(total_assigned_points <= 24)  # limit to at most 24 points per doctor

#---------------------------Check-----------------------------

# Check if there is a valid solution and print the assignments
print(f'Status: {solver.check()}')
if solver.check() == sat:
    model = solver.model()
    doctor_assignments = {doctor: [] for doctor in doctors}  # initialize dictionary for each doctor's assignments
    for i in range(num_samples):
        for j in range(num_doctors):
            if is_true(model[assignments[i][j]]):
                doctor_assignments[doctors[j]].append(samples[i])  # add sample to doctor's assignments
    for doctor, assigned_samples in doctor_assignments.items():
        assigned_points = sum([points[samples.index(sample)] for sample in assigned_samples])  # calculate total assigned points for the doctor
        print(f"{doctor} is assigned samples: {', '.join(assigned_samples)} with a total of {assigned_points} points")

else:
    print("No valid assignment found.")
