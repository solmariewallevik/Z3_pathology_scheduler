from z3 import *
import random

def resource_scheduler(slices, num_doctors, max_points_per_doctor, special_resp_assignment, deductionlist):

    print(f'Max points per doctor:   {max_points_per_doctor}')

    num_samples = len(slices) #number of samples
    num_special_samples = 12
    print(f'Number of special samples today: {num_special_samples}')
    special_samples = ['CITO','nålebiopsi','beinmarg','M-remisse','oral','PD-11', 'ØNH CITO', 'Gastro CITO'] # CITO = Hasteprøve

    samples = [f"Sample_{i}" for i in range(num_samples)] #list of samples
    doctors = [f"Pathologist {i}" for i in range(num_doctors)] #list of doctors

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
        0 : ['hud'],1:['u'],2:['m'],3: ['hud'],4: ['hud'],5: ['hud'],6: ['hud'],7: ['hud'],8:['m'],9: ['hud'],10: ['hud'],11: ['hud'],12: ['hud'],13: ['hud'],14: ['hud'],15: ['hud'],16: ['hud'],17:['m'],18:['m'],19: ['hud'],20: ['hud'],21:['m'],22: ['hud'],
        23:['g'],24:['g'],25:['g'],26:['g'],27:['g'],28:['g'],29:['g'],30:['g'],31:['g'],32:['g'],33:['g'],34:['g'],35:['g'],36:['g'],37:['g'],38:['g'],39:['g'],40:['g'],41:['g'],42:['g'],43:['g'],44:['g'],45:['g'],46:['g'],47:['g'],
        48:['g'],49:['g'],50:['g'],51:['g'],52:['g'],53:['g'],54:['g'],55:['g'],56:['g'],57:['l'],58:['g'],
        59:['g'],60:['h'],61:['h'],62:['h'],63:['h'],64:['h'],65:['g'],66:['h'],67:['h'],68:['h'],69:['g'],70:['h'],71:['g'],72:['h'],73:['h'],74:['g'],75:['g'],76:['h'],77:['g'],78:['h'],79:['g'],80:['g'],81:['g'],82:['h'],83:['g'],84:['g'],85:['h'],86:['h'],
        87:['g'],88:['s'],89:['s'],90:['s'],91:['hud'],92:['hud'],93:['hud'],94:['hud'],95:['s'],96:['s'],97:['hud'],98:['hud'],99:['hud'],100:['u'],101:['s'],102:['s'],103:['hud'],104:['u'],105:['u'],106:['u'],
        107:['g'],108:['g'],109:['g'],110:['g'],111:['g'],112:['hud'],113:['hud'],114:['hud'],115:['hud'],116:['hud'],117:['g'],118:['g'],119:['g'],120:['g'],121:['g'],122:['g'],123:['g'],124:['p'],125:['p'],126:['p'],
        127:['nevro'],
        128:['g'],129:['g'],
        130:['hud'],131:['hud'],132:['hud'],133:['hud'],134:['hud'],135:['hud'],136:['hud'],137:['hud'],138:['hud'],139:['hud'],140:['hud'],141:['hud'],142:['hud'],143:['hud'],144:['hud'],145:['hud'],146:['hud'],147:['hud'],
        148:['hud'],149:['h'],150:['h'],151:['h'],152:['h'],153:['h'],154:['h'],155:['h'],156:['h'],157:['hud'],158:['h'],159:['h'],160:['h'],161:['h'],162:['h'],163:['h'],164:['h'],165:['hud'],166:['h'],167:['h'],168:['h'],169:['h'],170:['h'],171:['h'],172:['h'],173:['h'],
        174:['hud'],175:['hud'],176:['m'],177:['r'],178:['r'],179:['u'],
        180:['hud'],181:['hud'],182:['hud'],183:['r'],184:['r'],185:['r'],186:['r'],187:['hud'],
        188:['x'],189:['x'],190:['x'],191:['x'],192:['x'],193:['x'],194:['x'],195:['x'],196:['x'],197:['x'],198:['x'],199:['x'],
        200:['h'],201:['h'],202:['h'],203:['h'],204:['h'],205:['h'],206:['h'],207:['h'],208:['p'],209:['h'],210:['h'],
        211:['x'],212:['x'],213:['x'],214:['x'],215:['x'],216:['x'],217:['x'],218:['x'],
        219:['x'],220:['x'],221:['x'],222:['x'],223:['x'],224:['x'],225:['x'],226:['x'],
        227:['g'],228:['g'],229:['g'],230:['g'],231:['g'],232:['g'],
        233:['hud'],234:['h'],235:['hud'],236:['hud'],237:['hud'],238:['hud'],239:['hud'],240:['hud'],241:['hud'],242:['hud'],243:['hud'],244:['r'],245:['r'],246:['u'],247:['r'],248:['u'],249:['u'],250:['r'],251:['hud'],252:['u'],253:['r'],254:['u'],255:['u'],
        256:['r'],257:['r'],258:['r']
        }
    doctors_spes = {
        'Doctor 0' : ['m','g','hud'],
        'Doctor 1' : ['g','hud'],
        'Doctor 2' : ['g','l','hud'],
        'Doctor 3' : ['g','h','hud'],
        'Doctor 4' : ['s','u','g','hud'],
        'Doctor 5' : ['g','hud','p'],
        'Doctor 6' : ['nevro','hud'],
        'Doctor 7' : ['g','hud'],
        'Doctor 8' : ['hud'],
        'Doctor 9' : ['h','hud'],
        'Doctor 10' : ['m','r','hud'], 
        'Doctor 11' : ['hud'], #oral
        'Doctor 12' : ['r','hud'],
        'Doctor 13' : ['x','hud'],
        'Doctor 14' : ['h','p','hud'],
        'Doctor 15' : ['x','hud'],
        'Doctor 16' : ['x','hud'],
        'Doctor 17' : ['g','hud'],
        'Doctor 18' : ['u','h','r','hud'],
        'Doctor 19' : ['r','hud']
        }

    special_sample = {
        0:['oral'],1:['oral'],2:['oral'],3:['oral'],
        4:['nålebiopsi'],5:['nålebiopsi'],
        6:['beinmarg'],7:['beinmarg'],8:['beinmarg'],9:['beinmarg'],10:['beinmarg'],11:['beinmarg']
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
        'Doctor 10' : ['nålebiopsi','beinmarg'],
        'Doctor 11' : ['oral'],
        'Doctor 12' : ['nålebiopsi','beinmarg'],
        'Doctor 13' : ['nålebiopsi','beinmarg'],
        'Doctor 14' : ['nålebiopsi','beinmarg'],
        'Doctor 15' : ['nålebiopsi','beinmarg'],
        'Doctor 16' : ['nålebiopsi','beinmarg'],
        'Doctor 17' : ['nålebiopsi','beinmarg'],
        'Doctor 18' : ['nålebiopsi','beinmarg'],
        'Doctor 19' : ['nålebiopsi','beinmarg']
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
    # 12 samples
    todays_special_samples.append('oral_0')
    todays_special_samples.append('oral_1')
    todays_special_samples.append('oral_2')
    todays_special_samples.append('oral_3')
    todays_special_samples.append('nålebiopsi_4')
    todays_special_samples.append('nålebiopsi_5')
    todays_special_samples.append('beinmarg_6')
    todays_special_samples.append('beinmarg_7') 
    todays_special_samples.append('beinmarg_8')
    todays_special_samples.append('beinmarg_9')
    todays_special_samples.append('beinmarg_10')
    todays_special_samples.append('beinmarg_11')

    # List with number of slices per special sample
    todays_special_sample_slices = []
    #for samp in range(num_special_samples):
        #todays_special_sample_slices.append(random.randint(1,20)) # NUMBER OF SLICES GENERATED
    todays_special_sample_slices = [1,1,1,1,3,1,2,2,1,1,1,1]

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
    doctor_vars = [Int(f'Pathologist {i}') for i in range(num_doctors)]
    special_sample_vars = [Int(f'special_sample{i}') for i in range(num_special_samples)]

    total_points = [Int(f'total_points_{i}') for i in range(num_doctors)]

    #----------------------Constraints, Base Case -------------------------
    # Add constraints to ensure each sample is assigned to exactly one doctor or added to not analyzed
    for i in range(num_samples):
        analyzed_sample = Bool(f'Sample{i}_analyzed')
        # Add the constraint that the sample is either assigned to one doctor or not analyzed
        solver.add(Or(Or([assignments[i][j] for j in range(num_doctors)]), Not(analyzed_sample)))
        # Add the sample to the not_analyzed list if it is not analyzed
        for j in range(num_doctors):
            not_analyzed.append(Or(Not(analyzed_sample), 
                                   And(analyzed_sample, 
                                       sum([If(assignments[i][k], points[i], 0) for k in range(num_doctors)]) > max_points_per_doctor[j])))

    # Add constraint to ensure each special sample is assigned to exactly one doctor or added to not analyzed
    for i in range(num_special_samples):
        solver.add(Or([spes_assignments[i][j] for j in range(num_doctors)]))

    # Add constraints to ensure each sample is assigned to at most one doctor or marked as un_analyzed
    for i in range(num_samples):
        solver.add(sum([If(assignments[i][j], 1,0) for j in range(num_doctors)]) + If(not_analyzed[i], 1, 0) <= 1)

    # Add constraint to ensure each special sample is assigned to at most one doctor 
    for i in range(num_special_samples):
        solver.add(sum([If(spes_assignments[i][j], 1, 0) for j in range(num_doctors)]) <= 1)

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
    #---------------------------------------------------------------------------------------
    
    #---------------------------------------------------------------------------------------

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

    #doctor_assignments = {doctor: [] for doctor in doctors}  # initialize dictionary for each doctor's assignments
    #special_samples_assignments = {doctor: [] for doctor in doctors}
    #assigned_points = {doctor: [] for doctor in doctors}  # initialize dictionary for each doctor's assigned points

    # Calculate the total points assigned to each doctor
    #total_points = [Sum([points[samples.index(sample)] for sample in doctor_assignments[doctor]]) +
                   #Sum([spes_points_dic[sample] for sample in special_samples_assignments[doctor]])
                   #for doctor in doctors]

    # Calculate the average points per doctor
    #average_points = Sum(total_points) // num_doctors

    # Add constraint to ensure each doctor's points are close to the average
    #for doctor in doctors:
        #doctor_samples = doctor_assignments[doctor] + special_samples_assignments[doctor]
        #assigned_points[doctor] = [points[samples.index(sample)] for sample in doctor_samples]

        #solver.add(Sum(assigned_points[doctor]) == average_points)

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
   #-----------------------------------------------------------#


    #---------------------------Check-----------------------------
    # Check if there is a valid solution and print the assignments
    points_for_the_next_day = []
    print(f'Status: {solver.check()}')
    if solver.check() == sat:
        model = solver.model()  

        for i in range(num_doctors):
            if model[request_physical_sample[i]]:
                print(f"Pathologist {i} - Request Physical Sample: True")

        current_pt = list(deductionlist.values())
        current_doctor = list(deductionlist.keys())
        for i in range(len(sick)):
            if sick[i]:
                max_points_per_doctor[i] = 0
                print(f'Pathologist {i} is sick')
                deductionlist[f'Doctor {i}'] = current_pt[i]-25
            elif sick[i] == False:
                max_points_per_doctor[i] = 30

        if True in sick:
            print(f'Deductionlist: {deductionlist}')

        print(f'New max points per pathologist: {max_points_per_doctor}')
    
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

            print(f"{doctor} is assigned samples: {', '.join(assigned_samples)} with a total of ")
            print(f'{assigned_points} points.')
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
            print(f'Total processing time for Pathologist {j}: {processing_time_in_total} minutes') 

        return points_for_the_next_day, not_analyzed_slices
    
    else:
        print("No valid assignment found.")
        #unsat_core = solver.unsat_core()
        #print("Unsatisfiable core:", unsat_core)

        print()
        for doc in range(num_doctors):
            points_for_the_next_day.append(0)
        return points_for_the_next_day, []
