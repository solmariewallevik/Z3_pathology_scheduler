import random
import problem_setup 
import scheduler_BaseCase

spes_table = {
    'u': 'Uro-group',
    'x': 'Gyno-group',
    'p': 'Perinatal-group',
    'm': 'Mom-group',
    'g': 'Gastro-group',
    'h': 'Skin-group',
    'l': 'Lymfoma-group',
    's': 'Sarkoma-group',
    'r': 'ear-nose-thought-group',
    'y': 'Kidney-group',
    'oral': 'oral',
    'nevro': 'nevro'
    }

def generate_doctors_spes():
    path_groups_doc = list(spes_table.keys())
    random.shuffle(path_groups_doc)

    doctors_spes = {}
    for doctor in doctors: 
        num_keys = random.randint(1,2)
        doctors_spes[doctor] = {}
        for i in range(num_keys):
            key = path_groups_doc.pop(0)
            doctors_spes[doctor][key] = spes_table[key]

    return doctors_spes