import json as js
import requests
import matplotlib.pyplot as plt
import numpy as np
import sys
import dateFunctions as df
import pandas

token = {'token':'DCuLsKnXYHAdEXGFLpeyOrNhbQDpcEdG'}

def getLatLong(ids):
    """Returns the latitude and longitude for a list of given stations.
    """
    baseurl = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/stations/'
    output = {}
    for i in ids:
        try:
            d = loadURL(baseurl+i)
            output[i] = [d['latitude'], d['longitude']]
        except KeyError:
            pass
    return output
    
def saveData(ds, vs, ids):
    """Adds the aquired data to the data file. Any missing days are replaced
        with NaNs. The date of 0 corresponds to Jan, 1 2010.
        ds - list of lists. The list of days for each station.
        vs - list of lists. The corresponding data values for each day/station.
        ids - list of string. All of the station IDs.
    """
    old_max = 0
    old_ids = []
    try:
        old_data = pandas.read_pickle('TMAXdata.pkl')
        old_ids = old_data.columns
        old_max = old_data.shape[0] - 1     
    except:
        pass
    max_date = max(max([x[-1] for x in ds]), old_max)
    dates = range(max_date+1)
    data = pandas.DataFrame(index=dates)
    for c in old_ids:
        data[c] = fillOut(old_data.index, old_data[c], dates, float('nan'))
    for i, newid in enumerate(ids):
        if newid not in old_ids:
            data[newid] = fillOut(ds[i], vs[i], dates, float('nan'))
    pandas.to_pickle(data, 'TMAXdata.pkl')       
        
def fillOut(dx, dy, fx, rv):
    """Makes dy align with fx. Creates an array of the same length as fx such
        that if output[i] = dy[j] when fx[i] == dx[j]. Anytime fx[i] is not 
        found in dx, the replacement value rv is used instead.
        dx - list of ordered values (probably ints) length==m.
        dy - list of number, string length=m.
        fx - list of ordered values (probably ints) length==n.
        rv - number, string.
    """
    dx = list(dx)
    output = fx[:]
    for i, v in enumerate(fx):
        try:
            output[i] = dy[dx.index(v)]
        except:
            output[i] = rv
    return output    

def checkStationData(stationID):
    url = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/stations/{}'
    url = url.format(stationID)
    return loadURL(url)

def loadStationData(stationID, startdate, enddate):
    url = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/data?'
    url += 'stationid={}&datasetid=GHCND&datatypeid=TMAX'
    url = url.format(stationID)
    d = getFullSet(url, startdate, enddate)
    dates = [x['date'] for x in d]    
    dates = df.dateTrim(dates)
    dates = df.dayNumber(startdate, dates)
    values = [x['value'] for x in d]
    return dates, values

def loadHourlyStationData(stationID, startdate, enddate):
    url = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/data?'
    url += 'stationid={}&datasetid=PRECIP_HLY'
    url = url.format(stationID)
    d = getFullSet(url, startdate, enddate)
    return d
    dates = [x['date'] for x in d]    
    dates = df.dateTrim(dates)
    dates = df.dayNumber(startdate, dates)
    values = [x['value'] for x in d]
    return dates, values   

def getFullSet(baseURL, startdate=None, enddate=None):
    """Obtains all the results from a base URL by repeated calls with
        increasing offsets. If time series data is desired, the startdate and
        enddate must be specified.
        baseURL - string. A URL string containing all the relavent information
                          other than the limit and offset.
        startdate - YYYY-MM-DD. The initial date.
        enddate - YYYY-MM-DD. The inclusive final date.
    """
    baseURL += '&limit=1000'
    offset = 0
    output = []
    if startdate != None:
        cstart = startdate
        cend = df.yearEnd(cstart)
        while True:
            if df.smallerDate(cend, enddate) == enddate:
                fullURL = baseURL+'&startdate={}&enddate={}'.format(cstart,
                                                                    enddate)
                new_data = loadURL(fullURL)['results']
                output += new_data
                return output
            fullURL = baseURL+'&startdate={}&enddate={}'.format(cstart,cend)          
            new_data = loadURL(fullURL)['results']
            output += new_data
            cstart = df.nextYear(cend)
            cend = df.yearEnd(cstart)          
                      
    while True:
        fullURL = baseURL + '&offset='+str(offset)
        try:
            new_data = loadURL(fullURL)['results']
            output += new_data
            offset += 1000
        except:
            break
    return output

def getData(reget=True):
    #Get the station ids for NC
    if reget == True:
        p = getAllStations('37')
        ids = [x['id'] for x in p]
        saveStationIds(ids)
    else:
        try:
            ids = openStationIds()
        except:
            p = getAllStations('37')
            ids = [x['id'] for x in p]
            saveStationIds(ids)
    ds = []
    vs = []
    oids = []
    print len(ids)
    for st in ids[:]:
        try:
            d, v  = loadStationData(st, '2010-01-01', '2014-12-31')
            ds += [d]
            vs += [v]
            oids += [st]
            print st + ' loaded'
        except:
            print st + ' failed'
    return ds, vs, oids
    
def openStationIds():
    file1 = open('NC_station_ids.txt', 'r')
    r = file1.read()
    file1.close()
    return r
    
def saveStationIds(ids):
    file1 = open('NC-Station_ids.txt', 'w')
    for i in ids:
        file1.write(i+'\n')
    file1.close()

def getAllStations(state_id):
    output = []
    start = 0
    while True:
        try:
            output += getHourStations(state_id, start=start)
            start += 1000
        except KeyError:
            break
    return output

def getStations(state_id, start=0, number=1000):    
    url = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/stations?'
    url += 'locationid=FIPS:{}&limit={}&offset={}&datasetid=GHCND'
    url += '&datatypeid=TMAX&startdate=2010-01-01&enddate=2014-12-31'
    url = url.format(state_id, number, start)
    return loadURL(url)['results']

def getHourStations(state_id, start=0, number=1000):
    url = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/stations?'
    url += 'locationid=FIPS:{}&limit={}&offset={}&datasetid=PRECIP_HLY'
    url += '&startdate=2010-01-01&enddate=2014-12-31'
    url = url.format(state_id, number, start)
    return loadURL(url)['results']
    
def loadURL(url):
    d = requests.get(url, headers=token)
    return js.loads(d.text)
    