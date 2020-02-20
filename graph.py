import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

from ParserChecker import *

#for Testing
# d = {'xss': 1, 'rfi': 1, 'lfi': 1, 'sql': 1}
# export = attackchecker(parser("accesssmall.log"), "/Users/waiqun/PycharmProjects/1002Proj", d)
# mylist = showflaggedIP(parser('accesssmall.log'), export)

xaxis = list()
yaxis = list()
for x in range(len(mylist)):
    xaxis.append(mylist[x][0])
for n in range(len(mylist)):
    yaxis.append(mylist[n][1])

print xaxis, yaxis
highest = max(yaxis)
freq = highest / 10
#resize graph
plt.figure(figsize=(20,6), dpi=100)
#
#UI for the legend

plt.bar(xaxis, yaxis, label='Flagged', color='blue', align='center')
plt.xticks(rotation=90)
plt.yticks(np.arange(0, max(yaxis), freq))
#
# Adding Title to the graph
plt.title('Data Analyze', fontdict={'fontname': 'comic Sans MS', 'fontsize': 20})

# #Adding label to the graph on the X axis and Y axis
plt.xlabel('Flagged IP')
plt.ylabel('Connection (Capture)')

# Adding a Legend
plt.legend(loc='upper right')

# Show plot
plt.tight_layout()
plt.show()
