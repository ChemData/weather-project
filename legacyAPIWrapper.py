import pandas as pd
import urllib2
import StringIO as StringIO
import time

#URL formation - http://www7.ncdc.noaa.gov/wsregistration/CDOServices.html
#web services: http://www.ncdc.noaa.gov/cdo-web/webservices/ncdcwebservices

####datatypes####
#TMP - temperature


token = 'bbigcbhFbcfIJIGGIlIm'

test = 'http://www7.ncdc.noaa.gov/rest/services/values/ish/72315003812/TMP/200101010000/200101312359'

def getStationsData(stationIDs, datatype, start_date, end_date):
    """Gets data from multiple stations in a specified range of dates.
       stationIDs - list of strings.
       datatype - string. Specifies what type of data to get.
       start_date - string with format YYYYMMDDHHMM.
       end_date - string with format YYYYMMDDHHMM.       
    """
    output = {}
    for ID in stationIDs:
        data = getStationData(ID, datatype, start_date, end_date)
        output[ID] = data
    return output
    
def getStationData(stationID, datatype, start_date, end_date):
    """Gets data from particular station in a specified range of
       dates.
       stationID - string.
       datatype - string. Specifies what type of data to get.
       start_date - string with format YYYYMMDDHHMM.
       end_date - string with format YYYYMMDDHHMM.
    """
    url = 'http://www7.ncdc.noaa.gov/rest/services/values/ish/{}/{}/{}/{}'
    url = url.format(stationID, datatype, start_date, end_date)
    print url
    data = getURL(url)
    output = pd.DataFrame()
    data = data[data[19] == 'FM-15']    
    output[['date', 'time', datatype]] = data[[2,3,5]]
    output.reset_index(drop=True, inplace=True)
    return output

def getStations(stateAbbrev):
    """Gets stations information from stations in a given state.
       stateAbbrev - string. Two letter abbreviation for a state.
    """
    url = 'http://www7.ncdc.noaa.gov/rest/services/sites/ish/stateAbbrev/{}'
    url = url.format(stateAbbrev)
    data = getURL(url)
    output = pd.DataFrame()
    output[['ID', 'name', 'lat', 'long', 'start', 'end']] = data[[1,3,4,5,8,9]]
    output['state'] = stateAbbrev
    output.reset_index(drop=True, inplace=True)
    return output
    

def getURL(url):
    """Takes a base URL and appends to token. Returns a dataframe of the
       corresponding data.
       url - string. A well formated url without token based on the rules
                     linked at the top of this page.
    """
    fullurl = url + '/?output=csv&token=' + token
    try:
        openurl = urllib2.urlopen(fullurl)
        csvstring = openurl.read()
        si = StringIO.StringIO(csvstring)
        print si
        return pd.read_csv(si, header=None)
    except urllib2.HTTPError as err:
        details = err.headers.headers
        for header in details:
            if 'Retry-After' in header:
                wait_time = int(header[13:].strip('\n').strip('\r'))
                time.sleep(wait_time+1)
                break
        return getURL(url)
        
    