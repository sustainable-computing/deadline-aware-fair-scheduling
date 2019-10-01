import numpy as np
import matplotlib.pyplot as plt
import utility as util
import sys
import plot

data = util.load_dict('data.txt')
algos = [key for key in data[0]]

jain_mean = []
jain_std = []
soc_mean = []
jain_color = []
soc_color = []

for algo in algos:
    jain_mean.append(data[0][algo]['jain'][0])
    jain_color.append((.9, .1, .1, .8))
    
    jain_mean.append(data[1][algo]['jain'][0])
    jain_color.append((.1, .9, .1, .8))

    jain_std.append(data[0][algo]['jain'][1])
    jain_std.append(data[1][algo]['jain'][1])
    
    soc_mean.append(data[0][algo]['soc'][0])
    soc_color.append((.9, .1, .5, .99))
    
    soc_mean.append(data[1][algo]['soc'][0])
    soc_color.append((.1, .9, .5, .99))

#color = np.array(color)

ind = []
for i in range(1, len(algos)+1):
    ind.append(3*i-2)
    ind.append(3*i-1)
ind = np.array(ind)

x_ind = [0.05+(ind[i]+ind[i+1])/2.0 for i in range(0, len(ind), 2)]

fig = plt.figure()
ax = fig.add_subplot(111)


#ax2 = ax.twinx()
rec = ax.bar(ind, jain_mean, 0.6, color=jain_color, align='center', yerr=jain_std, hatch='--', label='jain_index')
plot.autolabel(rec, ax)
rec = ax.bar(ind+0.25, soc_mean, 0.6, color=soc_color, align='center', hatch='//', label='% of EV')
plot.autolabel(rec, ax)

plt.xticks(x_ind, algos)
ax.yaxis.set_ticks_position("left")
ax.set_ylabel('Values')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=5, fancybox=True, shadow=True) 
#ax2.yaxis.set_ticks_position("left")

plt.tight_layout()
plt.show()
'''
from pychartdir import *

# The data for the bar chart
data0 = [100, 125, 156, 147, 87, 124, 178, 109, 140, 106, 192, 122]
data1 = [122, 156, 179, 211, 198, 177, 160, 220, 190, 188, 220, 270]
data2 = [167, 190, 213, 267, 250, 320, 212, 199, 245, 267, 240, 310]
labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

# Create a XYChart object of size 580 x 280 pixels
c = XYChart(580, 280)

# Add a title to the chart using 14pt Arial Bold Italic font
c.addTitle("Product Revenue For Last 3 Years", "arialbi.ttf", 14)

# Set the plot area at (50, 50) and of size 500 x 200. Use two alternative background colors (f8f8f8
# and ffffff)
c.setPlotArea(50, 50, 500, 200, 0xf8f8f8, 0xffffff)

# Add a legend box at (50, 25) using horizontal layout. Use 8pt Arial as font, with transparent
# background.
c.addLegend(50, 25, 0, "arial.ttf", 8).setBackground(Transparent)

# Set the x axis labels
c.xAxis().setLabels(labels)

# Draw the ticks between label positions (instead of at label positions)
c.xAxis().setTickOffset(0.5)

# Add a multi-bar layer with 3 data sets
layer = c.addBarLayer2(Side)
layer.addDataSet(data0, 0xff8080, "Year 2003")
layer.addDataSet(data1, 0x80ff80, "Year 2004")
layer.addDataSet(data2, 0x8080ff, "Year 2005")

# Set 50% overlap between bars
layer.setOverlapRatio(0.5)

# Add a title to the y-axis
c.yAxis().setTitle("Revenue (USD in millions)")

# Output the chart
c.makeChart("overlapbar.png")
'''
