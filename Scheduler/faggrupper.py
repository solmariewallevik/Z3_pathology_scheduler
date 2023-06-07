not_analyzed = ['Not(Sample2_analyzed)', 'Not(Sample4_analyzed)']
samples = ['Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5', 'Sample6']
num_samples = 6

slices = [1,2,3,4,5,6]


not_analyzed_dict = {}
for condition in not_analyzed:
    sample_name = condition.split('(')[1].split('_')[0]
    not_analyzed_dict[sample_name] = condition
print(not_analyzed_dict)

not_analyzed_samples = []
not_analyzed_slices = []
for sample in samples:
    if sample in not_analyzed_dict:
        not_analyzed_samples.append(sample)
        not_analyzed_slices.append(slices[samples.index(sample)])

print(not_analyzed_samples)
print(not_analyzed_slices)


un = [1,2]

un.extend(not_analyzed_slices)

print(un)
