from z3 import *

# Set up the problem data
num_samples = 10
num_doctors = 3

samples = [f"sample_{i}" for i in range(num_samples)]
doctors = [f"doctor_{i}" for i in range(num_doctors)]

# Initialize Z3 solver
solver = Solver()

# Create variables for each sample-doctor assignment
assignments = [[Bool(f"{sample}_assigned_to_{doctor}") for doctor in doctors] for sample in samples]

# Add constraints to ensure each sample is assigned to exactly one doctor
for sample_assignments in assignments:
    solver.add(Or(sample_assignments))
    solver.add(Not(And(sample_assignments)))

# Add constraints to ensure each sample is assigned to at most one doctor
for i in range(num_samples):
    solver.add(sum([If(assignments[i][j], 1, 0) for j in range(num_doctors)]) <= 1)

# Add constraints to limit the number of samples each doctor can receive
for j in range(num_doctors):
    num_assigned_samples = sum([If(assignments[i][j], 1, 0) for i in range(num_samples)])
    solver.add(num_assigned_samples <= 4)  # limit to at most 4 samples per doctor

# Check if there is a valid solution and print the assignments
if solver.check() == sat:
    model = solver.model()
    doctor_assignments = {doctor: [] for doctor in doctors}  # initialize dictionary for each doctor's assignments
    for i in range(num_samples):
        for j in range(num_doctors):
            if is_true(model[assignments[i][j]]):
                doctor_assignments[doctors[j]].append(samples[i])  # add sample to doctor's assignments
    for doctor, assigned_samples in doctor_assignments.items():
        print(f"{doctor} is assigned samples: {', '.join(assigned_samples)}")
else:
    print("No valid assignment found.")
