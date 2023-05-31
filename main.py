from z3 import *
import random
import Scheduler.problem_setup

# Set up the problem data
days_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] # One week

num_doctors = 8 #number of doctors, think 8 per week is normal

doctors = [f"Doctor {i}" for i in range(num_doctors)] # for the meetings and spes. resp.

max_points_per_doctor = [24 for i in range(num_doctors)]

doc_routine = ['full_time' for i in range(num_doctors)]
doc_routine[5] = '1/2'

# Point to earn with the different routines
for i in range(len(doc_routine)):
    if doc_routine[i] == 'full_time':
        max_points_per_doctor[i] = 24
    elif doc_routine[i] == '1/2':
        max_points_per_doctor[i] = 11 #or max_points_per_doctor[i] = 12
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

#The special areas of responsibility for the week (should be passed to the next day)
special_resp = ['CITO', 'ØNH CITO', 'Gastro CITO', 'Lymfom/hema']
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
    for i in range(1,20):
        n = random.randint(1,20)
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

# Simulate a week of assignments
for i, day in enumerate(days_week):
    #print(f"Samples for {day}: {slices[i]}")
    print(day)
    # Call task allocation program for current day
    assigned_points = Scheduler.problem_setup.resource_scheduler(slices[i], num_doctors, max_points_per_doctor, special_resp_assignment)
    print(f'Remaining points: {assigned_points}')
    print()
    for i in range(len(max_points_per_doctor)):
        max_points_per_doctor[i] += assigned_points[i]
        max_points_per_doctor[i] = min(max_points_per_doctor[i], 30) #TODO: what to do when the routine is different. 
