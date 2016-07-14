import pandas as pd
import numpy as np
import dateFunctions as df
import matplotlib.pyplot as plt

def loadFile():
    file1 = open('tempdata.txt', 'r')
    
    file1.readline()
    output = []
    header = cleanSpacedLine(file1.readline())
    for line in file1.readlines():
        output += [cleanCommadLine(line)[:-1]]
    output = np.array(output)
    output = pd.DataFrame(output, columns=header)
    output = output.drop(['USAF', 'I', 'Type', 'QCP', 'Q'], 1)
    output = output[output['NCDC'] != '99999']
    return output
    
def separateStations(data):
    """The input, data, is a dataframe output from loadFile. There is a column
       for station ID. This function separates out the data for each station
       and then does some cleaning to remove the "unknown station" ID "99999",
       change the times to be times from an initial point, and to interpolate
       the data to ensure that all stations have the same time values spaced
       out by 20 minutes.
    """
    d = data[data['NCDC'] != '99999']
    d['mins'] = df.toMinutes(d['Date'].values, d['HrMn'].values,
                             '20150131', '0000')
    max_val = int(max(d['mins']))/20*20
    stations = d['NCDC'].unique()
    output = pd.DataFrame(columns=['time'])    
    for s in stations:
        f = d[d['NCDC']==s]
        minutes, new_temps = respaceData(f['mins'].values,
                                         f['Temp'].astype('float'),
                                         20, 0, max_val)
        output[s] = new_temps
    output['time'] = minutes
    return output

def respaceData(minutes, y, spacing, start, end):
    """The data should have been collected in 15 minute intervals. The exact
        time difference varies. To deal with this, this function interpolates
        to ensure that there is data for each spacing minute reading.
        minutes - 1D array of the minutes of each measurement.
        y - 1D array of temperature readings for each measurement.
        spacing - int, the desired number of minutes between each reading.
        start - int, starting value.
        end - int, ending value.
    """
    #start = (int(minutes[0])/spacing+bool(minutes[0]%spacing))*spacing
    #end = int(minutes[-1])/spacing*spacing
    new_minutes = range(start, end+1, spacing)
    return new_minutes, np.interp(new_minutes, minutes, y)
    
def cleanCommadLine(s, convert_to_nums=False):
    """Takes a single line from a comma separated file. Breaks it into its
        constituent data.
        s - string. A single line with comma separated values.
        convert_to_nums - boolean or array. Whether numeric values should be
                          converted into floats of left as strings. If it is
                          boolean, all columns will try to be converted or
                          left as is. If it is an array of booleans, each
                          column will be effected as specified.
    """
    s = s.replace('\n','')
    s = s.split(',')
    output = []
    for k in s:
        k = k.strip()
        if convert_to_nums:
            try:
                k = float(k)
            except:
                pass
        output += [k]
    return output
        
def cleanSpacedLine(s, convert_to_nums=False):
    """Takes a single line from a space separated file. Breaks it into
        its consituent pieces.
        s - string. A single line with space separated values.
        convert_to_nums - boolean. Whether numeric values should be converted
                          into floats or left as strings.
    """
    s = s.replace('\n','')
    s = s.split(' ')
    v = []
    for k in s:
        if k != '':
            if convert_to_nums:
                try:
                    k = float(k)
                except:
                    pass
            v += [k]
    return v