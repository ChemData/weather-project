import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import legacyAPIWrapper as law
import dateFunctions as df
import time

states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL',
          'IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT',
          'NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI',
          'SC','SD','TN','TX','UT','VA','WA','WV','WI','WY']

def getAllStations(state_list):
    """Uses the API to get all the stations and their info. Save to an
       external file called 'AllStations'
       state_list - list of strings. two letter codes for states to get.
    """
        
    try:
        output = pd.read_pickle('all_stations.pkl') 
    except IOError:
        output = pd.DataFrame(columns=['ID', 'name', 'lat', 'long',
                                       'start', 'end', 'state'])
        output.to_pickle('all_stations.pkl')
    completed = []
    uncompleted = state_list[:]
    for state in state_list:
        print state
        try:
            output = pd.read_pickle('all_stations.pkl')
            output = output.append(law.getStations(state), ignore_index=True)
            output.to_pickle('all_stations.pkl')
            completed += [uncompleted.pop(0)]
        except:
            print 'Failed on ' + state
            break
    return completed, uncompleted
            
def findBestRange(stations, days, earliest=None):
    """Finds the range of dates which are present in the most of a set of
       station's data ranges.
       stations - DataFrame. Must contain columns start and end which contain
                             the start and end dates (in YYYYMMDD) of the data
                             for that station.
       days - int. Number of days the range should be.
       earliest - string. YYYYMMDD. Don't consider dates which start before
                             this.
    """
    stime = time.time()
    if earliest == None:
        earliest = str(int(min(stations['start'])))
    latest = df.futureDays(str(int(max(stations['end']))), -1*days)
    print earliest, latest
    best_start = earliest
    biggest_set = 0
    cur_start = earliest
    while True:
        print cur_start
        cur_end = df.futureDays(cur_start, days)
        count = 0
        for i, r in stations.iterrows():
            count += df.contains(str(int(r['start'])), str(int(r['end'])),
                                 cur_start, cur_end)
        if count >= biggest_set:
            biggest_set = count
            best_start = cur_start
        cur_start = df.futureDays(cur_start, 1)
        if df.isBigger(cur_start, latest):
            break
    print time.time()-stime
    return best_start, biggest_set
    
def getStationsInRange(stations, earliest, latest):
    """Returns a DataFrame with all the stations which have data in the
       specified time range.
       stations - DataFrame. Must contain start and end columns which give the
                             range of data for that station.
       earliest - string. YYYYMMDD.
       latest - string. YYYYMMDD.
    """
    indexes = []
    for i, r in stations.iterrows():
        if df.contains(str(int(r['start'])), str(int(r['end'])), earliest,
                       latest):
            indexes += [i]
    return stations.loc[indexes]