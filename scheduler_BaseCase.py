from z3 import *

# Define the problem parameters
x = 10 # number of samples
y = 3 # number of doctors
max_points = 24 # maximum number of points per doctor
points_per_sample = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12] # points for each sample

# Initialize z3 solver
s = Solver()

# Define the variables
samples = [Int(f"sample_{i}") for i in range(x)] # number of samples assigned to each doctor
doctors = [Int(f"doctor_{i}") for i in range(y)] # number of points assigned to each doctor

# Define constraints
for i in range(y):
    # Each doctor must have between 0 and max_points points
    s.add(doctors[i] >= 0)
    s.add(doctors[i] <= max_points)
    
    # Each sample can only be assigned to one doctor
    sample_constraints = [Or(samples[j] != i, samples[j] == -1) for j in range(x)]
    s.add(And(sample_constraints))
    
    # The sum of the points assigned to each doctor must be less than or equal to max_points
    doctor_constraints = [If(samples[j] == i, points_per_sample[j], 0) for j in range(x)]
    s.add(doctors[i] == Sum(doctor_constraints))
    
# Add the constraint that each sample must be assigned to exactly one doctor
sample_constraints = [Or(samples[i] == j, samples[i] == -1) for i in range(x) for j in range(y)]
s.add(And(sample_constraints))

# Solve the problem
if s.check() == sat:
    m = s.model()
    for i in range(y):
        assigned_samples = [j for j in range(x) if m.eval(samples[j]) == i]
        points_assigned = sum([points_per_sample[j] for j in assigned_samples])
        print(f"Doctor {i+1} assigned samples: {assigned_samples}, total points: {points_assigned}")
else:
    print("No solution found")
