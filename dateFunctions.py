import datetime as dt

def toMinutes(dates, HrMn, start_date, start_HrMn):
    """Converts a set of dates and times into values for minutes since the
       start.
       dates - array of strings of the form YYYYMMDD (1D, length N).
       HrMn - array of strings of the form HHMM  (1D, length N).
       start_date - string of the form YYYYMMDD.
       start_HrMn - string of the form HHMM.
       --------------------------------------------
       output - array of ints  (1D, length N). 
    """
    start_dt = dt.datetime(int(start_date[:4]), int(start_date[4:6]),
                           int(start_date[6:]), int(start_HrMn[:2]),
                           int(start_HrMn[2:]))
    output = [0]*len(dates)
    for i in range(len(dates)):
        new_dt = dt.datetime(int(dates[i][:4]), int(dates[i][4:6]),
                             int(dates[i][6:]), int(HrMn[i][:2]),
                             int(HrMn[i][2:]))
        output[i] = (new_dt-start_dt).total_seconds()/60.
    return output

def hyphenate(date):
    """Returns a hyphenated version of an unhyphenated date.
       date - YYYYMMDD.
    """
    return date[:4] + '-' + date[4:6] + '-' + date[6:]

def dehyphenate(date):
    """Returns a dehyphenated version of a hyphenated date.
       date - YYYY-MM-DD.
    """
    return date[:4] + date[5:7] + date[8:]

def hyphenated(date):
    """Returns True if the date is hyphenated.
    """
    return '-' in date

def futureDays(date, number_days):
    """Returns the date of a certain number of days in the future or past.
       date  - string. Either date type.
       number_days - int. Sould be negative for days in the past.
    """
    time = dateToDatetime(date)
    delta_time = dt.timedelta(number_days)
    return datetimeToDate(time+delta_time)

def nextYear(date):
    """Returns the date string of january 1st of the next year.
        date - YYYY-MM-DD or YYYYMMDD.
    """
    if hyphenated(date):
        return str(int(date[:4])+1) + '-01-01'
    else:
        return str(int(date[:4])+1) + '0101'

def yearEnd(date):
    """Returns the date string corresponding to december 31st of the year
       of the provided date.
       date - YYYY-MM-DD or YYYYMMDD.
    """
    if hyphenated(date):
        return date[:4] + '-12-31'
    else:
        return date[:4] + '1231'

def smallerDate(date1, date2):
    """Returns the date string which is smaller.
        date1 - YYYY-MM-DD or YYYYMMDD.
        date2 - YYYY-MM-DD or YYYYMMDD.
    """
    hyphens = False
    if hyphenated(date1):
        date1 = dehyphenate(date1)
        date2 = dehyphenate(date2)
        hyphens = True
    if int(date1) > int(date2):
        smaller = date1
    else:
        smaller = date2
    smaller = str(smaller)
    if hyphens:
        smaller = hyphenate(smaller)
    return smaller

def isBigger(date1, date2):
    """Returns True is date1 is greater than date2.
    """
    if hyphenated(date1):
        date1 = dehyphenate(date1)
        date2 = dehyphenate(date2)
    if int(date1) > int(date2):
        return True
    return False

def dateTrim(dates):
    """Removes any time data from the end of a date. Returning the YYYY-MM-DD.
        dates - list of strings.
    """
    return [x[:10] for x in dates]
    
def dayNumber(start_date, dates):
    """Takes in a list of dates. It returns how many days each of these is
        after the provided start_date.
        start_date - string. YYYY-MM-DD or YYYYMMDD, date which has the value 0.
        dates - list of strings. Format: YYYY-MM-DD or YYYYMMDD.
    """
    start = dateToDatetime(start_date)
    return [(dateToDatetime(x)-start).days for x in dates]
    
def dateToDatetime(date):
    """Takes in a date and returns the builtin datetime object.
        date - string. YYYY-MM-DD or YYYYMMDD.
    """
    if not hyphenated(date):
        date = hyphenate(date)
    ds = int(date[8:])
    ms = int(date[5:7])
    ys = int(date[:4])
    return dt.datetime(ys, ms, ds)

def datetimeToDate(datetime):
    """Takes in a year, month, day datetime and outputs a YYYYMMDD date.
       datetime - datetime.
    """
    year = str(datetime.year)
    month = '{:0>2d}'.format(datetime.month)
    day = '{:0>2d}'.format(datetime.day)
    return year + month + day
    
def contains(start_date, end_date, date1, date2=None):
    """Determines if date1 (and the optional date2) fall between start_date and
       end_date inclusive.
        start_date - string. Either date form.
        end_date - string. Either date form.
        date1 - string. Either date form.
        date2 - string (optional). Either date form.
    """
    #print start_date, end_date, date1, date2
    time1 = dateToDatetime(date1)
    start_time = dateToDatetime(start_date)
    end_time = dateToDatetime(end_date)
    if time1 >= start_time and time1 <= end_time:
        if date2 != None:
            time2 = dateToDatetime(date2)
            if time2 >= start_time and time2 <= end_time:
                return True
            else:
                return False
        else:
            return True
    return False
    