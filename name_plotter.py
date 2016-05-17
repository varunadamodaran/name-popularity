## Your code goes here!!
import glob
import re
import time
import collections
import operator
from collections import namedtuple
from operator import attrgetter

 
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
  #print(name_dict[1972])
  t2 = time.time()
  print('Done.Time to load:'+str(t2-t1)+' seconds')
  transformed_data = transform_data_hashmap(name_dict)
  return transformed_data



def transform_data(name_dict):
  print('Transforming data ...')
  t1 = time.time()
  Record = namedtuple('Record','name sex year')
  name_list = []
  year_new = {}
  record_found = 'N'
  for year in name_dict:
    for name_tuple in name_dict[year]:
      baby_name = name_tuple[0]
      baby_sex = name_tuple[1]
      baby_count = name_tuple[2]
      baby_rank = name_tuple[3]
      record_found = 'N'
      year_new = {}
      for record in name_list:
        if (baby_name == record.name and baby_sex == record.sex):
          count_rank_tuple = (baby_count,baby_rank)
          record.year[year] = count_rank_tuple
          record_found = 'Y'
      if(record_found == 'N'):
        count_rank_tuple = (baby_count,baby_rank)
        year_new[year] = count_rank_tuple
        new_record = Record(baby_name,baby_sex,year_new)
        name_list.append(new_record)
        
  t2 = time.time()
  print('Done.Time to transform:'+str(t2-t1)+' seconds')
  # for tup in name_list:
  #   if (tup.name == 'Sophia'):
  #     print(tup)
  return name_list

def transform_data_hashmap(name_dict):
  print('Transforming data ...')
  t1 = time.time()
  Record = namedtuple('Record','name sex year')
  name_list = []
  year_new = {}
  new_dict = {}
  year_list = []
  record_found = 'N'
  for year in name_dict:
    for name_tuple in name_dict[year]:
      baby_name = name_tuple[0]
      baby_sex = name_tuple[1]
      new_tuple = (baby_name,baby_sex)
      baby_count = name_tuple[2]
      baby_rank = name_tuple[3]
      record_found = 'N'
      year_new = {}
      year_old = {}
      for key,value in new_dict.items():
        if (key == new_tuple):
          count_rank_tuple = (baby_count,baby_rank)
          value[year] = count_rank_tuple
          # year_old[year] = count_rank_tuple
          # year_list.append(year_old)
          # new_dict[key] = year_list
          record_found = 'Y'
      if(record_found == 'N'):
        count_rank_tuple = (baby_count,baby_rank)
        year_new[year] = count_rank_tuple
        new_dict[new_tuple] = year_new       
  t2 = time.time()
  print('Done.Time to transform:'+str(t2-t1)+' seconds')
  # print(new_dict[('John','M')])
  # print(new_dict[('Jennifer','F')])
  return new_dict

def find_name_record_linear(name_list,name,sex):
  for record in name_list:
    if (str(record.name) == str(name) and str(record.sex) == str(sex)):
      return record
  return "None"

def find_name_record_binary(name_list,name,sex):
  new_list = sorted(name_list, key=attrgetter('name'))
  mid = new_list[0]
  lo = 0
  hi = None
  if hi is None:
    hi = len(new_list)
    while lo < hi:
      mid = (lo+hi)//2
      midval = new_list[mid]
      if midval.name < name:
        lo = mid+1
      elif midval.name > name:
        hi = mid
      else:
        return new_list[mid]
    return "None"

def find_name_record(name_list,name,sex):
  return find_name_record_binary(name_list,name,sex)

def find_name_record_hashmap(name_dict,name,sex):
  name_tuple = (name,sex)
  if(name_dict[name_tuple]):
    return name_dict[name_tuple]
  else:
    return "None"




      



def plot_names(data, names=[]):
    """Plots the given list of names in a web-based visualization.

    Params:
        data  - a list of name records (e.g., tuples) to act as a data source
        names - a list of names (strings) which should be plotted
    """
    Record1 = namedtuple('Record','name sex year')
    record = Record1
    #print(names[1])
    import plotly
    from plotly.graph_objs import Scatter, Scattergl, Layout

    traces = [] #all the lines to draw

    for name in names:
        for sex in ['M','F']: # draw lines for both sexes:
            try:
                x_vals = [] #the years for each data point
                y_vals = [] #the ranks for each data point
                labels = [] #the labels for each data point
                year = {}
                record = find_name_record_hashmap(data,name,sex)
                #TODO: find the record for the name & sex
                # if the record exists (it may not!)
                # go through each year in the record
                #   add the year to the list of x_vals
                #   add the rank to the list of y_vals
                #   add a label (e.g., "Count: 598") to the list of labels
                if (record != "None"):
                #   if(record.sex == sex):
                #     for key,value in record.year.items():
                #       x_vals.append(key)
                #       y_vals.append(value[1])
                  for key,value in record.items():
                    x_vals.append(key)
                    y_vals.append(value[1])
                    labels.append(value[0])
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
  if (sys.argv[2]):
    rank = sys.argv[2]
    names_data = load_names_data(names_folder,rank)
  else:
    names_data = load_names_data(names_folder)
  #transformed_data = transform_data(names_data)
  #print(names_data)
  #print(transformed_data)
  #print (names_data[1880])
  #names_data = load_names_data(names_folder)
  names_to_plot = sys.argv[3:] #rest of the arguments are names to plot
  plot_names(names_data, names_to_plot)
    
  # cmd = None
  # datafile = None

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
