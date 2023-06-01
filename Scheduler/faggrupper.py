# Add constraints to ensure each sample is assigned to exactly one doctor
for i in range(num_samples):
    solver.add(Or([assignments[i][j] for j in range(num_doctors)])) #Maybe not
    
# Add constraint to ensure each special sample is assigned to exactly one doctor
for i in range(num_special_samples):
    solver.add(Or([spes_assignments[i][j] for j in range(num_doctors)]))

# Add constraints to ensure each sample is assigned to at most one doctor
for i in range(num_samples):
    solver.add(sum([If(assignments[i][j], 1,0) for j in range(num_doctors)]) <= 1)

# Add constraint to ensure each special sample is assigned to at most one doctor
for i in range(num_special_samples):
    solver.add(sum([If(spes_assignments[i][j], 1, 0) for j in range(num_doctors)]) <= 1)

# Add the constraint that each sample is assigned to one doctor
for sample in range(num_samples):
    solver.add(And(sample_vars[sample] >= 0, sample_vars[sample] < num_doctors))

#Add the constraint that each special sample is assigned to one doctor
for sample in range(num_special_samples):
    solver.add(And(special_sample_vars[sample] >= 0, special_sample_vars[sample] < num_doctors))
