import random
import problem_setup
'''
spes_table = {
    'u': 'Urogruppen',
    'x': 'Gynogruppen',
    'p': 'Perinatalgruppen',
    'm': 'Mammagruppen',
    'g': 'Gastrogruppen',
    'h': 'Hudgruppen',
    'l': 'Lymfomgruppen',
    's': 'Sarkomgruppen',
    'r': '�re-nese-hals-gruppen',
    'y': 'Nyregrupper',
    'oral': 'oral',
    'nevro': 'nevro'
    }


path_groups = list(spes_table.keys()) #list of the keys in spes_table
random.shuffle(path_groups) #shuffle the keys so that they are assigned randomly


doctors_spes = {} #create a dictionary to store the assigned faggruppe for each doctor
#iterate over the list of doctors and assign 1 or 2 faggrupper randomly
for doctor in doctors: 
    num_keys = random.randint(1,2)
    doctors_spes[doctor] = {}
    for i in range(num_keys):
        key = path_groups.pop(0)
        doctors_spes[doctor][key] = spes_table[key]

#print the assigned keys for each doctor.
for doctor, key_values in doctors_spes.items():
    print(f"{doctor}: {', '.join(f'{value} ({key})' for key, value in key_values.items())}")
print()
'''