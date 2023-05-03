from z3 import *
import random

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

    # Add the constraint that total points assigned to all doctors must equal the sum of points for all samples
    total_assigned_points = Sum([If(assignments[i][j], points[i], 0) for i in range(num_samples) for j in range(num_doctors)])
    solver.add(total_assigned_points == Sum(points))




    '''
    # Add constraints to redistribute points if a doctor gets sick
    for j in range(num_doctors):
        sick_doctor = Bool('sick_doctor_' + str(j))
        solver.add(sick_doctor == False)  # assume no doctors are initially sick

        # add constraint to redistribute points if doctor j gets sick
        for k in range(num_doctors):
            if k != j:  # don't need to redistribute points to the sick doctor
                # add constraint to redistribute points to doctor k
                total_assigned_points_k = Sum([If(assignments[i][k], points[i], 0) for i in range(num_samples)])
                extra_points_k = max_points_per_doctor - total_assigned_points_k  # calculate how many extra points doctor k can take

                total_assigned_points_j = Sum([If(assignments[i][j], points[i], 0) for i in range(num_samples)])
                points_to_redistribute = total_assigned_points_j - max_points_per_doctor  # calculate how many points need to be redistributed

                # add constraint to redistribute points only if the sick doctor has been assigned points
                solver.add(Implies(sick_doctor == True, total_assigned_points_j > 0))

                # add constraint to redistribute points only if doctor k has the same specialization tag as doctor j
                solver.add(Implies(doctor_vars[k] == doctor_vars[j], extra_points_k >= points_to_redistribute))

                # add constraint to redistribute points to doctor k
                for i in range(num_samples):
                    if assignments[i][j] == True:
                        solver.add(Implies(sample_vars[i] == k, assignments[i][k] == True))  # assign sample i to doctor k
                        solver.add(Implies(sample_vars[i] == j, assignments[i][j] == False))  # unassign sample i from doctor j
                        extra_points_k_new = extra_points_k + points[i]
                        solver.add(Implies(sample_vars[i] == k, extra_points_k_new == extra_points_k + points[i])) # add points to doctor k
    '''

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