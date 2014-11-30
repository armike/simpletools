#!/usr/local/bin/python
import os, datetime
import matplotlib.pyplot as plt

def main():
    """
    Plots the powers of 2 and powers of 3 on the same graph.
    """
    # Creates a series that contains the powers of 2
    seriesA = Series([0, 1, 2, 3, 4,   5,  6,   7,   8,   9,   10],
                     [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024],
                     "Powers of 2")

    # Creates a series that contains the powers of 3
    # 
    seriesB = Series(range(8),
                     [3**x for x in range(8)],
                     "Powers of 3"
                     )

    # I know serieses isn't a word
    # 
    seriesesToPlot = [seriesA, seriesB]
    plotLineGraph(seriesesToPlot,
                  "/tmp/graph.png",
                  )

class Series(object):
    """
    Data points for a single line in a line graph.
    """
    def __init__(self, indepVar, depVar, label):
        """
        :Parameters:
            indepVar : `float list`
                The value of the independent variable for each index i.
            depVar : `float list`
                The value of the dependent variable for each index i.
                Should be the same size as indepVar.
            label : `str`
                Name of this series.
        """
        self.indepVar = indepVar
        self.depVar   = depVar
        self.label    = label

def plotLineGraph(serieses,
                  outpath,
                  yLimits=None, xLimits=None,
                  width=None, height=None,
                  xLabel=None, yLabel=None,
                  title=None,
                  dpi=72.0,
                  gridColor=.75,
                  ):
    """
    Plot the given Series objects to the file given by outpath.
    :Parameters:
        serieses : `Series list`
            List of Series objects, each one containing a line plot of data.
        outpath : `str`
            Path to write the resulting image on disk.
        yLimits : `int tuple`
            Min and Max value for the y axis.
        xLimits : `int tuple`
            Min and Max value for the x axis.
        width : `int`
            Width of the final image in pixels.
        height : `int`
            Height of the final image in pixels.
        title : `str`
            Title of the chart.
        dpi : `float`
            Dots per inch.
        gridColor : `float`
            Darkness of the grid.
    """
    fig = plt.figure()

    # Make a page that has 1 row, 1 column, 1 plot
    # 
    ax = fig.add_subplot(1, 1, 1)

    # Plot each series as a line.
    # 
    plots = []
    for s in serieses:
        plots += ax.plot(s.indepVar, s.depVar, label=s.label)

    # Place the labels in the "best" spot, according to matplotlib.
    # 
    handles,labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='best')

    # Label the x and y axes.
    # 
    ax.xaxis.set_label_text(xLabel, size=10)
    ax.yaxis.set_label_text(yLabel, size=10)

    # Display the grid, set its darkness with a float.
    # 
    ax.grid(True, color=str(gridColor))

    # Set the title of the graph.
    # 
    if title:
        ax.set_title(title)

    # width and height are in pixels, we need inches.
    # 
    if width:
        fig.set_figwidth(width/dpi)
    if height:
        fig.set_figheight(height/dpi)

    # Set the x and y boundaries for the chart if requested.
    # 
    if yLimits:
        ax.set_ylim(float(yLimits[0]), float(yLimits[1]))

    if xLimits:
        ax.set_xlim(float(xLimits[0]), float(xLimits[1]))

    # Close the file descriptor opened.
    # 
    fig.savefig(outpath, dpi=dpi, format='png')
    print "wrote chart to %s" % (outpath)

    # Render the graph interactively.
    # 
    plt.show()

    
    return outpath

def posixTimesToDates(posixTimes):
    """
    :Parameters:
        posixTimes : `int list`
            List of posix time values.
    :Returns:
        List of dates understood by matplotlib.
    :Rtype:
        `datetime list`
    """
    dates = [datetime.datetime.fromtimestamp(s) for s in posixTimes]
    return dates

if __name__ == "__main__":
    main()
