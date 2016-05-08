## Your code goes here!!




def plot_names(data, names=[]):
    """Plots the given list of names in a web-based visualization.

    Params:
        data  - a list of name records (e.g., tuples) to act as a data source
        names - a list of names (strings) which should be plotted
    """

    import plotly
    from plotly.graph_objs import Scatter, Scattergl, Layout

    traces = [] #all the lines to draw

    for name in names:
        for sex in ['M','F']: # draw lines for both sexes:
            try:
                x_vals = [] #the years for each data point
                y_vals = [] #the ranks for each data point
                labels = [] #the labels for each data point

                #TODO: find the record for the name & sex
                # if the record exists (it may not!)
                # go through each year in the record
                #   add the year to the list of x_vals
                #   add the rank to the list of y_vals
                #   add a label (e.g., "Count: 598") to the list of labels

                trace = Scatter(x=x_vals, y=y_vals, text=labels, name=name+" ("+sex+")", mode='lines', hoverinfo='text')
                traces.append(trace)
            except (KeyError): #if record key was not found, don't crash
                pass

    layout = Layout(title='Baby Name Popuarlity Over Time',
                xaxis = dict(title='Year',showgrid=False, showline=True, dtick=5),
                yaxis = dict(title='Popularity Ranking', showgrid=True, showline=True, zerolinewidth=0, autorange='reversed', dtick=100),
            )
    plotly.offline.plot({"data": traces, "layout": layout})


if __name__ == '__main__':
    import sys
    names_folder = sys.argv[1] #get the folder name from the command-line
    names_data = load_names_data(names_folder)
    
    names_to_plot = sys.argv[2:] #rest of the arguments are names to plot
    plot_names(names_data, names_to_plot)
    #plot_names(names, ['Joel','Ada'])
