import matplotlib.pyplot as plt
import numpy as np

# # Your histogram data
# histogram_data = {
#     "minimum": 68.93777529,
#     "einstein": 73.95163438,
#     "bounded_difference": 80.38956188,
#     "hamacher": 61.33398939
# }

# # Extract keys and values from the dictionary
# labels = list(histogram_data.keys())
# values = list(histogram_data.values())

# # Plot the histogram
# plt.bar(labels, values, edgecolor='black')

# # Add labels and title
# plt.xlabel('Histogram Bins')
# plt.ylabel('Defuzzifier Output')

# plt.yticks(np.arange(10, 101, 10))

# # Show the plot
# plt.show()

# import matplotlib.pyplot as plt

# # Data
# tnorms = ['minimum', 'algebraic', 'bounded_difference', 'hamacher']
# crisp_outputs = [63.53519343, 63.53519343, 50, 60.24512347]
# rule_strengths = [0.6765189638, 0.6765189638, 1, 0.4386366295]

# # Plotting
# fig, ax = plt.subplots()

# # Plotting the crisp output
# ax.bar(tnorms, crisp_outputs, alpha=0.7, label='Crisp Output')

# # Plotting the rule strength as line plot on secondary y-axis
# ax2 = ax.twinx()
# ax2.plot(tnorms, rule_strengths, color='red', marker='o', label='Rule Strength')

# # Setting labels and title
# ax.set_ylabel('Crisp Output')
# ax2.set_ylabel('Rule Strength')
# ax.set_xlabel('T-norms')
# plt.title('Crisp Output and Rule Strength for Different T-norms')

# # Adding legend
# ax.legend(loc='upper left')
# ax2.legend(loc='upper right')

# # Show the plot
# plt.show()

# Given defuzzifier outputs
# centroid = 60.24512347
# bisector = 67
# height = 80.5

# # Plotting the histogram
# plt.bar(['Centroid', 'Bisector', 'Height'], [centroid, bisector, height])
# plt.ylabel('Defuzzified Output')
# plt.title('Defuzzifier Output')
# plt.show()


# Given data
test_cases = [1, 2, 3, 4]
case1_output = [58.55683223, 80.81578947, 50, 50]
case2_output = [60.24512347, 80.81578947, 50, 50]

# Set up the figure and axis
fig, ax = plt.subplots()

# Set the width of the bars
bar_width = 0.35

# Set the positions for the bars
bar_positions_case1 = np.arange(len(test_cases))
bar_positions_case2 = bar_positions_case1 + bar_width

# Plot the bars for Case 1 and Case 2
bar1 = ax.bar(bar_positions_case1, case1_output, width=bar_width, label='Case 1')
bar2 = ax.bar(bar_positions_case2, case2_output, width=bar_width, label='Case 2')

# Add labels, title, and legend
ax.set_xlabel('Test Cases')
ax.set_ylabel('Output')
ax.set_title('Comparison of Fuzzy Models')
ax.set_xticks(bar_positions_case1 + bar_width / 2)
ax.set_xticklabels(test_cases)
ax.legend()

# Show the plot
plt.show()