import pandas
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

ind = np.array([0, 1])

width = 0.4

fig, ax = plt.subplots()

ax.barh(ind, np.array([0.0452,0.0537]), width, color='orange', label='Candidate Pool with Greedy Cover')
ax.barh(ind + width, np.array([0.0080425, 0.0172589]), width, color='blue', label='Pure Random Selection')


ax.set(yticks=ind + width, yticklabels=np.array(['20', '52']),
ylim=[2*width - 1, len(ind)])


ax.legend(loc='upper right')
plt.savefig("plot_eth.jpg")