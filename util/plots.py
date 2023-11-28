import matplotlib.pyplot as plt

# Your histogram data
histogram_data = {
    "minimum": 68.93777529,
    "einstein": 73.95163438,
    "bounded_difference": 80.38956188,
    "hamacher": 61.33398939
}

# Extract keys and values from the dictionary
labels = list(histogram_data.keys())
values = list(histogram_data.values())

# Plot the histogram
plt.bar(labels, values, edgecolor='black')

# Add labels and title
plt.xlabel('Histogram Bins')
plt.ylabel('Defuzzifier Output')

plt.yticks(np.arange(10, 101, 10))

# Show the plot
plt.show()