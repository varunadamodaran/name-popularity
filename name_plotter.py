## Your code goes here!!
import glob
import re
import time
def load_names_data(data_folder,maximum_rank='all ranks'):
  rank = 0
  t1 = time.time()
  print('Loading files...')
  if(maximum_rank !='all ranks'):
    rank = int(maximum_rank)
  content = []
  name_dict = {}
  name_list = []
  for filename in glob.glob('data/yob*.txt'):
    year = re.compile('[0-9]+').findall(filename)
    year = int(year[0])
    name_list = []
    count = 0
    with open(filename, "r") as baby_data:
      first_male = 'Y'
      for x in baby_data:       
        name = re.compile('^[\w]+').findall(x)
        sex = re.compile('(?<=,)[M,F](?=,)').findall(x)
        if(sex[0] == 'M' and first_male == 'Y'):
          count = 0
          first_male = 'N'
        number_babies = re.compile('[\d]+$').findall(x)
        count += 1
        if(rank != 0 and count > rank):
          continue
        else:
          name_tuple = (name[0],sex[0],number_babies[0],count)
          name_list.append(name_tuple)
      name_dict[year]= name_list
  #print(name_dict[1880])
  t2 = time.time()
  print('Done.Time to load:'+str(t2-t1)+'seconds')
  return name_dict






















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
  if(sys.argv[2] != ''):
    rank = sys.argv[2]
    names_data = load_names_data(names_folder,rank)
  else:
    names_data = load_names_data(names_folder)
    
  names_to_plot = sys.argv[3:] #rest of the arguments are names to plot
  print(names_to_plot)
  print(names_data[1880])
  plot_names(names_data, names_to_plot)
    
  cmd = None
  datafile = None

  # try: #catch invalid argument lengths
  #   cmd = sys.argv[1]
  #   datafile = sys.argv[2]
  # except:
  #   print(INVALID_MSG)
  # else:
  #   if cmd == 'load':
      #G = load_names_data(datafile)
      #print("loaded graph with", len(G), "nodes and", G.size(), "edges")
    #elif cmd == 'analyze':
      #G = load_graph(datafile)
      #analyze_graph(G)
    #elif cmd == 'plot':
      #G = load_graph(datafile)
      #plot_graph(G)
    #else:
      #print(INVALID_MSG)
    #plot_names(names, ['Joel','Ada'])
