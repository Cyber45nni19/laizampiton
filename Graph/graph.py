import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import pandas as pd
import numpy as np
import csv
from itertools import count
import random

style.use('ggplot')
data = pd.read_csv('Example.csv', delimiter=',')
df = pd.DataFrame(data)
x = df['NameOfAttack']
y = df['NumberofTimes']


#resize graph
plt.figure(figsize=(15,6.5), dpi=100)

#UI for the legend
plt.bar(x, y, label='Successful', color='blue')

# Adding Title to the graph
plt.title('Data Analze', fontdict={'fontname': 'comic Sans MS', 'fontsize': 20})

#Adding label to the graph on the X axis and Y axis
plt.xlabel('Attacks')
plt.ylabel('Num of attack (Successful)')

# X and Y axis Tickmarks (scale of your graph)
plt.yticks([0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300])


# Adding a Legend
plt.legend(loc='upper right')

# # Save figure on dpi 300 for high resolutions
# # plt.savefig('DataGraph', dpi=300)
#
# Show plot
plt.tight_layout()
plt.show()
