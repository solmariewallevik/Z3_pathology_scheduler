from z3 import *
import random
import Scheduler.problem_setup

# Set up the problem data
# This is for one week
days_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
num_doctors = 10 #number of doctors, think 8 per week is normal

max_points_per_doctor = [24 for i in range(num_doctors)]
#max_points_per_doctor = 24

# Generate list of random amount of slices
def simulate_slices():
    slices = []
    for i in range(1,23):
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
    #Scheduler.problem_setup.resource_scheduler(slices[i], num_doctors, max_points_per_doctor)
    assigned_points = Scheduler.problem_setup.resource_scheduler(slices[i], num_doctors, max_points_per_doctor)
    print(f'Remaining points: {assigned_points}')
    print()
    #TODO: add the assigned_points to the max for each doctor.
    for i in range(len(max_points_per_doctor)):
        max_points_per_doctor[i] += assigned_points[i]
        max_points_per_doctor[i] = min(max_points_per_doctor[i], 30)
