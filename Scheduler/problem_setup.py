from z3 import *
import random

def resource_scheduler(slices, num_doctors, max_points_per_doctor, special_resp_assignment, deductionlist):

    print(f'Max points per doctor:   {max_points_per_doctor}')

    num_samples = len(slices) #number of samples
    num_special_samples = 20
    print(f'Number of special samples today: {num_special_samples}')
    special_samples = ['CITO','nålebiopsi','beinmarg','M-remisse','oral','PD-11', 'ØNH CITO', 'Gastro CITO'] # CITO = Hasteprøve

    samples = [f"Sample_{i}" for i in range(num_samples)] #list of samples
    doctors = [f"Doctor {i}" for i in range(num_doctors)] #list of doctors

    sick = [False for i in range(num_doctors)] # Boolean representation of wealness status

    request_physical_sample = [Bool(f"request_sample_{i}") for i in range(num_doctors)] # Decision variables for each doctor

    processing_time = {} # Dictionary for the generated processing times, minutes
    processing_time_special = {} #Dictionary for the generated processing times for special samples, minutes

    analyzed = [Bool(f"is_analyzed_{i}") for i in range(num_samples)] # Boolean representation of if a sample has been analyzed

    not_analyzed = [] # list with all the samples that have not been analyzed

    #start_times = [Int(f"start_{i}") for i in range(num_total_samples)]

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
        'nevro': 'nevro',
        'lun' : 'lun',
        'hud' : 'everyone'
        }

    #sample_groups = {i: [random.choice(list(spes_table.keys()))] for i in range(num_samples)}
    #doctors_spes = {f'Doctor {i}': [random.choice(list(spes_table.keys()))] for i in range(num_doctors)}

    sample_groups = {
        0 : ['hud'],1 : ['hud'],2 : ['g'],3 : ['hud'],4 : ['g'],5 : ['m'],
        6 : ['g'],7 : ['g'],8 : ['g'],9 : ['g'],10 :['g'],11 :['g'],12 :['g'],13 :['g'],14 : ['g'],15 :['g'],16 :['g'],17 :['g'],18 : ['g'],19 : ['g'],20 :['g'],21 :['g'],22 :['g'],
        23 :['g'],24 : ['l'],25 :['g'],26 : ['g'],27 : ['l'],28 :['g'],
        29 :['g'],30 :['hud'],31: ['hud'],32 : ['hud'],33 :['hud'],34 :['g'],35 :['g'],36 : ['hud'],37 :['g'],38 : ['hud'],39 : ['h'],40 : ['g'],41 : ['h'],42 : ['g'],43 : ['g'],44 :['g'],45 :['g'],46 : ['g'],47 : ['hud'],48 : ['g'],
        49 : ['g'],50 : ['hud'],51 : ['hud'],52: ['s'], 53:['g'],54:['hud'],55:['g'],56:['g'], 57:['g'],58:['g'],59:['g'],60:['g'],61:['l'],62:['r'],
        63:['g'],64:['g'],65:['g'],66:['g'],67:['g'],68:['g'],69:['g'],70:['g'],71:['g'],72:['g'],73:['g'],74:['g'],
        75:['lun'],
        76:['hud'],77:['l'],78:['hud'],79:['hud'],80:['hud'],81:['hud'],82:['hud'],83:['x'],84:['hud'],85:['hud'],86:['hud'],87:['hud'],88:['hud'],89:['hud'],90:['hud'],91:['hud'],92:['u'],93:['hud'],94:['u'],95:['m'],
        96:['h'],97:['h'],98:['h'],99:['h'],100:['h'],101:['h'],102:['h'],103:['h'],104:['h'],105:['h'],106:['hud'],107:['h'],108:['h'],109:['h'],110:['h'],111:['h'],112:['h'],113:['h'],114:['h'],115:['h'],116:['h'],
        117:['hud'],118:['hud'],119:['r'],120:['g'],121:['hud'],122:['g'],123:['hud'],124:['hud'],125:['hud'],126:['r'],127:['hud'],128:['hud'],129:['hud'],130:['hud'],
        131:['g'],132:['g'],133:['g'],134:['g'],135:['h'],136:['h'],137:['x'],138:['x'],139:['x'],140:['x'],141:['x'],142:['x'],143:['x'],
        144:['hud'],145:['hud'],146:['h'],147:['h'],148:['h'],149:['hud'],150:['h'],151:['p'],152:['h'],
        153:['x'],154:['x'],155:['x'],156:['x'],157:['x'],158:['x'],159:['x'],160:['x'],161:['x'],162:['x'],163:['x'],164:['x'],165:['x'],166:['x'],
        167:['x'],168:['x'],169:['x'],170:['x'],171:['x'],172:['x'],
        173:['nevro'],
        174:['hud'],175:['hud'],176:['hud'],177:['hud'],178:['hud'],179:['r'],180:['u'],181:['u'],182:['u'],183:['u'],
        184:['r'],185:['r'],186:['r'],
        187:['g'],188:['g'],189:['g'],190:['g'],191:['g'],192:['g'],193:['g'],194:['g'],195:['g'],196:['g'],197:['g'],198:['g'],199:['g'],200:['g'],201:['g'],202:['g'],203:['g'],204:['g'],205:['g'],206:['g'],207:['g'],208:['g'],209:['g'],210:['g']
        }
    doctors_spes = {
        'Doctor 0' : ['m','g','hud'],
        'Doctor 1' : ['g','hud'],
        'Doctor 2' : ['g','l','hud'],
        'Doctor 3' : ['g','h','hud'],
        'Doctor 4' : ['s','g','r','l','hud'],
        'Doctor 5' : ['g','hud'],
        'Doctor 6' : ['lun','hud'],
        'Doctor 7' : ['m','l','x','u','hud'],
        'Doctor 8' : ['h','hud'],
        'Doctor 9' : ['m','hud','r'],
        'Doctor 10' : [], #oral
        'Doctor 11' : ['g','hud'],
        'Doctor 12' : ['x','hud'],
        'Doctor 13' : ['y','hud'],
        'Doctor 14' : ['h','p','hud'],
        'Doctor 15' : ['x','hud'],
        'Doctor 16' : ['x','hud'],
        'Doctor 17' : ['nevro','hud'],
        'Doctor 18' : ['u','r','x','hud'],
        'Doctor 19' : ['r','hud'],
        'Doctor 20' : ['g','hud']
        }

    special_sample = {
        0 : ['oral'],1 : ['oral'],2 : ['oral'],
        3 : ['nålebiopsi'],4 : ['nålebiopsi'],5 : ['nålebiopsi'],6 : ['nålebiopsi'],7 : ['nålebiopsi'],
        8 : ['nålebiopsi'],9 : ['nålebiopsi'],10 : ['nålebiopsi'],11 : ['nålebiopsi'],12 : ['nålebiopsi'],
        13 : ['nålebiopsi'],14:['beinmarg'],15:['beinmarg'],16:['beinmarg'],17:['beinmarg'],18:['nålebiopsi'],19:['nålebiopsi']
        }

    doctor_responsibility = {
        'Doctor 0' : ['nålebiopsi','beinmarg'],
        'Doctor 1' : ['nålebiopsi','beinmarg'],
        'Doctor 2' : ['nålebiopsi','beinmarg'],
        'Doctor 3' : ['nålebiopsi','beinmarg'],
        'Doctor 4' : ['nålebiopsi','beinmarg'],
        'Doctor 5' : ['nålebiopsi','beinmarg'],
        'Doctor 6' : ['nålebiopsi','beinmarg'],
        'Doctor 7' : ['nålebiopsi','beinmarg'],
        'Doctor 8' : ['nålebiopsi','beinmarg'],
        'Doctor 9' : ['nålebiopsi','beinmarg'],
        'Doctor 10' : ['oral'],
        'Doctor 11' : ['nålebiopsi','beinmarg'],
        'Doctor 12' : ['nålebiopsi','beinmarg'],
        'Doctor 13' : ['nålebiopsi','beinmarg'],
        'Doctor 14' : ['nålebiopsi','beinmarg'],
        'Doctor 15' : ['nålebiopsi','beinmarg'],
        'Doctor 16' : ['nålebiopsi','beinmarg'],
        'Doctor 17' : ['nålebiopsi','beinmarg'],
        'Doctor 18' : ['nålebiopsi','beinmarg'],
        'Doctor 19' : ['nålebiopsi','beinmarg'],
        'Doctor 20' : ['nålebiopsi','beinmarg'],
        }

    spa = special_resp_assignment
    # Update the dictionary with the responsibilities that week
    for doctor, specialties in spa.items():
        if doctor in doctor_responsibility:
            doctor_responsibility[doctor] += specialties
        else:
            doctor_responsibility[doctor] = specialties

    # List with names of the special sampels that day
    todays_special_samples = []
    #for i in range(num_special_samples):
        #todays_special_samples.append(f'{random.choice(special_samples)}_{i}')
    # 20 samples
    todays_special_samples.append('oral_0')
    todays_special_samples.append('oral_1')
    todays_special_samples.append('oral_2')
    todays_special_samples.append('nålebiopsi_3')
    todays_special_samples.append('nålebiopsi_4')
    todays_special_samples.append('nålebiopsi_5')
    todays_special_samples.append('nålebiopsi_6')
    todays_special_samples.append('nålebiopsi_7')
    todays_special_samples.append('nålebiopsi_8')
    todays_special_samples.append('nålebiopsi_9')
    todays_special_samples.append('nålebiopsi_10')
    todays_special_samples.append('nålebiopsi_11')
    todays_special_samples.append('nålebiopsi_12')
    todays_special_samples.append('nålebiopsi_13')
    todays_special_samples.append('beinmarg_14')
    todays_special_samples.append('beinmarg_15')
    todays_special_samples.append('beinmarg_16')
    todays_special_samples.append('beinmarg_17')
    todays_special_samples.append('nålebiopsi_18')
    todays_special_samples.append('nålebiopsi_19')

    # List with number of slices per special sample
    todays_special_sample_slices = []
    #for samp in range(num_special_samples):
        #todays_special_sample_slices.append(random.randint(1,20)) # NUMBER OF SLICES GENERATED
    todays_special_sample_slices = [1,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,2,3,4,1]

    #dictionary of the sample and the num of slices
    spes_samp_and_slice = dict(zip(todays_special_samples, todays_special_sample_slices))
        
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

    #Convert the list of special samples to the correct amount of points
    def special_slices_to_points():
        new_list = []
        for key, value in spes_samp_and_slice.items():
            if key.startswith('oral'):
                new_list.append(0)
            elif key.startswith('PD-11'):
                new_list.append(1)
            elif value in point_table[1]:
                new_list.append(2)
            else:
                for ky, lst in point_table.items():
                    if value in lst:
                        new_list.append(ky)
        return new_list

    # Convert the list of special samples to the correct amount of points in a dictionary
    def spes_sample_and_point():
        points_dict = {}
        for key, value in spes_samp_and_slice.items():
            if key.startswith('oral'):
                points_dict[key] = 0
            elif key.startswith('PD-11'):
                points_dict[key] = 1
            elif value in point_table[1]:
                points_dict[key] = 2
            else:
                for ky, lst in point_table.items():
                    if value in lst:
                        points_dict[key] = ky
                        break
        return points_dict
    spes_points_dic = spes_sample_and_point()

    points = slices_to_points() #list of points for todays samples
    special_points = special_slices_to_points() #list of the points for the special samples

    # Create a dictionary that matches each sample with a doctor based on shared FAGGRUPPE
    sample_doctor = {}
    for sample, sample_groups in sample_groups.items():
        matched_doctors = []
        for doctor, doctor_groups in doctors_spes.items():
            if any(group in sample_groups for group in doctor_groups):
                matched_doctors.append(doctor)
                # Choose a random doctor among the matched doctors for the sample
                sample_doctor[sample] = random.choice(matched_doctors) # sample y: doctor x

    # Create a dictionary that matches each special sample with a doctor with that responsibility
    special_sample_doctor = {}
    for sample, sample_groups in special_sample.items():
        m_doctors = []
        for doctor, doctor_groups in doctor_responsibility.items():
            if any(group in sample_groups for group in doctor_groups):
                m_doctors.append(doctor)
                special_sample_doctor[sample] = random.choice(m_doctors)

    # Create a dictionary that maps each doctor to an integer index
    doctor_indices = {doctor: i for i, doctor in enumerate(doctors_spes.keys())}

    # Create a dictionary that maps each special sample to an integer index
    spes_sample_index = {
        'CITO'          : 0,
        'ØNH CITO'      : 1,
        'Gastro CITO'   : 2,
        'Lymfom/hema'   : 3
        }

    # Assign random time to each sample
    for i, sample in enumerate(samples): 
        if points[samples.index(sample)] in range(0,10):
            processing_time[sample] = random.randint(1,3)
        elif points[samples.index(sample)] in range(11,30):
            processing_time[sample] = random.randint(4,6)
        else:
            processing_time[sample] = random.randint(7,10)
        
    # Assign random times to each special samples
    for i, sample, in enumerate(todays_special_samples):
        if special_points[todays_special_samples.index(sample)] in range(0,10):
            processing_time_special[sample] = random.randint(1,3)
        elif special_points[todays_special_samples.index(sample)] in range(4,6):
            processing_time_special[sample] = random.randint(16,40)
        else:
            processing_time_special[sample] = random.randint(7,10)

    # Create a list of Boolean variables to represent the assignments of samples to doctors
    assignments = [[Bool(f'sample_{i}_doctor{j}') for j in range(num_doctors)] for i in range(num_samples)]
    # Create a list of Boolean variables to represent the assignments of special samples to doctors
    spes_assignments = [[Bool(f'special_sample_{i}_doctor{j}') for j in range(num_doctors)] for i in range(num_special_samples)]

    # Initialize Z3 solver and define variables
    #--------------------------------------------------------------
    solver = Solver()

    # Enable proof generation
    #solver.set(unsat_core=True)

    sample_vars = [Int(f'Sample {i}') for i in range(num_samples)]
    doctor_vars = [Int(f'Doctor {i}') for i in range(num_doctors)]
    special_sample_vars = [Int(f'special_sample{i}') for i in range(num_special_samples)]

    total_points = [Int(f'total_points_{i}') for i in range(num_doctors)]

    #----------------------Constraints, Base Case -------------------------
    # Add constraints to ensure each sample is assigned to exactly one doctor or added to not analyzed
    for i in range(num_samples):
        analyzed_sample = Bool(f'Sample{i}_analyzed')
        # Add the constraint that the sample is either assigned to one doctor or not analyzed
        solver.add(Or(Or([assignments[i][j] for j in range(num_doctors)]), Not(analyzed_sample)))
        # Add the sample to the not_analyzed list if it is not analyzed
        not_analyzed.append(Not(analyzed_sample))

        #solver.add(Or([assignments[i][j] for j in range(num_doctors)])) #Maybe not

    # Add constraint to ensure each special sample is assigned to exactly one doctor or added to not analyzed
    for i in range(num_special_samples):
        solver.add(Or([spes_assignments[i][j] for j in range(num_doctors)]))

    # Add constraints to ensure each sample is assigned to at most one doctor or marked as un_analyzed
    for i in range(num_samples):
        solver.add(sum([If(assignments[i][j], 1,0) for j in range(num_doctors)]) + If(not_analyzed[i], 1, 0) <= 1)

    # Add constraint to ensure each special sample is assigned to at most one doctor 
    for i in range(num_special_samples):
        solver.add(sum([If(spes_assignments[i][j], 1, 0) for j in range(num_doctors)]) <= 1)

    # Add the constraint that each sample is assigned to one doctor
    #for sample in range(num_samples):
        #solver.add(And(sample_vars[sample] >= 0, sample_vars[sample] < num_doctors))
    # Add the constraint that each sample is assigned to one doctor or marked as unanalyzed
    for sample in range(num_samples):
        solver.add(Or(
            [assignments[sample][j] for j in range(num_doctors)] + [not_analyzed[sample]]
        ))

    #Add the constraint that each special sample is assigned to one doctor
    for sample in range(num_special_samples):
        solver.add(And(special_sample_vars[sample] >= 0, special_sample_vars[sample] < num_doctors))

    # Add constraints to limit the number of points each doctor can receive
    for j in range(num_doctors):
        # Calculate total assigned points for sampels (regular and special)
        tap_regular = sum([If(assignments[i][j], points[i], 0) for i in range(num_samples)]) 
        tap_special = sum([If(spes_assignments[k][j], special_points[k], 0) for k in range(num_special_samples)])
        
        # Enforce the constraint that total assigned points (regular + special) for each doctor does not exceed max_points_per_doctor
        solver.add(tap_regular + tap_special <= max_points_per_doctor[j] + 2)

    # Add the constraint that each doctor has at most max_points_per_doctor points
    for doctor in range(num_doctors):
        # Calculate total assigned points for regular samples for each doctor
        t_regular = Sum([If(sample_vars[sample] == doctor, points[sample], 0) for sample in range(num_samples)])
        # Calculate total assigned points for special samples for each doctor
        t_special = Sum([If(special_sample_vars[sample] == doctor, special_points[sample], 0) for sample in range(num_special_samples)])

        # Enforce the constraint that the total assigned points (regular + special) for each doctor does not exceed max_points_per_doctor
        solver.add(t_regular + t_special <= max_points_per_doctor[doctor] + 2)

    # Add the constraint that each tagged sample is assigned to the correct tagged doctor
    for sample, doctor in sample_doctor.items():
        solver.add(assignments[sample][doctor_indices[doctor]] == True)

    # Add the constraint that each tagged special sample is assigned to the correct tagged doctor
    for sample, doctor in special_sample_doctor.items():
        solver.add(spes_assignments[sample][doctor_indices[doctor]] == True)

    # Add the constraint that total points assigned to all doctors must equal the sum of points for all samples
    total_assigned_points = Sum([If(assignments[i][j], points[i], 0) for i in range(num_samples) for j in range(num_doctors)])
    solver.add(total_assigned_points == Sum(points))

    #Add the consteraint that total points assigned to all doctors must equal the sum of points for all sampels
    total_ass_special_points = Sum([If(spes_assignments[i][j], special_points[i], 0) for i in range(num_special_samples) for j in range(num_doctors)])
    solver.add(total_ass_special_points == Sum(special_points))
     
    #------------------------------- SICK ------------------------------#
    # This doctor is sick
    #sick[1] = True

    # Add a constraint that if a doctor is sick, they cannot be assigned any samples or points
    for i in range(num_samples):
        for j in range(num_doctors):
            solver.add(Implies(sick[j], Not(assignments[i][j])))

    # Add a constraint that if a doctor is sick, they cannot be assigned any special samples or points
    for i in range(num_special_samples):
        for j in range(num_doctors):
            solver.add(Implies(sick[j], Not(spes_assignments[i][j])))

    #-----------------------EVEN DISTRIBUTION---------------------------#

    doctor_assignments = {doctor: [] for doctor in doctors}  # initialize dictionary for each doctor's assignments
    special_samples_assignments = {doctor: [] for doctor in doctors}
    assigned_points = {doctor: [] for doctor in doctors}  # initialize dictionary for each doctor's assigned points

    # Calculate the total points assigned to each doctor
    total_points = [Sum([points[samples.index(sample)] for sample in doctor_assignments[doctor]]) +
                   Sum([spes_points_dic[sample] for sample in special_samples_assignments[doctor]])
                   for doctor in doctors]

    # Calculate the average points per doctor
    average_points = Sum(total_points) // num_doctors

    # Add constraint to ensure each doctor's points are close to the average
    for doctor in doctors:
        doctor_samples = doctor_assignments[doctor] + special_samples_assignments[doctor]
        assigned_points[doctor] = [points[samples.index(sample)] for sample in doctor_samples]

        solver.add(Sum(assigned_points[doctor]) == average_points)

    #----------------------PHYSICAL SAMPLE------------------------------------#
    # Add constraint: Only some doctors request a physical sample
    solver.add(Or([request_physical_sample[i] for i in range(num_doctors)]))
    # Doctor 3 and 7 want physical samples
    solver.add(request_physical_sample[2])
    solver.add(request_physical_sample[6])

    #-----------------------TIME-----------------------------#
    # Add constraint: Sum of processing times for each doctor's assigned samples (regular and special) should not exceed 400
    for j in range(num_doctors):
        doctor_assigned_samples = [If(assignments[i][j], processing_time.get(i, 0), 0) for i in range(num_samples)] #regular samples
        total_processing_time = Sum(doctor_assigned_samples)

        doctor_assigned_spes_samp = [If(spes_assignments[i][j], processing_time_special.get(i,0), 0) for i in range(num_special_samples)] #special samples
        total_spes_processing_time = Sum(doctor_assigned_spes_samp)

        solver.add(total_processing_time + total_spes_processing_time <= 400) # 400 minutes is one work day, 7 hours.

    #---------------------------Check-----------------------------
    # Check if there is a valid solution and print the assignments
    points_for_the_next_day = []
    print(f'Status: {solver.check()}')
    if solver.check() == sat:
        model = solver.model()  

        for i in range(num_doctors):
            if model[request_physical_sample[i]]:
                print(f"Doctor {i} - Request Physical Sample: True")

        current_pt = list(deductionlist.values())
        current_doctor = list(deductionlist.keys())
        for i in range(len(sick)):
            if sick[i]:
                max_points_per_doctor[i] = 0
                print(f'Doctor {i} is sick')
                deductionlist[f'Doctor {i}'] = current_pt[i]-25
            elif sick[i] == False:
                max_points_per_doctor[i] = 30

        if True in sick:
            print(f'Deductionlist: {deductionlist}')

        print(f'New max points per doctor: {max_points_per_doctor}')
    
        doctor_assignments = {doctor: [] for doctor in doctors}  # initialize dictionary for each doctor's assignments
        special_samples_assignments = {doctor: [] for doctor in doctors}  # initialize dictionary for each doctor's special sample assignments

        list_of_all_points = []

        # Add regular sample to doctor's assignments
        for i in range(num_samples):
            for j in range(num_doctors):
                if is_true(model[assignments[i][j]]):
                    doctor_assignments[doctors[j]].append(samples[i])
    
        # Add special sample to doctor's assignments
        for i in range(num_special_samples):
            for j in range(num_doctors):
                if is_true(model[spes_assignments[i][j]]):
                    special_samples_assignments[doctors[j]].append(todays_special_samples[i])

        # Print the regular samples and special samples assigned to each doctor and their total points
        print("Sample Assignments and Points:")
        for doctor in doctors:
            assigned_samples = doctor_assignments[doctor] + special_samples_assignments[doctor]
            assigned_points = sum([points[samples.index(sample)] for sample in doctor_assignments[doctor]]) + sum([spes_points_dic[sample] for sample in special_samples_assignments[doctor]])

            if assigned_points > 25:
                extra_work = assigned_points-25
                deductionlist[doctor] += extra_work

            print(f"{doctor} is assigned samples: {', '.join(assigned_samples)} with a total of {assigned_points} points")
            list_of_all_points.append(assigned_points)

        print(f'The deduction list: {deductionlist}')

        #The unassigned samples
        not_analyzed_next_day = []
        for sample in not_analyzed:
            if is_true(model.evaluate(sample)):
                not_analyzed_next_day.append(sample)

        not_analyzed_dict = {}
        for condition in not_analyzed_next_day:
            sample_name = condition.split('(')[1].split('_')[0]
            not_analyzed_dict[sample_name] = condition

        not_analyzed_samples = []
        not_analyzed_slices = []
        for sample in samples:
            if sample in not_analyzed_dict:
                not_analyzed_samples.append(sample)
                not_analyzed_slices.append(slices[samples.index(sample)])
        print(f'Samples not analyzed today: {not_analyzed_samples}') #The samples sent to the next day

        #Calculate points for the next day
        for max_points, points in zip(max_points_per_doctor, list_of_all_points):
            remaining_points = max(max_points - points, 0)
            points_for_the_next_day.append(remaining_points)

        #Print the processing time for each doctor
        print(f'Processing Time: ')
        for j in range(num_doctors):
            doctor_assigned_samples = [model.eval(assignments[i][j]) for i in range(num_samples)]
            total_processing_time = sum(
                processing_time[samples[i]] for i, assignment in enumerate(doctor_assigned_samples) if assignment
            )
            doctor_assigned_spes_samp = [model.eval(spes_assignments[i][j]) for i in range(num_special_samples)]
            total_spes_processing_time = sum(
                processing_time_special[todays_special_samples[i]] for i, spes_assignments in enumerate(doctor_assigned_spes_samp) if spes_assignments
            )
            processing_time_in_total = total_processing_time + total_spes_processing_time
            print(f'Total processing time for Doctor {j}: {processing_time_in_total} minutes') 

        return points_for_the_next_day, not_analyzed_slices
    
    else:
        print("No valid assignment found.")
        #unsat_core = solver.unsat_core()
        #print("Unsatisfiable core:", unsat_core)

        print()
        for doc in range(num_doctors):
            points_for_the_next_day.append(0)
        return points_for_the_next_day, []
