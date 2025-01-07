import matplotlib.pyplot as plt
import numpy as np

# # Sample data
# categories = ['Category A']
# values1 = [10]
# values2 = [15]

# categories = np.array([r'$(\mathcal{C},\mathcal{B})$', r'$(\mathcal{C},\mathcal{G})$', r'$(\mathcal{P},\mathcal{B})$', r'$(\mathcal{P},\mathcal{G})$ ', r'$(\mathcal{S},\mathcal{B})$', r'$ (\mathcal{S},\mathcal{G})$'])
# values1 = np.array([0.011,0.0108,0.04,0.04,0.04,0.04])
# values2 = np.array([0.0031,0.0031,0.0038,0.0039,0.0038,0.0038])

# # Set up positions for the bars
# positions = np.arange(len(categories))

# # Set up the figure and axis
# fig, ax = plt.subplots()

# # Plot the first set of values
# bar1 = ax.bar(positions - 0.2, values1, 0.4, label='Memory-less', color='black')

# # Plot the second set of values
# bar2 = ax.bar(positions + 0.2, values2, 0.4, label='Memory-enhanced', color='grey')

# # Add labels and title
# ax.set_xticks(positions)
# ax.set_xticklabels(categories)
# ax.set_xlabel('Fair-Spread Algorithm')
# ax.set_ylabel('Disparity Q(J) in juror selection')
# plt.title('Comparision of Memory-enhanced and Memory-less')

# # Add legend
# ax.legend()

# # Display the plot
# plt.show()
########################################################


# x = np.array([r'$(\mathcal{C},\mathcal{B})$', r'$(\mathcal{C},\mathcal{G})$', r'$(\mathcal{P},\mathcal{B})$', r'$(\mathcal{P},\mathcal{G})$ ', r'$(\mathcal{S},\mathcal{B})$', r'$ (\mathcal{S},\mathcal{G})$'])
# memless_dis = np.array([0.011,0.0108,0.04,0.04,0.04,0.04])
# memEnhanced_dis = np.array([0.0031,0.0031,0.0038,0.0039,0.0038,0.0038])


# memless_eq = np.array([66.56,65.36,70.31,70.19,109.18,108.73])
# memEnhanced_eq = np.array([20.74,20.50,12.35,12.44,17.62,17.67])

# # Set up positions for the bars
# positions = np.arange(len(x))

# # Set up the figure and axis
# fig, ax1 = plt.subplots()

# # Plotting the first set of bars for y1 and y2
# bar1 = ax1.bar(positions - 0.2, memless_dis, 0.4, label='Memory-less', color='black')
# bar2 = ax1.bar(positions + 0.2, memEnhanced_dis, 0.4, label='Memory-enhanced', color='grey')

# # Creating a secondary y-axis for z1 and z2 as lines
# ax2 = ax1.twinx()
# line1, = ax2.plot(positions, memless_eq, label='Memory-less', color='darkred', marker='o')
# line2, = ax2.plot(positions, memEnhanced_eq, label='Memory-enhanced', color='darkorange', marker='s')

# # Add labels and title
# ax1.set_xticks(positions)
# ax1.set_xticklabels(x)
# ax1.set_xlabel('X-axis')
# ax1.set_ylabel('Disparity Q(J) in juror selection', color='black')
# ax2.set_ylabel('Equality E(J) in juror selection', color='darkred')
# plt.title('Comparision of Disparity and Equality for Memory-less and Memory-enhanced')

# # Add legends
# ax1.legend(loc='upper left')
# ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.9))
# # Display the plot
# plt.show()


#########################################################################################################
#########################################################################################################
#########################################################################################################

# x = np.array([r'$(\mathcal{C},\mathcal{B})$', r'$(\mathcal{C},\mathcal{G})$', r'$(\mathcal{P},\mathcal{B})$', r'$(\mathcal{P},\mathcal{G})$ ', r'$(\mathcal{S},\mathcal{B})$', r'$ (\mathcal{S},\mathcal{G})$'])
# memless_dis = np.array([0.011,0.0108,0.04,0.04,0.04,0.04])
# memEnhanced_dis = np.array([0.0031,0.0031,0.0038,0.0039,0.0038,0.0038])


