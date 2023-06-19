from z3 import *
import random
import Scheduler.problem_setup

# Set up the problem data
days_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] # One week

num_doctors = 21 # number of doctors working that week

doctors = [f"Doctor {i}" for i in range(num_doctors)] # for the meetings and spes. resp.

unassigned_samples = []

max_points_per_doctor = [100 for i in range(num_doctors)]

doc_routine = ['full_time' for i in range(num_doctors)]
#doc_routine[12] = '1/2'
#doc_routine[17] = '1/2'
#doc_routine[8] = '1/2'
#doc_routine[9] = '1/2'
#doc_routine[10] = '1/2'
#doc_routine[11] = '1/2'
#doc_routine[12] = '1/2'
#doc_routine[13] = '1/2'
#doc_routine[14] = '1/2'
#doc_routine[15] = '1/2'
#doc_routine[16] = '1/2'

#doc_routine[6] = '1/3'
#doc_routine[10] = '1/3'
#doc_routine[11] = '1/3'
#doc_routine[13] = '1/3'
#doc_routine[14] = '1/3'
#doc_routine[15] = '1/3'
#doc_routine[16] = '1/3'
#doc_routine[18] = '1/3'
#doc_routine[19] = '1/3'

# Store doctors who have earned extra points and the number of extra points they have earned
#Fratrekkslisten
deductionlist = {doctor : 0 for doctor in doctors}

# Point to earn with the different routines
for i in range(len(doc_routine)):
    if doc_routine[i] == 'full_time':
        max_points_per_doctor[i] = 24
    elif doc_routine[i] == '1/2':
        max_points_per_doctor[i] = 12 
    elif doc_routine[i] == '1/3':
        max_points_per_doctor[i] = 8

print(f'Max points per doctor: {max_points_per_doctor}')

# Meeting assigned for that week
meetings = ['Mammamøte', 'Uromøte', 'ØNH møte', 'Thorax møte', 'Gynmøte']
random.shuffle(meetings)
meeting_assignment = {}
for meeting in meetings:
    doctor = random.choice(doctors)
    while doctor not in meeting_assignment: # need to alter this
        meeting_assignment.setdefault(doctor, []).append(meeting)

#The special areas of responsibility for the week
special_resp = ['CITO', 'ØNH CITO', 'Gastro CITO', 'Lymfom/hema', 'nålebiopsi', 'beinmarg']
random.shuffle(special_resp)
special_resp_assignment = {}
for value in special_resp:
    doctor = random.choice(doctors)
    special_resp_assignment.setdefault(doctor, []).append(value)
    
print('Meetings this week:')
for doctor, meeting in meeting_assignment.items():
    print(f'{doctor} : {meeting}')
print()

print('Responsibilities this week:')
for doctor, value in special_resp_assignment.items():
    print(f'{doctor} : {value}')
print()

# Generate list of random amount of slices
def simulate_slices():
    slices = []
    for i in range(1,50):
        n = random.randint(1,1)
        slices.append(n)
    return slices

slices = [1,1,1,3,3,65,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,29,1,1,
          1,2,5,13,1,1,1,1,1,1,1,1,1,1,1,2,2,2,3,3,4,4,6,14,1,1,1,1,1,1,
          1,2,2,2,2,2,4,7,1,1,1,1,1,1,1,2,5,7,8,8,1,1,1,1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,2,2,2,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,3,
          6,6,8,1,1,1,1,1,1,1,1,1,2,2,2,4,15,1,1,1,1,1,1,1,2,3,5,10,10,10,
          1,1,1,1,1,1,6,7,12,1,1,1,1,1,1,2,2,2,2,2,4,4,10,1,1,1,3,10,10,1,
          1,1,1,1,1,1,2,3,7,53,1,2,3,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,
          3,3,3,3,3,3,4,5]

# List of samples ready for each day of the week
def slices_week(days):
    samples_week = []
    for day in days:
        #slices = simulate_slices()
        samples_week.append(slices)
    return samples_week

slices = slices_week(days_week)

# Simulate a week of assignments
for i, day in enumerate(days_week):
    num_samp_day = len(slices[i])
    print(f"Number of samples for {day}: {num_samp_day} samples")
    print(day)
    
    # Call task allocation program for current day
    problem = Scheduler.problem_setup.resource_scheduler(slices[i], num_doctors, 
                                                                 max_points_per_doctor, special_resp_assignment, deductionlist)
    assigned_points = problem[0]
    un_analyzed = problem[1]

    # Add the not analyzed samples to the list of slices for the next day
    slices.extend(un_analyzed)

    print(f'Remaining points: {assigned_points}')
    print()

    # the amount of points per doctors that will be their max for the next day
    for i in range(len(max_points_per_doctor)):
        max_points_per_doctor[i] += assigned_points[i]
        if doc_routine[i] == 'full_time':
            max_points_per_doctor[i] = min(max_points_per_doctor[i], 30) 
        elif doc_routine[i] == '1/2':
            max_points_per_doctor[i] = min(max_points_per_doctor[i], 18)
        elif doc_routine[i] == '1/3':
            max_points_per_doctor[i] = min(max_points_per_doctor[i], 15)
