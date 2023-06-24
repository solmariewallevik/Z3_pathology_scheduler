import matplotlib.pyplot as plt

# Sample data
categories = ['Category A', 'Category B', 'Category C', 'Category D']
values1 = [25, 40, 30, 35]
values2 = [30, 35, 20, 45]

# Plotting the bar chart
plt.bar(categories, values1, label='Schedule 1')
plt.bar(categories, values2, label='Schedule 2')

# Adding labels and title
plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Comparison of Schedules')

# Adding a legend
plt.legend()

# Displaying the chart
plt.show()