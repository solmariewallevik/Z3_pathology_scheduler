from z3 import *
import random
import Scheduler.problem_setup

# Set up the problem data
# This is for one week
days_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
num_doctors = 10 #number of doctors, think 8 per week is normal

# Generate list of random amount of slices
def simulate_slices():
    slices = []
    for i in range(1,15):
        n = random.randint(1,80)
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
    print(f"Samples for {day}: {slices[i]}")
    print()
    # Call task allocation program for current day
    Scheduler.problem_setup.resource_scheduler(slices[i], num_doctors)
