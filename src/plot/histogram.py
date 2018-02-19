import matplotlib.pyplot as plt

def plot_histogram(dataframe):
    try:
        plt.clf()  # this clears the plot so can start
        histogram_plot = dataframe.hist(bins=150, log=True, sharey=True, sharex=True)
        plt.xlim(0, 3000000)
        plt.show()
    except:
        raise
    else:
        return histogram_plot
