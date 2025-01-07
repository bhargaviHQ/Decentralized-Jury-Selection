import matplotlib.pyplot as plt

from matplotlib.ticker import ScalarFormatter

plt.figure(figsize=(20, 12))
# plt.barh([ r'$j=6$', r'$j=12$', r'$j=20$', r'$j=52$'],
# [0.0298609, 0.037468, 0.043526, 0.054161], align='center', color='dimgray',label=r'$\mathcal{FS}(\mathcal{C},\mathcal{G})$')

# resolution_value = 1200

# plt.xticks(fontsize=30) 
# plt.yticks(fontsize=30) 
# plt.ylabel("Varying Jury Sizes",fontsize=33, labelpad=20)
# plt.xlabel('Fractional Node Coverage with radius = 2',fontsize=33, labelpad=20)

# plt.savefig("eth_pool_jury.jpg")




# plt.figure(figsize=(24, 12))
# plt.barh([ r'$j=6$', r'$j=12$', r'$j=20$', r'$j=52$'],
# [1.7551040099545606e-06, 4.440728090439679e-06, 7.973841219777245e-06, 1.6611930612979378e-05], align='center', color='dimgray',label=r'Pure Random Selection')

# resolution_value = 1200
# plt.clf
# plt.xticks(fontsize=30) 
# plt.yticks(fontsize=30) 
# plt.ylabel("Varying Jury Sizes",fontsize=33, labelpad=20)
# plt.xlabel('Fractional Node Coverage with radius = 2',fontsize=33, labelpad=20)

# plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))

# plt.savefig("eth_RANDOM_jury.jpg")


# LOG LOG : 

import numpy as np

x_positions = np.arange(len([ r'$j=6$', r'$j=12$', r'$j=20$', r'$j=52$']))



plt.loglog([ 6, 12, 20,52], [0.0298609, 0.037468, 0.043526, 0.054161], marker='o', linestyle='-', linewidth=4,label=r'$\mathcal{F}=(\mathcal{C},\mathcal{G})$',markersize=10)
plt.loglog([  6, 12, 20,52], [1.7551040099545606e-06, 4.440728090439679e-06, 7.973841219777245e-06, 1.6611930612979378e-05], marker='s', linestyle='-',linewidth=4, label='Pure-Random',markersize=10)


resolution_value = 1200
plt.clf
plt.legend(fontsize=30)
plt.xticks(fontsize=30) 
plt.yticks(fontsize=30) 
plt.xlabel("Varying Jury Sizes",fontsize=33, labelpad=20)
plt.ylabel('Fractional Node Coverage with radius = 2',fontsize=28, labelpad=20)
plt.grid(True)

x_ticks = [ 6, 12, 20,52]
plt.xticks(x_ticks, [str(tick) for tick in x_ticks])


plt.savefig("eth_log_lin_jury.jpg")


