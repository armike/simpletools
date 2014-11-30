#!/usr/local/bin/python
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot([101, 102, 110, 111], [10, 20, 50, 60])
ax.plot([101, 102, 110, 111], [15, 23, 80, 10])
labels = [label.get_text() for label in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticklabels(labels)
# ax.xaxis.set_tick_params(labelsize=4)
ax.xaxis.set_label_text("Frame", size=10)
ax.yaxis.set_label_text("Minutes",size=10)
ax.grid(True, color='.75')

# ax2 = fig.add_subplot(1, 1, 2)

fig.set_figwidth(4.0)
fig.set_figheight(2.0)
fig.savefig('test.png', format='png')
