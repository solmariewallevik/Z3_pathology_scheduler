from z3 import *
import random

# Set up the problem data
slices = [1,1,1,1,1,1,1] #number of slices
num_samples = len(slices) #number of samples
num_doctors = 3 #number of doctors
max_points_per_doctor = 24 #the max amount of points for a doctor to have

samples = [f"sample_{i}" for i in range(num_samples)]
doctors = [f"doctor_{i}" for i in range(num_doctors)] 

#FAGGRUPPER. Each doctor has 1 or 2 (some have 3 and some none).
spes_table = {
    'u': 'Uro-group',
    'x': 'Gyno-group',
    'p': 'Perinatal-group',
    'm': 'Mom-group',
    'g': 'Gastro-group',
    'h': 'Skin-group',
    'l': 'Lymfoma-group',
    's': 'Sarkoma-group',
    'r': 'ear-nose-thought-group',
    'y': 'Kidney-group',
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
    print(f"{doctor}: {', '.join(f'{key}' for key, value in key_values.items())}")
print()

#each sample must be marked with one specialization (faggruppe) What type of sample it is. 

# POINTSYSTEM: points that each sample/section has
# key = points, value = number of sections per sample
point_table = {
    1 : [1,2,3,4,5],
    2 : [6,7,8,9,10]
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

# Create a dictionary to store the assigned path_groups for each sample
'''
sample_groups = {}
for i, sample in enumerate(samples):
    sample_groups[sample] = path_groups[i]
'''

# Initialize Z3 solver
#--------------------------------------------------------------
solver = Solver()

# Create variables for each sample-doctor assignment
assignments = [[Bool(f"{sample}_assigned_to_{doctor}") for doctor in doctors] for sample in samples]

# Create variables for the total points assigned to each doctor
points_assigned = [Int(f"{doctor}_points_assigned") for doctor in doctors]

# Create variables for the path_group assigned to each sample
sample_path_group = [String(f"{sample}_path_group") for sample in samples]

# Assign a random path_group to each sample
for i in range(num_samples):
    path_group = path_groups.pop(0)
    solver.add(sample_path_group[i] == path_group)


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
    solver.add(total_assigned_points <= max_points_per_doctor)  # limit to at most 24 points per doctor

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
        # Print the assigned path_group for each sample
    for i in range(num_samples):
         print(f"{samples[i]}: {model[sample_path_group[i]]}")
            

else:
    print("No valid assignment found.")
