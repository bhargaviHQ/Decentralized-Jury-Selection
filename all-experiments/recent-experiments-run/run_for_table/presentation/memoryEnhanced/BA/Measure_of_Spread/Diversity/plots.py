import matplotlib.pyplot as plt

plt.figure(figsize=(24, 12))
plt.barh([r'$(\mathcal{C},\mathcal{B})$', r'$(\mathcal{C},\mathcal{G})$', r'$(\mathcal{P},\mathcal{B})$', r'$(\mathcal{P},\mathcal{G})$ ', r'$(\mathcal{S},\mathcal{B})$', r'$ (\mathcal{S},\mathcal{G})$', "Pure-\nRandom"],
[0.066929, 0.069285, 0.046903, 0.048072, 0.061586, 0.062194, 0.009870], align='center', color='dimgray')

resolution_value = 1200

plt.xticks(fontsize=30) 
plt.yticks(fontsize=30) 
plt.ylabel("Jury Selection Algorithms",fontsize=33, labelpad=20)
plt.xlabel('Ratio of Uniquely covered nodes to total nodes',fontsize=33, labelpad=20)

plt.savefig("Compare_with_Random_final.jpg")