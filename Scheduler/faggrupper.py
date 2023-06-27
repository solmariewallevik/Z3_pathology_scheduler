# Add the constraint that each tagged sample is assigned to the correct tagged doctor
    
    for sample, doctor in sample_doctor.items():
        doctor_index = doctor_indices[doctor]
    
        # Check if the doctor index is within the range of max_points_per_doctor list
        if doctor_index < len(max_points_per_doctor):
            # Calculate the total points assigned to the doctor for the sample
            sample_index = sample
            assigned_points = sum([If(assignments[sample][j], points[sample_index], 0) for j in range(num_doctors)])

            # Create a symbolic variable for the maximum allowed points for the doctor
            max_points = max_points_per_doctor[doctor_index]
            solver.add(max_points >= 0)

            # Add the constraint: assigned_points <= max_points
            solver.add(assigned_points <= max_points)

            # Check if the assigned_points is strictly less than max_points
            if is_false(solver.check(assigned_points == max_points)):
                # Check if there are other doctors with the same tag
                other_doctors = [d for d in sample_doctor.values() if d != doctor]
                if len(other_doctors) == 0:
                    # If there are no other doctors with the same tag, pass the sample to the next day
                    not_analyzed.append(Not(assignments[sample][doctor_index]))
                else:
                    # Assign the sample to a random doctor among the other doctors with the same tag
                    other_doctor = random.choice(other_doctors)
                    other_doctor_index = doctor_indices[other_doctor]
                    solver.add(assignments[sample][other_doctor_index] == True)
        else:
            # Handle the case where the doctor index is out of range
            not_analyzed.append(Not(assignments[sample][doctor_index]))
   

    # Ensure that each sample is assigned to exactly one doctor
    for sample, doctor in sample_doctor.items():
        assigned_doctor = doctor_indices[doctor]
        for other_doctor in range(num_doctors):
            if other_doctor == assigned_doctor:
                solver.add(assignments[sample][other_doctor] == True)
            else:
                solver.add(assignments[sample][other_doctor] == False)


    # Create a dictionary that matches each sample with a doctor based on shared FAGGRUPPE
    sample_doctor = {}
    used_doctors = set() #keep track of doctors already used for matching

    #Match doctors based on shared FAGGRUPPE
    
    for sample, sample_groups in sample_groups.items():
        matched_doctors = []
        for doctor, doctor_groups in doctors_spes.items():
            if any(group in sample_groups for group in doctor_groups):
                matched_doctors.append(doctor)
                # Choose a random doctor among the matched doctors for the sample
                #sample_doctor[sample] = doctor # sample y: doctor x

        match_found = False
        for doctors in matched_doctors:
            if doctor not in used_doctors:
                sample_doctor[sample] = doctor
                used_doctors.add(doctor)
                match_found = True
                break

        #If no match found based on tags, match randomly with any doctor
        if not match_found:
            available_doctors = set(doctors_spes.keys()) - used_doctors
            if available_doctors:
                random_doctor = random.choice(list(available_doctors))
                sample_doctor[sample] = random_doctor
                used_doctors.add(random_doctor)