# memless_eq = np.array([66.56,65.36,70.31,70.19,109.18,108.73])
# memEnhanced_eq = np.array([20.74,20.50,12.35,12.44,17.62,17.67])


# # Create the first plot
# plt.subplot(2, 1, 1)  # 2 rows, 1 column, plot 1
# plt.plot(x, memless_dis, label='Memory-less')
# plt.plot(x, memEnhanced_dis, label='Memory-enhanced')
# plt.xlabel('Fair-Spread Algorithm',fontsize=20)
# plt.ylabel('Q(J) values ',fontsize=20)
# plt.title('(a) Comparision of Disparity Metric',fontsize=20)

# plt.xticks(fontsize=20) 
# plt.yticks(fontsize=20) 
# plt.legend()

# # Create the second plot
# plt.subplot(2, 1, 2)  # 2 rows, 1 column, plot 2
# plt.plot(x, memless_eq, label='Memory-less')
# plt.plot(x, memEnhanced_eq, label='Memory-enhanced')
# plt.xlabel('Fair-Spread Algorithm',fontsize=20)
# plt.ylabel('E(J) values',fontsize=20)
# plt.title('(b) Comparision of Equality Metric',fontsize=20)
# plt.legend()


# plt.xticks(fontsize=20) 
# plt.yticks(fontsize=20) 
# # Adjust layout to prevent overlapping
# plt.tight_layout()

# # Save the figure
# plt.savefig('two_plots_in_one_figure.png')

# # Show the figure (optional)
# plt.show()


#########################################################################################################
#########################################################################################################
#########################################################################################################

import matplotlib.pyplot as plt
import numpy as np

# # Sample data
# x = np.array([1, 2, 3, 4])  # x-axis values
# y1 = np.array([10, 15, 7, 12])  # y1 values
# y2 = np.array([5, 12, 10, 8])   # y2 values
# z1 = np.array([8, 11, 5, 9])    # z1 values
# z2 = np.array([3, 8, 6, 4])     # z2 values

algorithms = np.array([r'$(\mathcal{C},\mathcal{B})$', r'$(\mathcal{C},\mathcal{G})$', r'$(\mathcal{P},\mathcal{B})$', r'$(\mathcal{P},\mathcal{G})$ ', r'$(\mathcal{S},\mathcal{B})$', r'$ (\mathcal{S},\mathcal{G})$'])
memless_dis = np.array([0.011,0.0108,0.04,0.04,0.04,0.04])
memEnhanced_dis = np.array([0.0031,0.0031,0.0038,0.0039,0.0038,0.0038])


memless_eq = np.array([66.56,65.36,70.31,70.19,109.18,108.73])
memEnhanced_eq = np.array([20.74,20.50,12.35,12.44,17.62,17.67])


# Plotting the first bar plot
plt.figure(figsize=(10, 5))  # Adjust the figure size as needed

plt.subplot(1, 2, 1)  # Subplot for the first bar plot
plt.bar(algorithms, memless_dis, width=0.4, label='Memory-less', color='grey')
plt.bar(algorithms, memEnhanced_dis, width=0.4, label='Memory-enhanced', color='black')
plt.xlabel('Fair-Spread Algorithm',fontsize=20)
plt.ylabel('Q(J) values ',fontsize=20)
plt.xticks(fontsize=15) 
plt.yticks(fontsize=15) 
plt.title('(a) Comparison of Disparity Metric',fontsize=20)
plt.legend()

  
# Plotting the second bar plot
plt.subplot(1, 2, 2)  # Subplot for the second bar plot
plt.bar(algorithms, memless_eq, width=0.4, label='Memory-less', color='grey')
plt.bar(algorithms, memEnhanced_eq, width=0.4, label='Memory-enhanced', color='black')
plt.xlabel('Fair-Spread Algorithm',fontsize=20)
plt.ylabel('E(J) values',fontsize=20)
plt.xticks(fontsize=15) 
plt.yticks(fontsize=15) 
plt.title('(b) Comparison of Equality Metric',fontsize=20)
plt.legend()

# Add tight layout
plt.tight_layout()

# Show the plot
plt.show()

