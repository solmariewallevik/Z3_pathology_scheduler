from z3 import *
import random

# Set up the problem data
days_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
num_doctors = 8 #number of doctors, think 8 per week is normal

# Generate list of random amount of slices
def simulate_slices():
    slices = []
    for i in range(1,13):
        n = random.randint(1,110)
        slices.append(n)
    return slices

# List of samples ready for each day of the week
def slices_week(days):
    samples_week = []
    for day in days:
        slices = simulate_slices()
        samples_week.append(slices)
    return samples_week

slices = slices_week(days_week)


#-----------------------------------------------------
def resource_scheduler(slices, num_doctors):
    #slices =  simulate_slices() #number of slices
    num_samples = len(slices) #number of samples
    max_points_per_doctor = 24 #the max amount of points for a doctor to have

    samples = [f"sample_{i+1}" for i in range(num_samples)]
    doctors = [f"doctor_{i+1}" for i in range(num_doctors)] #list of doctors

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

    sample_groups = {i: [random.choice(list(spes_table.keys()))] for i in range(num_samples)}
    doctors_spes = {f'Doctor {i}': [random.choice(list(spes_table.keys()))] for i in range(num_doctors)}

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
        22 : [106,107,108,109,110]
        }

    # Converts the list of samples to the correct amount of points
    def slices_to_points():
        points_for_todays_slices = []
        for pt, semp in point_table.items():
            for s in semp:
                for slice in slices:
                    if s == slice:
                        points_for_todays_slices.append(pt)
        return points_for_todays_slices

    #list of the points for the samples 
    points = slices_to_points() 
    print(f'Points for that day: {points}')
    print()

    # Create a dictionary that matches each sample with a doctor based on shared FAGGRUPPE
    sample_doctor = {}
    for sample, sample_groups in sample_groups.items():
        matched_doctors = []
        for doctor, doctor_groups in doctors_spes.items():
            if any(group in sample_groups for group in doctor_groups):
                matched_doctors.append(doctor)
                # Choose a random doctor among the matched doctors for the sample
                sample_doctor[sample] = random.choice(matched_doctors)

    # Create a dictionary that maps each doctor to an integer index
    doctor_indices = {doctor: i for i, doctor in enumerate(doctors_spes.keys())}

    # Create a list of Boolean variables to represent the assignments of samples to doctors
    assignments = [[Bool(f'sample_{i}_doctor{j}') for j in range(num_doctors)] for i in range(num_samples)]


    # Initialize Z3 solver and define variables
    #--------------------------------------------------------------
    solver = Solver()

    sample_vars = [Int(f'sample_{i}') for i in range(num_samples)]
    doctor_vars = [Int(f'doctor_{i}') for i in range(num_doctors)]
    points_assigned = [Int(f"{doctor}_points_assigned") for doctor in doctors] #total points assigned to each doctor


    #----------------------Constraints-------------------------
    # Add constraints to ensure each sample is assigned to exactly one doctor
    for i in range(num_samples):
        solver.add(Or([assignments[i][j] for j in range(num_doctors)]))

    # Add constraints to ensure each sample is assigned to at most one doctor
    for i in range(num_samples):
        solver.add(sum([If(assignments[i][j], 1,0) for j in range(num_doctors)]) <= 1)

    # Add constraints to limit the number of points each doctor can receive
    for j in range(num_doctors):
        total_assigned_points = sum([If(assignments[i][j], points[i], 0) for i in range(num_samples)]) # assume points is a list containing the number of points for each sample
        solver.add(total_assigned_points <= max_points_per_doctor)  # limit to at most 24 points per doctor

    # Add the constraint that each sample is assigned to one doctor
    for sample in range(num_samples):
        solver.add(And(sample_vars[sample] >= 0, sample_vars[sample] < num_doctors))

    # Add the constraint that each doctor has at most max_points_per_doctor points
    for doctor in range(num_doctors):
        total_assigned_points = Sum([If(sample_vars[sample] == doctor, points[sample],0) for sample in range(num_samples)])
        solver.add(total_assigned_points <= max_points_per_doctor)

    # Add the constraint that each tagged sample is assigned to the tagged doctor
    for sample, doctor in sample_doctor.items():
        #solver.add(sample_vars[sample] == list(doctors_spes.keys()).index(doctors))
        solver.add(assignments[sample][doctor_indices[doctor]] == True)


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
        print()
    
    else:
        print("No valid assignment found.")
        print()


# Simulate a week of assignments
for i, day in enumerate(days_week):
    print(f"Samples for {day}: {slices[i]}")
    print()
    # Call task allocation program for current day
    resource_scheduler(slices[i], num_doctors)
