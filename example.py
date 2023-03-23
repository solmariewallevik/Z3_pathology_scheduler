from z3 import *

#Times that each step takes
task_length = {
        1: 20,
        2: 50,
        3: 80,
        4: 50,
        5: 60,
        6: 45,
        7: 20,
        8: 25,
        9: 50,
        10: 30,
        11: 40,
        12: 50
}

s = Optimize()

#Variable for the time for each step to start. 
tx = {k: Int("t{}".format(k)) for k in task_length.keys()}
s.add(And([t >= 0 for t in tx.values()]))

#All the processes will have finished at some time in the future
tend = Int("tend")

#Restrictions
#2 cannot before 1, 3 not before step 2 and so on... 
#Tend cannot be samller than the time when the last step has finished
for i in [1, 2, 3]:
    s.add(tx[i] + task_length[i] <= tx[i+1])
s.add(tx[4] + task_length[4] <= tend)

for i in [5, 6, 7]:
    s.add(tx[i] + task_length[i] <= tx[i+1])
s.add(tx[8] + task_length[8] <= tend)

for i in [9, 10, 11]:
    s.add(tx[i] + task_length[i] <= tx[i+1])
s.add(tx[12] + task_length[12] <= tend)


#Colouring restriction: step 1,5 and 11 cant run at the same time etc.
#b1,5 will be true if step 1 goes before step 5, false otherwise.
def add_related_constraint(s, a, b):
    bo = Bool("b{},{}".format(a, b))
    s.add(
        If(bo, tx[a] + task_length[a] <= tx[b], tx[b] + task_length[b] <= tx[a]))

add_related_constraint(s, 1, 5)
add_related_constraint(s, 5, 11)
add_related_constraint(s, 1, 11)

add_related_constraint(s, 2, 7)
add_related_constraint(s, 7, 9)
add_related_constraint(s, 2, 9)

add_related_constraint(s, 3, 8)
add_related_constraint(s, 8, 10)
add_related_constraint(s, 3, 10)

add_related_constraint(s, 4, 6)
add_related_constraint(s, 6, 12)
add_related_constraint(s, 4, 12)

#Make the solver do its stuff. Carefully formatted. 
s.minimize(tend)
print(s.check())
m = s.model()

for i in sorted(task_length.keys()):
    print(tx[i], m[tx[i]])

print(tend, m[tend])

