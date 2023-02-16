from z3 import *

# Define the problem data
n = 5  # number of tasks
m = 3  # number of workers
tasks = ['task1', 'task2', 'task3', 'task4', 'task5']
points = [8, 6, 10, 9, 7]
workers = ['worker1', 'worker2', 'worker3']
capacities = [24, 24, 24]

# Define the decision variables
x = [[Int("x_%s_%s" % (i+1, j+1)) for j in range(m)] for i in range(n)]

# Create an instance of the Optimize class
opt = Optimize()

# Define the constraints
for i in range(n):
    opt.add(sum([x[i][j] for j in range(m)]) == 1)
for j in range(m):
    opt.add(sum([x[i][j] * points[i] for i in range(n)]) <= capacities[j])

# Define the objective function
objective = Sum([x[i][j] * points[i] for i in range(n) for j in range(m)])
opt.minimize(objective)

# Solve the problem and print the solution
if opt.check() == sat:
    m = opt.model()
    for j in range(m):
        for i in range(n):
            if m.eval(x[i][j]) == 1:
                print("%s assigned to %s" % (tasks[i], workers[j]))
else:
    print("No solution found")